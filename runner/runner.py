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
        result = subprocess.run(
            ["python3", f"/exploits/{exploit}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        if result.stderr:
            print(f"stderr running {exploit}: {result.stderr}")
        print(result.stdout)
        flags = re.findall(FLAG_REGEX, result.stdout)
        for flag in flags:
            flag_obj = {"flag": flag, "exploit": exploit, "target": ip}
            cache.rpush("submissions", json.dumps(flag_obj))


def install_exploit_dependencies():
    print("Installing dependencies for exploits")
    os.system("pipreqs . --force >/dev/null 2>&1")
    os.system("pip install -r requirements.txt >/dev/null 2>&1")
