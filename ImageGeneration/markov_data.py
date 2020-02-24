# Author
# William Lucca

import random


class MarkovData:
    
    def __init__(self):
        self.num_pairs = 0
        self.first_color_count = dict()
        self.data = dict()

    def record_pair(self, color1, color2):
        """Add a single pixel color pair to the markov pairs data"""
    
        # Keep track of how many data points have been added
        self.num_pairs += 1
    
        # Use RGBA mode
        color1 = getRGBA(color1)
        color2 = getRGBA(color2)
    
        # Add pair to dicts
        if color1 not in self.data:
            self.data[color1] = {color2: 1}
            self.first_color_count[color1] = 1
        else:
            self.first_color_count[color1] += 1
            if color2 not in self.data[color1]:
                self.data[color1][color2] = 1
            else:
                self.data[color1][color2] += 1

    def random_color(self):
        # Get random value to select color
        rand = random.random()
        cumulative_prob = 0
        for color2_map in self.data.values():
            for key in color2_map:
                cumulative_prob += color2_map[key] / self.num_pairs
                if rand < cumulative_prob:
                    return key

    def next_color(self, prev_color):
        # Return random color if no markov data for this prev_color
        if prev_color not in self.data:
            return self.random_color()
    
        # Get random value to select color
        rand = random.random()
        cumulative_prob = 0
        for color in self.data[prev_color]:
            prob = self.data[prev_color][color] / self.first_color_count[
                prev_color]
            cumulative_prob += prob
            if rand < cumulative_prob:
                return color
    
        # No choices from prev_color, return random
        return self.random_color()
    
    def __contains__(self, color):
        return color in self.data


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


def get_color_int(rgba):
    num = 0
    for channel in rgba:
        # Add channel value to appropriate bits
        num <<= 8
        num += channel
    
    return num


def get_color_tuple(num):
    rgba = [0 for i in range(4)]
    for i in range(3, -1, -1):
        # Add channel value to appropriate bits
        rgba[i] = num % 256
        num >>= 8
    
    return tuple(rgba)
