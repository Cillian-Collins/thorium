import json
import os
import re
import redis
import subprocess


FLAG_REGEX = os.getenv("FLAG_REGEX")
cache = redis.Redis(host="redis", port=6379)


def run(exploits, ip, extra):
    for exploit in exploits:
        env = os.environ.copy()
        env["TARGET"] = ip
        env["EXTRA"] = json.dumps(extra)
        result = subprocess.run(
            ["python3", f"/exploits/{exploit}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        if result.stderr:
            print(result.stderr)
        flags = re.findall(FLAG_REGEX, result.stdout)
        for flag in flags:
            flag_obj = {"flag": flag, "exploit": exploit, "target": ip}
            cache.rpush("submissions", json.dumps(flag_obj))
