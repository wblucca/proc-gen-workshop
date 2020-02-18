# Author: William Lucca

import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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
        with open(argv) as fp:
            pass
