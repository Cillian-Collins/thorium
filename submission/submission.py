from config.config import submit
from db import insert_submission
import json
import sqlite3
import threading


def read_queue(p, cache):
    _, message = cache.brpop("submissions")
    flag_obj = json.loads(message.decode())
    if flag_obj:
        flag = flag_obj["flag"]
        exploit = flag_obj["exploit"]
        target = flag_obj["target"]
        status = submit(p, flag)

        if status not in ["OK", "OLD", "DUP", "INV", "OWN", "ERR"]:
            status = "ERR"

        local = threading.local()
        if not hasattr(local, "conn"):
            local.conn = sqlite3.connect("/database/database.db")
        print("Inserting", flag, status, target, exploit)
        insert_submission(flag, status, target, exploit)
