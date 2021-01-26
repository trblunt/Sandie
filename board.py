import math
import numpy as np

from constants import elements, colors

from process import process_board

from render_simulation import render_game_map

from pygame import Surface, surfarray

class Board:
    def __init__(self, width: int, height: int, zoom_factor: int, surface: Surface):
        self.width = width
        self.height = height
        self.offset = False
        self.zoom_factor = zoom_factor
        self.surface = surface
        self.tick_delay = 100
        self.pen_size = 6
        self.selected_element = elements["sand"]
        self.array = np.zeros((height, width), dtype=np.ubyte)
        # self.array = np.random.randint(0, 0x0e, (height, width), dtype=np.ubyte)
        self.array[0:3, ::] = elements["wall"]
        self.array[::, 0:3] = elements["wall"]
        self.array[::, width - 3:width] = elements["wall"]
        self.array[height - 3:height, ::] = elements["wall"]

    def set(self, y: int, x: int, value: np.ubyte):
        if self.array[y,x] != value:
            self.array[y,x] = value
            pixel_array = surfarray.pixels2d(self.surface)
            pixel_array[x*self.zoom_factor:(x+1)*self.zoom_factor, y*self.zoom_factor:(y+1)*self.zoom_factor] = colors[value]
            #pixel_array.close()

    def paint(self, y: float, x: float):
        radius = self.pen_size
        for j in range(y - (radius - 1), y + radius):
            for i in range(x - math.floor(math.sqrt(radius ** 2 - (j-y) ** 2)), x + math.ceil(math.sqrt(radius ** 2 - (j-y) ** 2))):
                if j >= 0 and j < self.height and i >= 0 and i < self.width:
                    self.set(j, i, self.selected_element)

    def is_border(self, x: int, y: int) -> bool:
        return x == 0 or y == 0 or x == self.width or y == self.height

    def update(self) -> None:
        process_board(self, self.offset)
        self.offset = not self.offset

    def render(self):
        render_game_map(self.array, self.surface, z=self.zoom_factor)

