import numpy as np

from constants import elements

from process import process_game_map

from render_simulation import render_game_map

from pygame import Surface

class Board:
    def __init__(self, width: int, height: int, zoom_factor: int = 1):
        self.width = width
        self.height = height
        self.offset = False
        self.zoom_factor = zoom_factor
        # self.array = np.zeros((height, width), dtype=np.ubyte)
        self.array = np.random.randint(0, 0x0e, (height, width), dtype=np.ubyte)

    def is_border(self, x: int, y: int) -> bool:
        return x == 0 or y == 0 or x == self.width or y == self.height

    def update(self) -> None:
        process_game_map(self.array, self.offset)
        self.offset = not self.offset

    def render(self, surface: Surface):
        render_game_map(self.array, surface, z=self.zoom_factor)