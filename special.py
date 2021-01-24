# This file defines special rules to apply to each neighborhood.

from numpy import ubyte

from constants import elements, fire_stages, NeighborhoodTuple


def process_fire(element: ubyte) -> ubyte:
    if element in fire_stages:
        if element == elements["fire_end"]:
            return elements["nothing"]
        return element + 1
    return element


def process_fire_for_neighborhood(top_left: ubyte, top_right: ubyte, bottom_left: ubyte, bottom_right: ubyte) -> NeighborhoodTuple:
    return (process_fire(top_left), process_fire(top_right), process_fire(bottom_left), process_fire(bottom_right))
