#!/usr/bin/env python
"""This allows for swirling the disk at the top of the tree."""

from dotstar import tree_lights
import time
import random


# Module information:
__author__ = "Lucien Gaitskell"
__credits__ = ["Lucien Gaitskell"]
__version__ = "1.0"
__maintainer__ = "Lucien Gaitskell"
__status__ = "Development"


# Initialize the strip:
tree = tree_lights.TreeLights()  # slower rate

# DISK SWIRL:
startOfDisk = tree_lights.TreeLightSectionPositions.startOfDisk
endOfDisk = tree_lights.TreeLightSectionPositions.endOfDisk

swirlHead  = startOfDisk    # Index of first 'on' pixel
swirlTail  = startOfDisk-10  # Index of last 'off' pixel
swirlColor = [32, 0, 0]


def swirlDiskStep():
    """Step the swirl on the disk at the top of the tree."""
    global swirlHead
    global swirlTail
    global swirlColor

    tree.setPixel(swirlHead, *swirlColor)  # Turn on 'head' pixel
    tree.setPixel(swirlTail, 0)     # Turn off 'tail'
    tree.show()                     # Refresh strip
    time.sleep(1.0 / 50)             # Pause 20 milliseconds (~50 fps)

    swirlHead += 1                        # Advance head position
    if(swirlHead >= endOfDisk):           # Off end of strip?
        swirlHead = startOfDisk              # Reset to start

    swirlTail += 1                        # Advance tail position
    if(swirlTail >= endOfDisk):
        swirlTail = startOfDisk  # Off end? Reset


# TWINKLE TREE BASE:
startOfBase = tree_lights.TreeLightSectionPositions.startOfBase
endOfBase = tree_lights.TreeLightSectionPositions.endOfBase


def baseTwinkleOnce():
    """Twinkle the base lights on the tree once."""
    for px in range(startOfBase, endOfBase):
        # Get a random number in a specific range:
        randomNumb = random.randrange(4, 33, 1)
        tree.setPixel(px, 0, int(randomNumb*1.5), randomNumb)
    tree.show()


if __name__ == "__main__":
    try:
        while True:
            # Update the Disk Swirl:
            swirlDiskStep()

            # Update base twinkle:
            baseTwinkleOnce()
    except KeyboardInterrupt:
        # Shutdown pixels on interrupt:
        tree.zeroAllPixels()
