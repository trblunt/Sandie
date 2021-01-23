from constants import densities as d, fluids
import numpy as np


def apply_gravity_for_neighborhood(top_left: np.ubyte, top_right: np.ubyte, bottom_left: np.ubyte, bottom_right: np.ubyte):
    if top_left in d or top_right in d or bottom_left in d or bottom_right in d:

        #  Horizontally adjacent fluids should switch positions as long as they are both in the correct position
        #  in their vertical slice with regard to density, in order to simulate fluid flow.

        if top_left in fluids and top_right in fluids and (bottom_left not in d or d[bottom_left] >= d[top_left]) and (bottom_right not in d or d[bottom_right] >= d[top_right]):
            top_left, top_right = top_right, top_left

        if bottom_left in fluids and bottom_right in fluids and (top_left not in d or d[top_left] <= d[bottom_left]) and (top_right not in d or d[top_right] <= d[bottom_right]):
            bottom_left, bottom_right = bottom_right, bottom_left

        #  Elements should fall through fluids if they are more dense than the fluid below them.

        if bottom_left in fluids and top_left in d and d[top_left] > d[bottom_left]:
            top_left, bottom_left = bottom_left, top_left

        if bottom_right in fluids and top_right in d and d[top_right] > d[bottom_right]:
            top_right, bottom_right = bottom_right, top_right

        #  Check for unstable piles, which satisfy the following conditions:
        #    - Either the left or the right side of the neighborhood must entirely consist of fluids. (The "fluid" side)
        #    - The top element of the other side must be affected by gravity. (The "pile" side)
        #    - The top element of the pile side must not be both resting on a fluid and denser than the bottom element of the pile side.
        #    - The top element of the pile side must be more dense than both elements of the fluid side.
        #  If these conditions are met, swap the top element of the pile side with the bottom element of the fluid side, collapsing the pile.

        if top_right in fluids and bottom_right in fluids and top_left in d and (bottom_left not in fluids or d[top_left] <= d[bottom_left]) and d[top_left] > d[top_right] and d[top_left] > d[bottom_right]:
            top_left, bottom_right = bottom_right, top_left
        elif top_left in fluids and bottom_left in fluids and top_right in d and (bottom_right not in fluids or d[top_right <= d[bottom_right]]) and d[top_right] > d[top_left] and d[top_right] > d[top_left]:
            top_right, bottom_left = bottom_left, top_right

    return (top_left, top_right, bottom_left, bottom_right)
