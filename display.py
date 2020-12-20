#!/usr/bin/env python3
#
# The three-color (black/white/red) Waveshare 12.48 inch e-ink display works by writing two images to the display.
# The first image is for black and white, the second is for red and white display. 
#
# This script uses imagemagick's convert to read a regular image and split it into two images. One for black and white
# the other for red and white display.
#
# The -f fuzz parameter may help getting better red color coverage for images with little red in them.
#
# The end-to-end display of an image on a Raspberry Pi 3B+ is over a minute, this is 'normal'. 
#
import sys
import os
import time
import random
import subprocess
import argparse
from PIL import Image

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import epd12in48b

def check_args(settings):
    parser = argparse.ArgumentParser(
        description="This script converts and displays an image on the Waveshare 12.48inch e-Paper Module (B) (black red white)"
    )
    ag = parser.add_argument_group(title="Generic Settings")
    ag.add_argument("-i", "--image", help="The image to be displayed.", required=True)

    ag.add_argument(
        "-r", "--rotate", help="Specify rotation in degrees." 
    )
    ag.add_argument("-f", "--fuzz", help="How fuzzy (in percent) the process of red color extraction should be."
         "Higher percentages can improve image quality with low amounts of red in the image.")
    try:
        args = parser.parse_args()
    except OSError:
        parser.print_help()
        sys.exit(1)

    args = vars(args)

    if not os.path.exists(args["image"]):
        print(f"Specified file {args['image']} does not exist.")
        sys.exit(1)

    settings.update(args)
    return settings

def run_cmd(cmdline):
    convert = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = convert.communicate()
    if len(stderr) > 1:
        print(stderr)
    return stdout.decode("UTF-8")

def convert_image(settings):
    res = settings["resolution"]
    image = settings["image"]
    black = settings["black_image"]
    red = settings["red_image"]
    fuzz = "30%"

    if settings["fuzz"]:
        fuzz = str(settings["fuzz"]) + "%"

    cmd_black = ["convert", image, "-resize", res, "-gravity", "center", "-crop", res, "-extent", res, black]
    cmd_red =   ["convert", image, "-resize", res, "-gravity", "center", "-crop", res, "-extent", res, "-channel", "rgba", "-fuzz", fuzz, "-fill", "none", "+opaque", "red", "-monochrome", "-depth", "4", "-negate", red]

    if settings["rotate"]:
        rotate = settings["rotate"] 
        cmd_black.insert(2, "-rotate")
        cmd_black.insert(3, rotate)
        cmd_red.insert(2, "-rotate")
        cmd_red.insert(3, rotate)

    run_cmd(cmd_black)
    run_cmd(cmd_red)

def display_image(settings):
    epd = epd12in48b.EPD()
    epd.Init()
    epd.clear()
    Blackimage = Image.open(settings["black_image"])
    Redimage = Image.open(settings["red_image"])
    epd.display(Blackimage, Redimage)
    epd.EPD_Sleep()

def get_settings():
    rand = int(random.random() * 10000) 
    settings = { "black_image": f"/tmp/black-{rand}.png", 
                 "red_image": f"/tmp/red-{rand}.png",
                 "resolution": "1304x984",
                 "fuzz": None
            }
    return settings

def cleanup(settings):
    black = settings["black_image"]
    red = settings["red_image"]
    if os.path.exists(black):
        os.remove(black)
    if os.path.exists(red):
        os.remove(red)

def main():
    settings = get_settings()
    settings = check_args(settings)
    convert_image(settings)
    try:
        display_image(settings)
    except Exception as ex: 
        print(ex)
    finally:
        cleanup(settings)

if __name__ == "__main__":
    main()