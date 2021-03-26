from numba import njit, prange
from typing import Callable
import numpy as np
from constants import elements, NeighborhoodTuple

from alchemy import apply_alchemy_to_neighborhood

from gravity import apply_gravity_for_neighborhood

from special import process_fire_for_neighborhood


def generate_margolus_neighborhoods(game_map: np.ndarray, is_offset: bool) -> list[tuple[int, int]]:
    neighborhoods = []
    height, width = game_map.shape

    for y in range(-1 if is_offset else 0, height, 2):
        for x in range(-1 if is_offset else 0, width, 2):
            # Slice 2x2 section of game map (Margolus neighborhood)

            # neighborhood = game_map[max(y, 0):y+2, max(x, 0):x+2]
            # # No need to process empty neighborhoods (where all values are 0)
            # if neighborhood.any():
            #     neighborhoods.append((y, x))
            neighborhoods.append((y, x))

    return np.array(neighborhoods)


# def apply_function_to_neighborhood(func: Callable[[np.ubyte, np.ubyte, np.ubyte, np.ubyte], NeighborhoodTuple], top_left: np.ubyte, top_right: np.ubyte, bottom_left: np.ubyte, bottom_right: np.ubyte) -> NeighborhoodTuple:
#
#    return func(
#        top_left, top_right, bottom_left, bottom_right)

@njit
def process_neighborhood(pos: np.ndarray, map: np.ndarray) -> None:

    top_left = top_right = bottom_left = bottom_right = 0x00

    y, x = pos
    max_y, max_x = map.shape
    if y >= 0 and y < max_y and x >= 0 and x < max_x:
        top_left = map[y, x]

    if y >= 0 and y < max_y and x+1 >= 0 and x+1 < max_x:
        top_right = map[y, x+1]

    if y+1 >= 0 and y+1 < max_y and x >= 0 and x < max_x:
        bottom_left = map[y+1, x]

    if y+1 >= 0 and y+1 < max_y and x+1 >= 0 and x+1 < max_x:
        bottom_right = map[y+1, x+1]

    top_left, top_right, bottom_left, bottom_right = process_fire_for_neighborhood(
        top_left, top_right, bottom_left, bottom_right)
    top_left, top_right, bottom_left, bottom_right = apply_gravity_for_neighborhood(
        top_left, top_right, bottom_left, bottom_right)
    top_left, top_right, bottom_left, bottom_right = apply_alchemy_to_neighborhood(
        top_left, top_right, bottom_left, bottom_right)

    if y >= 0 and y < max_y and x >= 0 and x < max_x:
        #board.set(y, x, top_left)
        map[y, x] = top_left

    if y >= 0 and y < max_y and x+1 >= 0 and x+1 < max_x:
        #board.set(y, x + 1, top_right)
        map[y, x+1] = top_right

    if y+1 >= 0 and y+1 < max_y and x >= 0 and x < max_x:
        #board.set(y + 1, x, bottom_left)
        map[y+1, x] = bottom_left

    if y+1 >= 0 and y+1 < max_y and x+1 >= 0 and x+1 < max_x:
        #board.set(y + 1, x + 1, bottom_right)
        map[y+1, x+1] = bottom_right


@njit(parallel=True)
def process_neighborhoods(map, neighborhoods):
    for i in prange(neighborhoods.shape[0]):
        process_neighborhood(neighborhoods[i], map)

def process_board(board) -> None:
    neighborhoods = board.neighborhoods_offset if board.offset else board.neighborhoods
    process_neighborhoods(board.array, neighborhoods)
