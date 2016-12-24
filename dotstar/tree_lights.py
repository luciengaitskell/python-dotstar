"""A library with useful functions for running the tree lights."""

from . import Adafruit_DotStar


NUM_PIXELS = 3*300+255+256  # 3 Strips + Disk + Square
SPI_SPEED = 4000000  # slower rate
BADPIXELS = [593, 594]


class TreeLights(object):
    """Allows for easy control of the tree lights."""

    def __init__(self):
        """Initialize the DotStar lights."""
        self.lights = Adafruit_DotStar(NUM_PIXELS, SPI_SPEED)
        self.lights.begin()            # Initialize pins for output
        self.lights.setBrightness(64)  # Limit brightness to ~1/4 duty cycle

    def setPixel(self, px, *args, **kwargs):
        """Set a pixel on the strip.

        Equivalent to 'strip.setPixelColor' with bad pixel ignoring.
        """
        if px not in BADPIXELS:
            self.lights.setPixelColor(px, *args, **kwargs)

    def show(self):
        """Update the lights."""
        self.lights.show()

    def zeroAllPixels(self):
        """Shut down all lights on the tree."""
        for px in range(NUM_PIXELS):
            self.setPixel(px, 0, 0, 0)
        self.show()
