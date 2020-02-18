# Author: William Lucca

import sys
import random
from PIL import Image

# Command line options
OPTIONS = ['-h', '-W', '-H', '-o', '-s']

# Default settings
DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 300
DEFAULT_OUT_PATH = 'markov_image.png'

# Other globals
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


def printhelp():
    # Print basic usage
    print('\nUsage:  markov_images.py',
          '[-h] [-W WIDTH] [-H HEIGHT] [-o PATH] [-s SEED]\n')
    
    # Print description of each option
    print('[' + OPTIONS[0] + ']\t\tDisplay this help message')
    print('[' + OPTIONS[1] + ' WIDTH]\tSet the width of the output image')
    print('[' + OPTIONS[2] + ' HEIGHT]\tSet the height of the output image')
    print('[' + OPTIONS[3] + ' PATH]\tSet the filepath for the output image')
    print('[' + OPTIONS[4] + ' SEED]\tSet the seed for the random generator')
    

if __name__ == '__main__':
    # Initialize variables for image creation
    width = DEFAULT_WIDTH
    height = DEFAULT_HEIGHT
    out_path = DEFAULT_OUT_PATH
    
    # Iterate over command line arguments
    argv = ''
    for i in range(1, len(sys.argv)):
        # Get argument and potential option flag
        prev = argv
        argv = sys.argv[i]

        if argv == '-h':
            # Display usage information
            printhelp()
            exit(0)
        elif argv in OPTIONS:
            continue
        elif prev == '-s':
            # Set random seed
            random.seed(argv)
        elif prev == '-W':
            # Set output image width
            width = int(argv)
        elif prev == '-H':
            # Set output image height
            height = int(argv)
        elif prev == '-o':
            # Set output image filepath
            out_path = argv
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
