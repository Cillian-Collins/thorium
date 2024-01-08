from celery import Celery
from config.config import connect
from pwn import context
from submission import read_queue
import logging
import redis
import time

app = Celery('tasks')
app.config_from_object('celery_config')
cache = redis.StrictRedis(host="redis", port=6379)


@app.task
def run_submission_task():
    logging.getLogger('pwnlib').setLevel(logging.ERROR)
    p = connect()
    backoff_exponent = 1

    while True:
        if not read_queue(p, cache):
            backoff_exponent += 1
            backoff = pow(2, backoff_exponent)
            print(f"Rate limited. Sleeping for {backoff}s")
            time.sleep(backoff)
            return None
        else:
            backoff_exponent = 1
