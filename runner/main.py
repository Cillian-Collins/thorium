from config.config import info
from db import fetch_active_exploits
from runner import run
import concurrent.futures
import os
import sqlite3
import threading
import time


TICK_LENGTH_SECONDS = int(os.getenv("TICK_LENGTH_SECONDS", "60"))


if __name__ == "__main__":
    while True:
        t = time.time()
        local = threading.local()

        if not hasattr(local, "conn"):
            local.conn = sqlite3.connect("/database/database.db")
        items = fetch_active_exploits()
        exploits = [x[0] for x in items]

        ips, extra = info()

        with concurrent.futures.ThreadPoolExecutor(50) as executor:
            futures = [executor.submit(run, exploits, ip, extra) for ip in ips]
            concurrent.futures.wait(futures)
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(e)
        time_elapsed = time.time() - t
        with open("/stats/time.txt", "w") as f:
            f.write(str(time_elapsed))
        if time_elapsed < TICK_LENGTH_SECONDS:
            time.sleep(TICK_LENGTH_SECONDS - time_elapsed)
