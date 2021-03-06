# This file defines special rules to apply to each neighborhood.

from numpy import ubyte

from numba import njit

from numpy.random import random

from constants import elements, NeighborhoodTuple

fire_start = elements["fire_start"]
fire_end = elements["fire_end"]
nothing = elements["nothing"]

@njit
def process_fire(element: ubyte) -> ubyte:
    if element >= fire_start and element <= fire_end and random()<0.2:
        if element == fire_end:
            return nothing
        return element + 1
    return element

@njit
def process_fire_for_neighborhood(top_left: ubyte, top_right: ubyte, bottom_left: ubyte, bottom_right: ubyte) -> NeighborhoodTuple:
    return process_fire(top_left), process_fire(top_right), process_fire(bottom_left), process_fire(bottom_right)
