from celery import Celery
from config.config import connect, submit
from submission import read_queue
from tasks import run_submission_task
import concurrent.futures
import redis


def main():
    app = Celery('tasks')
    app.config_from_object('celery_config')
    cache = redis.StrictRedis(host="redis", port=6379)

    p = connect()

    while True:
        run_submission_task(p, cache)


if __name__ == "__main__":
    main()
