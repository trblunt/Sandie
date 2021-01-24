from pygame import PixelArray, Surface

from constants import colors

import numpy as np

def render_game_map(game_map: np.ndarray, surface: Surface, z: int = 1):
    
    pixel_array = PixelArray(surface)

    # assert(game_map.shape == pixel_array.shape[::-1])

    height, width = game_map.shape

    for y in range(height):
        for x in range(width):
            pixel_array[ x*z:(x+1)*z, y*z:(y+1)*z ] = colors[game_map[y,x]]

    pixel_array.close()
