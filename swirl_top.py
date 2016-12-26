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

    swirlHead += 1                        # Advance head position
    if(swirlHead >= endOfDisk):           # Off end of strip?
        swirlHead = startOfDisk              # Reset to start

    swirlTail += 1                        # Advance tail position
    if(swirlTail >= endOfDisk):
        swirlTail = startOfDisk  # Off end? Reset

    appendColor = swirlColor[0]
    del swirlColor[0]
    swirlColor.append(appendColor)


# TWINKLE TREE BASE:
startOfBase = tree_lights.TreeLightSectionPositions.startOfBase
endOfBase = tree_lights.TreeLightSectionPositions.endOfBase

colorChangeIndex = 0


def baseTwinkleOnce():
    """Twinkle the base lights on the tree once."""
    global colorChangeIndex

    for px in range(startOfBase, endOfBase):
        # Get a random number in a specific range:
        randomNumb = random.randrange(4, 33, 1)
        color = []

        for ii in range(colorChangeIndex):
            color.append(0)
        color.append(randomNumb)
        for ii in range(3 - (colorChangeIndex + 1)):
            color.append(0)

        colorChangeIndex += 1
        if colorChangeIndex > 2:
            colorChangeIndex = 0
        tree.setPixel(px, 0, randomNumb, 0)


if __name__ == "__main__":
    try:
        swirlTime = time.time()
        swirlSleepTime = 0.02
        twinkleTime = time.time()
        twinkleSleepTime = 0.05
        while True:

            if time.time() - swirlTime > swirlSleepTime:
                # Update the Disk Swirl:
                swirlDiskStep()
                swirlTime = time.time()

            if time.time() - twinkleTime > twinkleSleepTime:
                # Update base twinkle:
                baseTwinkleOnce()
                twinkleTime = time.time()

            tree.show()                     # Refresh strip
            time.sleep(1.0 / 50)             # Pause 20 milliseconds (~50 fps)
    except KeyboardInterrupt:
        # Shutdown pixels on interrupt:
        tree.zeroAllPixels()
