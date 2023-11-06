from config.config import connect, submit
from submission import read_queue
import concurrent.futures
import redis


def main():
    cache = redis.StrictRedis(host="redis", port=6379)

    p = connect()

    while True:
        with concurrent.futures.ThreadPoolExecutor(20) as executor:
            futures = [executor.submit(read_queue, p, cache) for i in range(20)]
            concurrent.futures.wait(futures)
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    main()
