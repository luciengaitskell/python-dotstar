#!/usr/bin/env python
"""This allows for twinkling the lights on the tree."""

import random
import time
from dotstar import Adafruit_DotStar

# Module information:
__author__ = "Lucien Gaitskell"
__credits__ = ["Lucien Gaitskell"]
__version__ = "1.0"
__maintainer__ = "Lucien Gaitskell"
__status__ = "Development"


# 3 Strips + Disk + Square:
numpixels = 3*300+255+256

# Initialize the strip:
strip = Adafruit_DotStar(numpixels, 4000000)  # slower rate

strip.begin()            # Initialize pins for output
strip.setBrightness(64)  # Limit brightness to ~1/4 duty cycle

# List bad pixels to ignore:
badPixels = [593, 594]


# Equivalent to 'strip.setPixelColor' with bad pixel ignoring:
def __setPixel(px, *args, **kwargs):
    if px not in badPixels:
        strip.setPixelColor(px, *args, **kwargs)


# Shut down all pixels:
def shutDownAllPixels():
    """Shut down all lights on the tree."""
    for px in range(numpixels):
        if px not in badPixels:
            __setPixel(px, 0, 0, 0)
    strip.show()


# Main 'run' function:
def run():
    """Twinkle the lights on the tree."""
    while True:
        for px in range(numpixels):
            # Get a random number in a specific range:
            randomNumb = random.randrange(4, 33, 1)
            __setPixel(px, 0, int(randomNumb*1.5), randomNumb)
        strip.show()
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        # Run the main function:
        run()
    except KeyboardInterrupt:
        # Shutdown pixels on interrupt:
        shutDownAllPixels()
