<h1 align="center">
    <img src="server/static/images/logo.png" width="200px" alt="Thorium">
    <br>
    <span>Thorium</span>
</h1>
<div align="center">Thorium is an exploit manager for Attack/Defence CTF competitions.</div>

### Getting Started
You will need Docker installed to run this application.
```shell
docker compose up
```
This will spawn the necessary containers and the application will be available on port 5000.

### Writing Exploits
Exploits can be uploaded directly via the Thorium server. Exploits should be a standalone Python file with the following function signature:
```python
def exploit(ip, extra):
    ...
    print(flag)
```
This is where `ip` is the IP address of the target and `extra` is the extra information being passed in (usually some JSON containing flag ids).

You must always print the flags which you find the runner will regex match valid flags from stdout and submit them.

### Credits
Copyright &copy; 2023 [Cillian Collins](https://github.com/Cillian-Collins)