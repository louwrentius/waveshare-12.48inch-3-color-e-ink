#!/usr/bin/env python3
import sys
import os
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
print(libdir)
import epd12in48b
import time
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from PIL import Image

print("12.48inch e-paper B Demo...")
epd = epd12in48b.EPD()
# Initialize library.
epd.Init()
print("clearing...")
#epd.clear()

# Create blank image for drawing.
Blackimage = Image.new("1", (epd12in48b.EPD_WIDTH, epd12in48b.EPD_HEIGHT), 255)
Redimage = Image.new("1", (epd12in48b.EPD_WIDTH, epd12in48b.EPD_HEIGHT), 255)
Blackdraw = ImageDraw.Draw(Blackimage)
Reddraw = ImageDraw.Draw(Redimage)


print("drawing...")

screen_x = 1304
screen_y = 984

step = 30 
color = { 0: { 'canvas': Blackdraw, 'fill': "BLACK"} , 1: { 'canvas': Reddraw, 'fill': "BLACK"}, 2: { 'canvas': Blackdraw, 'fill': "WHITE" }, 3: { 'canvas': Reddraw, 'fill': "WHITE" }}

color_select = 0 
x = 0
y = 0 
for x in range(0,int(screen_x/2),step):
    for y in range(0,int(screen_y/2),step):
        if x == y:
            print(f"{x},{y}", end=' ')
            color[color_select]['canvas'].ellipse([(x,y),(screen_x-x,screen_y-y)], fill=color[color_select]['fill'])
            if color_select == 1:
                color[3]['canvas'].ellipse([(x+step,y+step),(screen_x-(x+step),screen_y-(y+step))], fill=color[3]['fill'])

            color_select+=1
            if color_select == 3:
              color_select = 0

epd.display(Blackimage, Redimage)
epd.EPD_Sleep()
