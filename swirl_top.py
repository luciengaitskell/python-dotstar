#!/usr/bin/env python
"""This allows for swirling the disk at the top of the tree."""

from dotstar import tree_lights
import time


# Module information:
__author__ = "Lucien Gaitskell"
__credits__ = ["Lucien Gaitskell"]
__version__ = "1.0"
__maintainer__ = "Lucien Gaitskell"
__status__ = "Development"

startOfDisk = 3*300
endOfDisk = 3*300+255


# Initialize the strip:
tree = tree_lights.TreeLights()  # slower rate


def swirlDisk():
    """Swirl the disk at the top of the tree."""
    head  = startOfDisk    # Index of first 'on' pixel
    tail  = startOfDisk-10  # Index of last 'off' pixel
    color = [32, 0, 0]

    while True:                              # Loop forever
        tree.setPixel(head, *color)  # Turn on 'head' pixel
        tree.setPixel(tail, 0)     # Turn off 'tail'
        tree.show()                     # Refresh strip
        time.sleep(1.0 / 50)             # Pause 20 milliseconds (~50 fps)

        head += 1                        # Advance head position
        if(head >= endOfDisk):           # Off end of strip?
            head = startOfDisk              # Reset to start

        tail += 1                        # Advance tail position
        if(tail >= endOfDisk):
            tail = startOfDisk  # Off end? Reset


if __name__ == "__main__":
    try:
        # Run the main function:
        swirlDisk()
    except KeyboardInterrupt:
        # Shutdown pixels on interrupt:
        tree.zeroAllPixels()
