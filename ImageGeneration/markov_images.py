# Author: William Lucca

import sys
import random
from PIL import Image


num_pairs = 0
markov_data = dict()


def record_pair(color1, color2):
    """Add a single pixel color pair to the markov pairs data"""
    global num_pairs
    
    # Keep track of how many data points have been added
    num_pairs += 1
    
    # Add pair to dicts
    if color1 not in markov_data:
        markov_data[color1] = {color2: 1}
    else:
        if color2 not in markov_data[color1]:
            markov_data[color1][color2] = 1
        else:
            markov_data[color1][color2] += 1


def create_image(width, height):
    # Starting pixel
    # Get random value to select color
    rand = random.random()
    for color2 in markov_data.items():
        for count in color2.items():
            pass
    

if __name__ == '__main__':
    # Get images from input and add to markov data
    for i in range(1, len(sys.argv)):
        # Get argument
        prev = sys.argv[i - 1]
        argv = sys.argv[i]

        if argv == '-s' or argv == '--seed':
            continue
        elif prev == '-s' or prev == '--seed':
            # Set random seed
            random.seed(argv)
            print(argv)
        elif argv == '-h' or argv == '--help':
            # Display usage information
            print('\nUsage:\tmarkov_images.py [-s|--seed SEED] IMAGE_FILES...')
            exit(0)
        else:
            # Process images
            image = Image.open(argv)
            for x in range(1, image.width):
                for y in range(1, image.height):
                    # Add color pair from left to right
                    record_pair(image.getpixel((x, y)),
                                image.getpixel((x - 1, y)))
                    # Add color pair from top to bottom
                    record_pair(image.getpixel((x, y)),
                                image.getpixel((x, y - 1)))
            image.close()
        
        # Create an image
        # TODO
