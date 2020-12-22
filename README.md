# Waveshare 12.48 inch red/black/white image display tool

This tool is written in Python for the [Waveshare 13.48 inch three-color display][ws]. 

[ws]: https://www.waveshare.com/product/displays/e-paper/epaper-1/12.48inch-e-paper-module-b.htm

[![e-paper][image]][large]

[image]: https://louwrentius.com/static/images/epaper/epaper04_small.jpg
[large]: https://louwrentius.com/static/images/epaper/epaper04_large.jpg

This display supports three colors black, white and red. 

By default, the display needs two images, one in black and white and a second one in red and white. Processing regular images, separating the colors and displaying them is a cumbersome process.

Therefore, this tool automates these steps (using Imagemagick) making it very simple to display an image on the e-paper display. 

Example: 

    ./dispay -i <image file.jpg> [--rotate 90] [--fuzz 35]

The color red is extracted from the original image and drawn separately. This process is not always perfect and can be tuned with the --fuzz parameter. The value is a percentage. By supplying a higher or lower value, the image may look better (less or more redness).

Drawbacks: on a Raspberry Pi 3B+, it takes about 55 seconds for an image to be displayed. The python library and display take about 30 seconds, the rest is for the Imagemagick image processing. 

### Requirements: 

You need to install Imagemagick.

    apt install imagemagick

### Modified library

The python library as supplied by Waveshare and as included in this repository has been modified.
The modifications make the library less verbose and it won't do a double image conversion to monochrome, improving image quality.

### Extra example programs

Depending on the application, it may be easier, or more desired to just draw an image programatically using the Python PIL library. Two example programs have been included. 

    - rectangles.py
    - circles.py

### Loop.py

This is a very simple program that loops through a list of images and displays them with a defined interval in between. By default, the image is changed every hour.

The file needs to be edited to add the appropriate filenames and  - if required - a Fuzz percentage.
