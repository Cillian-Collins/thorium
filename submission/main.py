from config.config import connect, submit
from db import insert_submission
import json
import redis
import sqlite3
import threading


def main():
    print("Connecting to Redis")
    # Connect to the Redis server
    cache = redis.StrictRedis(host='redis', port=6379)

    p = connect()

    while True:
        _, message = cache.brpop("submissions")
        flag_obj = json.loads(message.decode())
        if flag_obj:
            flag = flag_obj['flag']
            exploit = flag_obj['exploit']
            status = submit(p, flag)

            local = threading.local()
            if not hasattr(local, "conn"):
                local.conn = sqlite3.connect('/database/database.db')
            insert_submission(flag, status, exploit)


if __name__ == '__main__':
    main()
