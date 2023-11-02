import os
import re
import subprocess


FLAG_REGEX = os.getenv("FLAG_REGEX")


def run(exploit):
    result = subprocess.run(['python3', f'/exploits/{exploit}'], stdout=subprocess.PIPE, text=True)
    flags = re.findall(FLAG_REGEX, result.stdout)
    print(flags)
