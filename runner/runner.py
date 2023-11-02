import json
import os
import re
import subprocess


FLAG_REGEX = os.getenv("FLAG_REGEX")


def run(exploits, ip, extra):
    for exploit in exploits:
        env = os.environ.copy()
        env['TARGET'] = ip
        env['EXTRA'] = json.dumps(extra)
        result = subprocess.run(['python3', f'/exploits/{exploit}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        if result.stderr:
            print(result.stderr)
        flags = re.findall(FLAG_REGEX, result.stdout)
        print(flags)
