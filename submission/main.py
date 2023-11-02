from config.config import connect, submit
from db import insert_submission
import json
import redis
import sqlite3
import threading


def main():
    cache = redis.StrictRedis(host="redis", port=6379)

    p = connect()

    while True:
        _, message = cache.brpop("submissions")
        flag_obj = json.loads(message.decode())
        if flag_obj:
            flag = flag_obj["flag"]
            exploit = flag_obj["exploit"]
            target = flag_obj["target"]
            try:
                status = submit(p, flag)
            except:
                status = "ERR"

            if status not in ["OK", "OLD", "DUP", "INV", "OWN", "ERR"]:
                status = "ERR"

            local = threading.local()
            if not hasattr(local, "conn"):
                local.conn = sqlite3.connect("/database/database.db")
            insert_submission(flag, status, target, exploit)


if __name__ == "__main__":
    main()
