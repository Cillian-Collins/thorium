from db import fetch_active_exploits
from runner import run
import concurrent.futures
import os
import sqlite3
import threading
import time


TICK_LENGTH_SECONDS = int(os.getenv("TICK_LENGTH_SECONDS"))


if __name__ == "__main__":

    while True:
        local = threading.local()

        if not hasattr(local, "conn"):
            local.conn = sqlite3.connect('/database/database.db')
        items = fetch_active_exploits()
        exploits = [x[0] for x in items]

        with concurrent.futures.ThreadPoolExecutor(50) as executor:
            futures = [executor.submit(run, exploit) for exploit in exploits]
            concurrent.futures.wait(futures)
        time.sleep(TICK_LENGTH_SECONDS)
