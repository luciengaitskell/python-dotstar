#!/usr/bin/env python
"""This allows for twinkling the lights on the tree."""

import random
import time
from dotstar import tree_lights

# Module information:
__author__ = "Lucien Gaitskell"
__credits__ = ["Lucien Gaitskell"]
__version__ = "1.0"
__maintainer__ = "Lucien Gaitskell"
__status__ = "Development"


# Initialize the strip:
tree = tree_lights.TreeLights()  # slower rate


# Main 'run' function:
def run():
    """Twinkle the lights on the tree."""
    while True:
        for px in range(tree_lights.NUM_PIXELS):
            # Get a random number in a specific range:
            randomNumb = random.randrange(4, 33, 1)
            tree.setPixel(px, 0, int(randomNumb*1.5), randomNumb)
        tree.show()
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        # Run the main function:
        run()
    except KeyboardInterrupt:
        # Shutdown pixels on interrupt:
        tree.zeroAllPixels()
