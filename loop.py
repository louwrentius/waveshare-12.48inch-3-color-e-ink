#!/usr/bin/env python3
from datetime import datetime, timedelta
import subprocess
import time


imagelist = [
    {"filename": "test_images/nzflag.svg", "fuzz": None},
    {"filename":"test_images/redpainting.jpg", "fuzz": None},
    {"filename":"test_images/redwhiteblack-art.jpg", "fuzz": None},
    {"filename":"test_images/textile.jpg", "fuzz": None},
    {"filename":"test_images/stpaul.jpg", "fuzz": None},
    {"filename": "test_images/banksy.jpg", "fuzz": 40},
    {"filename": "test_images/art-cropped.jpg", "fuzz": None},
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