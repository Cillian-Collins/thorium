from pwn import *


def connect():
    p = remote("ip", 1337)
    return p


def submit(p, flag):
    p.sendline(flag.encode())
    return "OK"
