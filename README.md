<h1 align="center">
    <img src="server/static/images/logo.png" width="200px" alt="Thorium">
    <br>
    <span>Thorium</span>
</h1>
<div align="center">Thorium is an exploit manager for Attack/Defence CTF competitions.</div>

### Getting Started
You will need Docker installed to run this application.
```shell
docker compose up --build
```
This will spawn the necessary containers and the application will be available on port 5000.

### Initial Configuration
You should modify the `.env` file to use the correct values for the competition you are playing.

### Runner Configuration
You must write a config file (Python) for the Runner container. This is located in `config/runner/config.py` and should define an `info()` function which returns a list of IPs to attack and extra information (usually JSON containing flag IDs).

An example script looks like:
```python
import requests


def info():
    # Send a request to teams.json and fetch the ips and extra info
    r = requests.get("http://10.10.254.254/competition/teams.json")
    ips = r.json()['teams']
    extra = r.json()['services']
    return ips, extra
```

### Submission Configuration
You will also need to write a config file (Python) for the Submission container. This is located in `config/submission/config.py` and should define a function `connect()` to establish a connection with the flag submission service and `submit(p, flag)` which uses that session to send flags. It should then return a valid status (`"OK", "OLD", "DUP", "INV", "OWN", "ERR"`) for inclusion on the Server.

An example script looks like:
```python
from pwn import *


def connect():
    p = remote("10.10.254.254", 31337)
    return p


def submit(p, flag):
    resp = p.sendline(flag.encode()).decode()
    if "OK" in resp:
        return "OK"
    elif 

```

### Writing Exploits
Exploits can be uploaded directly via the Thorium server. Exploits should be a standalone Python file with the following function signature:
```python
import json
import os

# Load target host
target = os.getenv("TARGET")
# Load extra data - normally requires json.loads()
extra = json.loads(os.getenv("EXTRA"))
# Find flags
flags = [...]
# Print flags to stdout
print(flags)
```
This is where `target` is the IP address of the target and `extra` is the extra information being passed in (usually some JSON containing flag ids).

Simply print the flags found and the runner will regex match valid flags from stdout and submit them.

### Credits
Copyright &copy; 2023 [Cillian Collins](https://github.com/Cillian-Collins)