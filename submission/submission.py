from config.config import submit
from db import insert_submissions
import json
import sqlite3
import threading


def read_queue(p, cache):
    flag_objs = []
    while check_queue(cache) > 0:
        _, message = cache.brpop("submissions")
        flag_obj = json.loads(message.decode())
        flag_objs.append(flag_obj)
    if len(flag_objs) > 0:
        flags = [flag_obj['flag'] for flag_obj in flag_objs]
        #flag = flag_obj["flag"]
        #exploit = flag_obj["exploit"]
        #target = flag_obj["target"]
        status = submit(p, flags)

        for i in range(len(flag_objs)):
            if i < len(status):
                flag_objs[i]['status'] = status[i] if status[i] in ["OK", "OLD", "DUP", "INV", "OWN", "ERR"] else "ERR"
            else:
                flag_objs[i]['status'] = 'ERR'
            #if flag_obj[i]['status'] == "ERR":
                #flag_obj[i]["iter"] += 1
                #cache.rpush("submissions", json.dumps(flag_obj))
        local = threading.local()
        if not hasattr(local, "conn"):
            local.conn = sqlite3.connect("/database/database.db")
        submissions = []
        for flag_obj in flag_objs:
            flag = flag_obj["flag"]
            exploit = flag_obj["exploit"]
            target = flag_obj["target"]
            status = flag_obj["status"]
                
            submissions.append([flag, status, target, exploit])
        insert_submissions(submissions)
        return True

def check_queue(cache):
    return cache.llen("submissions")
