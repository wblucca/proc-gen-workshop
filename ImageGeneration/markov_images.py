# Author: William Lucca

import sys
import random
import queue
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

# Offsets for iterating over neighbors
DX = [0, 1, 0, -1]
DY = [-1, 0, 1, 0]


def record_pair(color1, color2):
    """Add a single pixel color pair to the markov pairs data"""
    global num_pairs, markov_data, first_color_count
    
    # Keep track of how many data points have been added
    num_pairs += 1
    
    # Use RGBA mode
    color1 = getRGBA(color1)
    color2 = getRGBA(color2)
    
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


def create_image_from_corner(width, height):
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


def color_point_from_neighbors(xy0, image):
    # Iterate over neighbors and consider colors that exist in markov data
    neighbor_colors = []
    for i in range(len(DX)):
        xy = (xy0[0] + DX[i], xy0[1] + DY[i])
        
        # Add neighbor if in bounds of image
        if in_bounds(xy, image):
            color = image.getpixel(xy)
            if color in markov_data:
                neighbor_colors.append(color)
    
    # No markov neighbors returns random color
    if len(neighbor_colors) == 0:
        return pick_random_color()
    
    # Pick random neighbor color to use data from
    return pick_next_color(random.choice(neighbor_colors))


def create_image_from_point(x0, y0, width, height):
    # Create image file
    out_image = Image.new('RGBA', (width, height))
    num_pixels = width * height
    
    # Iterate over all pixels
    to_color = queue.PriorityQueue()
    colored = set()
    to_color.put((0, (x0, y0)))
    while not to_color.empty():
        # Color next pixel
        xy = to_color.get()[1]
        color = color_point_from_neighbors(xy, out_image)
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


def getRGBA(color):
    num_channels = len(color)
    colorRGBA = []
    for i in range(4):
        if i < num_channels:
            colorRGBA.append(color[i])
        else:
            colorRGBA.append(255)
    
    # Convert to tuple
    return tuple(colorRGBA)


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
                    record_pair(image.getpixel((x, y)),
                                image.getpixel((x - 1, y)))
                    # Add color pair from top to bottom
                    record_pair(image.getpixel((x, y)),
                                image.getpixel((x, y - 1)))
            image.close()
    
    # Create an image
    out = create_image_from_point(width // 2, height // 2, width, height)
    out.save(out_path)
    print('Success! Image "' + out_path + '" has been generated.')
    exit(0)


if __name__ == '__main__':
    main()
