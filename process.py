from typing import Callable
import numpy as np
from constants import elements, NeighborhoodTuple

from alchemy import apply_alchemy_to_neighborhood

from gravity import apply_gravity_for_neighborhood

from special import process_fire_for_neighborhood

# TODO: Fix issue where some cells are not represented in offset Margolus neighborhoods.

def generate_margolus_neighborhoods(game_map: np.ndarray, is_offset: bool) -> list[tuple[np.ndarray, int, int]]:
    neighborhoods = []
    height, width = game_map.shape

    for y in range(1 if is_offset else 0, height, 2):
        for x in range(1 if is_offset else 0, width, 2):
            # Slice 2x2 section of game map (Margolus neighborhood)
            neighborhood = game_map[y:y+2, x:x+2]
            # No need to process empty neighborhoods (where all values are 0)
            if neighborhood.any():
                neighborhoods.append((neighborhood, y, x))

    return neighborhoods


#def apply_function_to_neighborhood(func: Callable[[np.ubyte, np.ubyte, np.ubyte, np.ubyte], NeighborhoodTuple], top_left: np.ubyte, top_right: np.ubyte, bottom_left: np.ubyte, bottom_right: np.ubyte) -> NeighborhoodTuple:
#
#    return func(
#        top_left, top_right, bottom_left, bottom_right)


def process_neighborhood(neighborhood: np.ndarray, pos: tuple[int, int], board) -> None:

    max_y, max_x = neighborhood.shape

    top_left = top_right = bottom_left = bottom_right = 0x00

    if max_y == 2 and max_x == 2:
        top_left = neighborhood[0, 0]
        top_right = neighborhood[0, 1]
        bottom_left = neighborhood[1, 0]
        bottom_right = neighborhood[1, 1]
    elif max_y == 2 and max_x == 1:
        top_left = neighborhood[0, 0]
        bottom_left = neighborhood[1, 0]
    elif max_y == 1 and max_x == 2:
        top_left = neighborhood[0, 0]
        top_right = neighborhood[0, 1]
    elif max_y == 1 and max_x == 1:
        top_left = neighborhood[0, 0]

    top_left, top_right, bottom_left, bottom_right = process_fire_for_neighborhood(top_left, top_right, bottom_left, bottom_right)
    top_left, top_right, bottom_left, bottom_right = apply_gravity_for_neighborhood(top_left, top_right, bottom_left, bottom_right)
    top_left, top_right, bottom_left, bottom_right = apply_alchemy_to_neighborhood(top_left, top_right, bottom_left, bottom_right)

    if max_y == 2 and max_x == 2:
        board.set(pos[0], pos[1], top_left)
        board.set(pos[0], pos[1] + 1, top_right)
        board.set(pos[0] + 1, pos[1], bottom_left)
        board.set(pos[0] + 1, pos[1] + 1, bottom_right)
    elif max_y == 2 and max_x == 1:
        board.set(pos[0], pos[1], top_left)
        board.set(pos[0] + 1, pos[1], bottom_left)
    elif max_y == 1 and max_x == 2:
        board.set(pos[0], pos[1], top_left)
        board.set(pos[0], pos[1] + 1, top_right)
    elif max_y == 1 and max_x == 1:
        board.set(pos[0], pos[1], top_left)


def process_board(board, is_offset: bool) -> None:
    for neighborhood, y, x in generate_margolus_neighborhoods(board.array, is_offset):
        process_neighborhood(neighborhood, (y, x), board)
