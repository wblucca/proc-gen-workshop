# Author: William Lucca

import sys
import random
from PIL import Image

# Command line options
OPTIONS = ['-h', '-W', '-H', '-o', '-s']

# Default settings
DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 300
DEFAULT_OUT_PATH = 'output_image.png'

# Other globals
num_pairs = 0
first_color_count = dict()
markov_data = dict()


def record_pair(color1, color2):
    """Add a single pixel color pair to the markov pairs data"""
    global num_pairs, markov_data, first_color_count
    
    # Keep track of how many data points have been added
    num_pairs += 1
    
    # Use RGBA mode
    if len(color1) <= 3:
        color1 = (color1[0], color1[1], color1[2], 255)
    if len(color2) <= 3:
        color2 = (color2[0], color2[1], color2[2], 255)
    
    # Add pair to dicts
    if color1 not in markov_data:
        markov_data[color1] = {color2: 1}
        first_color_count[color1] = 1
    else:
        first_color_count[color1] += 1
        if color2 not in markov_data[color1]:
            markov_data[color1][color2] = 1
        else:
            markov_data[color1][color2] += 1


def pick_random_color():
    # Get random value to select color
    rand = random.random()
    cumulative_prob = 0
    for color2_map in markov_data.values():
        for key in color2_map:
            cumulative_prob += color2_map[key] / num_pairs
            if rand < cumulative_prob:
                return key


def pick_next_color(prev_color):
    # Return random color if no markov data for this prev_color
    if prev_color not in markov_data:
        return pick_random_color()
    
    # Get random value to select color
    rand = random.random()
    cumulative_prob = 0
    for color in markov_data[prev_color]:
        prob = markov_data[prev_color][color] / first_color_count[prev_color]
        cumulative_prob += prob
        if rand < cumulative_prob:
            return color
    
    # No choices from prev_color, return random
    return pick_random_color()


def select_random_color(color1, color2):
    if random.random() < 0.5:
        return color1
    return color2


def create_image(width, height):
    # Create image file
    out_image = Image.new('RGBA', (width, height))
    
    # Calculate pixel colors
    for w in range(width):
        for h in range(height):
            if (w, h) == (0, 0):
                # Starting pixel
                out_image.putpixel((0, 0), pick_random_color())
            elif h == 0:
                # Get next pixel from left pixel
                color = pick_next_color(out_image.getpixel((w - 1, h)))
                out_image.putpixel((w, 0), color)
            elif w == 0:
                # Get next pixel from top pixel
                color = pick_next_color(out_image.getpixel((w, h - 1)))
                out_image.putpixel((w, h), color)
            else:
                # Get next pixel from either top or left (50/50)
                if random.random() < 0.5:
                    color = pick_next_color(out_image.getpixel((w - 1, h)))
                else:
                    color = pick_next_color(out_image.getpixel((w, h - 1)))
                out_image.putpixel((w, h), color)
    
    return out_image


def printhelp():
    # Print basic usage
    print('\nUsage:  markov_images.py',
          '[-h] [-W WIDTH] [-H HEIGHT] [-o PATH] [-s SEED]\n')
    
    # Print description of each option
    print('[' + OPTIONS[0] + ']\t\tDisplay this help message')
    print('[' + OPTIONS[1] + ' WIDTH]\tSet the width of the output image '
                             '(default 300px)')
    print('[' + OPTIONS[2] + ' HEIGHT]\tSet the height of the output image '
                             '(default 300px)')
    print('[' + OPTIONS[3] + ' PATH]\tSet the filepath for the output image '
                             '(default "output_image.png")')
    print('[' + OPTIONS[4] + ' SEED]\tSet the seed for the random generator '
                             '(uses random seed by default)')
    

if __name__ == '__main__':
    # Initialize variables for image creation
    img_width = DEFAULT_WIDTH
    img_height = DEFAULT_HEIGHT
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
            img_width = int(argv)
        elif prev == '-H':
            # Set output image height
            img_height = int(argv)
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
    out = create_image(img_width, img_height)
    out.save(out_path)
    print('Success! Image "' + out_path + '" has been generated.')
    exit(0)
