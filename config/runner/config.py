import random
import string


def info():
    # Send a request to teams.json and fetch the ips and extra info
    ips = [f"10.10.10.{i+1}" for i in range(10)]
    extra = {}
    for ip in ips:
        extra_arr = ["".join([random.choice(string.ascii_letters) for i in range(5)]) for j in range(5)]
        extra[ip] = extra_arr
    return ips, extra
