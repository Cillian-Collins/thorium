from celery import Celery
from config.config import info
from db import fetch_active_exploits, fetch_targets
from runner import run, install_exploit_dependencies
from tasks import run_exploit_task
import concurrent.futures
import os
import sqlite3
import threading
import time


TICK_LENGTH_SECONDS = int(os.getenv("TICK_LENGTH_SECONDS", "60"))


if __name__ == "__main__":
    app = Celery('tasks')
    app.config_from_object('celery_config')
    while True:
        t = time.time()
        local = threading.local()

        if not hasattr(local, "conn"):
            local.conn = sqlite3.connect("/database/database.db")
        items = fetch_active_exploits()
        exploits = [x[0] for x in items]

        install_exploit_dependencies()

        ips, extra = [target[0] for target in fetch_targets()], info()

        for ip in ips:
            run_exploit_task.delay(exploits, ip, extra)

        time_elapsed = time.time() - t
        with open("/stats/time.txt", "w") as f:
            f.write(str(time_elapsed))
        if time_elapsed < TICK_LENGTH_SECONDS:
            time.sleep(TICK_LENGTH_SECONDS - time_elapsed)
