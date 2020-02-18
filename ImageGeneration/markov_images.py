# Author: William Lucca

import sys
from PIL import Image


markov_data = dict()


def record_pair(color1, color2):
    """Add a single pixel color pair to the markov pairs data"""
    if color1 not in markov_data:
        markov_data[color1] = {color2: 1}
    else:
        if color2 not in markov_data[color1]:
            markov_data[color1][color2] = 1
        else:
            markov_data[color1][color2] += 1
    

if __name__ == '__main__':
    # Get images from input and add to markov data
    for argv in sys.argv[1:]:
        image = Image.open(argv)
        for x in range(1, image.width):
            for y in range(1, image.height):
                # Add color pair from left to right
                record_pair(image.getpixel((x, y)), image.getpixel((x - 1, y)))
                # Add color pair from top to bottom
                record_pair(image.getpixel((x, y)), image.getpixel((x, y - 1)))
        image.close()
