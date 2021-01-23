import numpy as np


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.array = np.fromfunction(lambda j, i: self.is_border(i, j), [
                                     height, width], dtype=np.ubyte)

    def is_border(self, x: int, y: int) -> bool:
        return x == 0 or y == 0 or x == self.width or y == self.height
