from constants import densities_array as densities, fluids_array as fluids, NeighborhoodTuple
import numpy as np
from numba import njit

@njit
def apply_gravity_for_neighborhood(top_left: np.ubyte, top_right: np.ubyte, bottom_left: np.ubyte, bottom_right: np.ubyte) -> NeighborhoodTuple:
    if top_left in densities or top_right in densities or bottom_left in densities or bottom_right in densities:

        d_tl = densities[top_left]
        d_tr = densities[top_right]
        d_bl = densities[bottom_left]
        d_br = densities[bottom_right]

        f_tl = fluids[top_left]
        f_tr = fluids[top_right]
        f_bl = fluids[bottom_left]
        f_br = fluids[bottom_right]

        #  Horizontally adjacent fluids should switch positions as long as they are both in the correct position
        #  in their vertical slice with regard to density, in order to simulate fluid flow.

        if f_tl and f_tr and (d_bl == -128 or d_bl >= d_tl) and (d_br == -128 or d_br >= d_tr):
            top_left, top_right = top_right, top_left
            d_tl, d_tr = d_tr, d_tl

        if f_bl and f_br and (d_tl <= d_bl) and (d_tr <= d_br):
            bottom_left, bottom_right = bottom_right, bottom_left
            d_bl, d_br = d_br, d_bl

        #  Elements should fall through fluids if they are more dense than the fluid below them.

        if f_bl and d_tl > d_bl:
            top_left, bottom_left = bottom_left, top_left
            d_tl, d_bl = d_bl, d_tl
            f_tl, f_bl = f_bl, f_tl

        if f_br and d_tr > d_br:
            top_right, bottom_right = bottom_right, top_right
            d_tr, d_br = d_br, d_tr
            f_tr, f_br = f_br, f_tr

        #  Check for unstable piles, which satisfy the following conditions:
        #    - Either the left or the right side of the neighborhood must entirely consist of fluids. (The "fluid" side)
        #    - The top element of the other side must be affected by gravity. (The "pile" side)
        #    - The top element of the pile side must be more dense than both elements of the fluid side.
        #  If these conditions are met, swap the top element of the pile side with the bottom element of the fluid side, collapsing the pile.

        if f_tr and f_br and d_tl > d_tr and d_tl > d_br:
            top_left, bottom_right = bottom_right, top_left
        elif f_tl and f_bl and d_tr > d_tl and d_tr > d_bl:
            top_right, bottom_left = bottom_left, top_right

    return top_left, top_right, bottom_left, bottom_right
