import os


def is_internet_alive():
    p = os.popen("nm-online")
    out = p.read()
    print("Terminal output: ", out)
    if when_online(out):
        return True
    return False


def when_online(out):
    res = out.split()
    for word in res:
        if word == "[online]":
            return True
    return False
