# Author
# William Lucca

import sys
import random
import queue
from markov_data import MarkovData
from PIL import Image

# Command line options
OPTIONS = ['-h', '-W', '-H', '-o', '-s']

# Default settings
DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 300
DEFAULT_OUT_PATH = 'output_image.png'

# Offsets for iterating over neighbors
DX = [0, 1, 0, -1]
DY = [-1, 0, 1, 0]

# Globals
markov_data = MarkovData()
colored = set()


def color_pixel_from_neighbors(xy0, image):
    # Iterate over neighbors and consider colors that exist in markov data
    neighbor_colors = []
    for i in range(len(DX)):
        xy = (xy0[0] + DX[i], xy0[1] + DY[i])
        
        # Add neighbor if in bounds of image
        if in_bounds(xy, image):
            color = image.getpixel(xy)
            if color in markov_data and xy in colored:
                neighbor_colors.append(color)
    
    # No markov neighbors returns random color
    if len(neighbor_colors) == 0:
        return markov_data.random_color()
    
    # Pick random neighbor color to use data from
    return markov_data.next_color(random.choice(neighbor_colors))


def create_image_from_point(x0, y0, width, height):
    # Create image file
    out_image = Image.new('RGBA', (width, height))
    num_pixels = width * height
    
    # Iterate over all pixels
    to_color = queue.PriorityQueue()
    to_color.put((0, (x0, y0)))
    while not to_color.empty():
        # Color next pixel
        xy = to_color.get()[1]
        color = color_pixel_from_neighbors(xy, out_image)
        out_image.putpixel(xy, color)
        
        # Add adjacent pixels to queue/colored set
        for i in range(len(DX)):
            adj_xy = (xy[0] + DX[i], xy[1] + DY[i])
            if in_bounds(adj_xy, out_image) and adj_xy not in colored:
                colored.add(adj_xy)
                to_color.put((random.randrange(0, num_pixels), adj_xy))
    
    return out_image


def in_bounds(xy, image):
    x, y = xy[0], xy[1]
    if 0 <= x < image.width and 0 <= y < image.height:
        return True
    return False


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


def main():
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
                    markov_data.record_pair(image.getpixel((x, y)),
                                            image.getpixel((x - 1, y)))
                    # Add color pair from top to bottom
                    markov_data.record_pair(image.getpixel((x, y)),
                                            image.getpixel((x, y - 1)))
            image.close()
    
    # Create an image
    out = create_image_from_point(width // 2, height // 2, width, height)
    out.save(out_path)
    print('Success! Image "' + out_path + '" has been generated.')
    exit(0)


if __name__ == '__main__':
    main()
