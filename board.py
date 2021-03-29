import math
from numba import njit, prange
import numpy as np

from constants import elements, colors_array as colors

from process import process_board, generate_margolus_neighborhoods

#from render_simulation import render_game_map

from pygame import Surface, surfarray


@njit(parallel=True)
def process_render_internal(changed_pixels, pixel_array, map, zoom_factor):
    for i in prange(changed_pixels[0].shape[0]):
        y = changed_pixels[0][i]
        x = changed_pixels[1][i]
        pixel_array[x*zoom_factor:(
            x+1)*zoom_factor, y*zoom_factor:(y+1)*zoom_factor] = colors[map[y, x]]

class Board:
    def __init__(self, width: int, height: int, zoom_factor: int, surface: Surface):
        self.width = width
        self.height = height
        self.offset = False
        self.zoom_factor = zoom_factor
        self.surface = surface
        self.tick_delay = 15
        self.pen_size = 6
        self.selected_element = elements["sand"]
        self.array = np.zeros((height, width), dtype=np.ubyte)
        # self.array = np.random.randint(0, 0x0e, (height, width), dtype=np.ubyte)
        self.array[0:3, ::] = elements["wall"]
        self.array[::, 0:3] = elements["wall"]
        self.array[::, width - 3:width] = elements["wall"]
        self.array[height - 3:height, ::] = elements["wall"]
        self.drawn_state = self.array.copy().fill(255)
        self.neighborhoods = generate_margolus_neighborhoods(self.array, False)
        self.neighborhoods_offset = generate_margolus_neighborhoods(self.array, True)

    def set(self, y: int, x: int, value: np.ubyte):
        self.array[y,x] = value

    def paint(self, y: float, x: float):
        radius = self.pen_size
        for j in range(y - (radius - 1), y + radius):
            for i in range(x - math.floor(math.sqrt(radius ** 2 - (j-y) ** 2)), x + math.ceil(math.sqrt(radius ** 2 - (j-y) ** 2))):
                if j >= 0 and j < self.height and i >= 0 and i < self.width:
                    self.set(j, i, self.selected_element)

    def is_border(self, x: int, y: int) -> bool:
        return x == 0 or y == 0 or x == self.width or y == self.height

    def update(self) -> None:
        process_board(self)
        self.offset = not self.offset

    def render(self):
        pixel_array = surfarray.pixels2d(self.surface)
        changed_pixels = np.where(self.array != self.drawn_state) # A copy of the game map where each cell is True if it is different than the drawn state, and false otherwise
        # for y, x in self.changed_pixels:
        # for i in range(changed_pixels[0].shape[0]):
        #     y = changed_pixels[0][i]
        #     x = changed_pixels[1][i]
        #     pixel_array[x*self.zoom_factor:(
        #         x+1)*self.zoom_factor, y*self.zoom_factor:(y+1)*self.zoom_factor] = colors[self.array[y,x]]

        process_render_internal(changed_pixels, pixel_array, self.array, self.zoom_factor)

        self.drawn_state = self.array.copy()

    
    # def render_entire_board(self):
    #     render_game_map(self.array, self.surface, z=self.zoom_factor)

