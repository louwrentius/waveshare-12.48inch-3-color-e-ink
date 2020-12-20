#!/usr/bin/env python3
from datetime import datetime, timedelta
import subprocess
import time


imagelist = [
    {"filename": "flag.jpg", "fuzz": 35},
    {"filename":"redpainting.jpg", "fuzz": None},
    {"filename":"mrrobot.jpg", "fuzz": None},
    {"filename":"street.png", "fuzz": None},
    {"filename":"St._Paul's_Cathedral_black_white_and_red.jpg", "fuzz": None},
    {"filename": "banksy01.jpg", "fuzz": 40},
]

def run_cmd(cmdline):
    convert = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = convert.communicate()
    if len(stderr) > 1:
        print(stderr)
    return stdout.decode("UTF-8")

while True:
    item = imagelist.pop()
    imagelist.insert(0,item)

    cmdline = ["./display.py", "-i", item["filename"]]

    if item["fuzz"]:
        cmdline.append("-f")
        cmdline.append(f"{str(item['fuzz'])}")

    print(item["filename"])
    run_cmd(cmdline)

    dt = datetime.now() + timedelta(hours=1)
    #dt = dt.replace(minute=0)
    while datetime.now() < dt:
        time.sleep(60)