from typing import Callable
import numpy as np
from constants import elements, ElementPair


def generate_margolus_neighborhoods(game_map: np.ndarray, is_offset: bool) -> list[np.ndarray]:
    neighborhoods = []
    height, width = game_map.shape

    for y in range(1 if is_offset else 0, height, 2):
        for x in range(1 if is_offset else 0, width, 2):
            # Slice 2x2 section of game map (Margolus neighborhood)
            neighborhood = game_map[y:y+2, x:x+2]
            # No need to process empty neighborhoods (where all values are 0)
            if neighborhood.any():
                neighborhoods.append(neighborhood)

    return neighborhoods


def apply_function_to_neighborhood(func: Callable[[np.ubyte, np.ubyte], ElementPair], neighborhood: np.ndarray) -> None:

    def get_element(y: int, x: int) -> np.ubyte:
        if neighborhood.shape < (y+1, x+1):
            return elements["nothing"]
        return neighborhood[y, x]

    def set_element(y: int, x: int, value: np.ubyte) -> None:
        if neighborhood.shape >= (y+1, x+1):
            neighborhood[y][x] = value

    top_left = get_element(0, 0)
    top_right = get_element(0, 1)
    bottom_left = get_element(1, 0)
    bottom_right = get_element(1, 1)

    top_left, bottom_left = func(top_left, bottom_left)
    top_right, bottom_right = func(top_right, bottom_right)
    top_left, top_right = func(top_left, top_right)
    bottom_left, bottom_right = func(bottom_left, bottom_right)

    set_element(0, 0, top_left)
    set_element(0, 1, top_right)
    set_element(1, 0, bottom_left)
    set_element(1, 1, bottom_right)
