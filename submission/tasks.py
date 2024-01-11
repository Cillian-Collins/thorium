from celery import Celery
from config.config import connect
from pwn import context
from submission import read_queue, check_queue
import logging
import os
import redis
import time

BATCH_NUM_SECONDS = int(os.getenv("BATCH_NUM_SECONDS"))
BATCH_NUM_TOTAL = int(os.getenv("BATCH_NUM_TOTAL"))

app = Celery('tasks')
app.config_from_object('celery_config')
cache = redis.StrictRedis(host="redis", port=6379)


@app.task
def run_submission_task():
    LAST_RUN = time.time()
    logging.getLogger('pwnlib').setLevel(logging.ERROR)
    p = connect()
    backoff_exponent = 1

    while True:
        print(f"Flags in queue: {check_queue(cache)}")
        if BATCH_NUM_SECONDS and time.time() - LAST_RUN < BATCH_NUM_SECONDS:
            time.sleep(BATCH_NUM_SECONDS - LAST_RUN)
        elif check_queue(cache) < BATCH_NUM_TOTAL:
            continue
        elif not read_queue(p, cache):
            LAST_RUN = time.time()
            backoff_exponent += 1
            backoff = pow(2, backoff_exponent)
            print(f"Rate limited. Sleeping for {backoff}s")
            time.sleep(backoff)
            return None
        else:
            backoff_exponent = 1
