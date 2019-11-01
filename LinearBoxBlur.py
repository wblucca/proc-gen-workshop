# Author
# William Lucca

import pygame
import random

# Grid variables
MAX_HEIGHT = 100
MIN_HEIGHT = -100
GRID_WIDTH = 100
GRID_HEIGHT = 100
DX = [0, 1, 0, -1]
DY = [-1, 0, 1, 0]
EMPTY_GRID = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]

COLORS = [
    (3, 0),
    (3, 1),
    (2, 1),
    (1, 1),
    (0, 1),
    (0, 2),
    (0, 3)
]

# Display variables
STAGE_WIDTH = 1000
STAGE_HEIGHT = 1000
STAGE = pygame.display.set_mode((STAGE_WIDTH, STAGE_HEIGHT))
LOW_HUE = 0
HIGH_HUE = 240

# Generator variables
PEAK_HEIGHT = 1000
NUM_BLURS = 200
NUM_POINTS = 30


def linear_box_blur(grid):
    """Blurs the input grid by taking the averaging surrounding tiles once
    
    :param grid: A 2-dimensional array with values to blur
    :return: The grid, blurred once
    """
    
    blurred_grid = grid
    
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            # Average value of surrounding tiles
            total = 0
            num_totaled = 0
            
            for k in range(len(DX)):
                # Coords of tile to add into average
                x = i + DX[k]
                y = j + DY[k]
                
                # Only average it if on the grid
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    total += grid[x][y]
                    num_totaled += 1
            
            # Compute average
            blurred_grid[i][j] = total / num_totaled
    
    return blurred_grid


def add_points(grid, num_points):
    """Set num_points random locations to be random elev values"""
    
    for i in range(num_points):
        # Coord for crit point
        rand_x = random.randint(0, GRID_WIDTH - 1)
        rand_y = random.randint(0, GRID_HEIGHT - 1)
        
        # Set value of crit point
        elev = (MAX_HEIGHT - MIN_HEIGHT) * random.random() + MIN_HEIGHT
        grid[rand_x][rand_y] = elev * PEAK_HEIGHT
    
    return grid


def draw_grid(grid):
    """Draw the given grid to the pygame window"""
    
    # Tile size variables
    tile_width = STAGE_WIDTH / GRID_WIDTH
    tile_height = STAGE_HEIGHT / GRID_HEIGHT
    
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            elev = grid[i][j]
            rect_x = i * tile_width
            rect_y = j * tile_height
            pygame.draw.rect(STAGE, get_color(elev),
                             (rect_x, rect_y, tile_width, tile_height))


def get_color(elev):
    """Returns a color to represent the given tile elev"""
    
    # Map from [from_low, from_high] to [0, 1]
    elev_range = MAX_HEIGHT - MIN_HEIGHT
    zero_to_one = 1 - (elev - MIN_HEIGHT) / elev_range
    
    # Set hue based on [0, 1]
    hue_range = HIGH_HUE - LOW_HUE
    elev_hue = zero_to_one * hue_range + LOW_HUE
    if elev_hue < 0:
        elev_hue = 0
    if elev_hue > 255:
        elev_hue = 255
    
    # Get color from hue
    elev_color = pygame.color.Color("red")
    elev_color.hsva = (elev_hue, 100, 100, 100)
    return elev_color


def main():
    pygame.init()
    
    # Make grid with random peaks
    grid = add_points(EMPTY_GRID, NUM_POINTS)
    
    # Begin the blurring
    for i in range(NUM_BLURS):
        # Blur once
        grid = linear_box_blur(grid)
    
        # Draw grid and update
        draw_grid(grid)
        pygame.display.update()

    pygame.time.wait(2000)
    

if __name__ == '__main__':
    main()
