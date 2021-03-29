from numpy import random
from constants import elements as el, cloneables, fire_stages, ElementPair, NeighborhoodTuple

from typing import Union, Callable

import numpy as np

from numba import njit

alchemy_array = np.full((256*256, 5), 255, dtype=np.ubyte) # p, (success1, success2), (failure1, failure2)

# Swap the order of the reactants and results of the reaction.
def converse_reaction(reaction: np.ndarray) -> np.ndarray:
    converse = reaction.copy()
    #Swap reactants
    converse[1] = reaction[2]
    converse[2] = reaction[1]
    #Swap results
    converse[3] = reaction[4]
    converse[4] = reaction[3]
    return converse

def define_reaction(element1: np.ubyte, element2: np.ubyte, result: Union[np.ndarray, ElementPair]) -> None:

    if len(result) == 2:
        # Convert result to ndarray format
        result = np.array([100, result[0], result[1], 0, 0], dtype=np.ubyte)

    alchemy_key = (element1 << 8) + element2
    alchemy_converse_key = (element2 << 8) + element1

    alchemy_array[alchemy_key] = result
    alchemy_array[alchemy_converse_key] = converse_reaction(result)


def random_outcome(outcome_success: ElementPair, outcome_failure: ElementPair, p: float = 0.5) -> np.ndarray:
    byte_probability = np.ubyte(p * 100)
    return np.array([byte_probability, outcome_success[0], outcome_success[1], outcome_failure[0], outcome_failure[1]], dtype=np.ubyte)
@njit
def apply_alchemy(element1: np.ubyte, element2: np.ubyte) -> ElementPair:
    alchemy_key = (element1 << 8) + element2
    result = alchemy_array[alchemy_key]
    success_probability = result[0]
    if success_probability != 255:
        if success_probability == 100:
            return result[1], result[2] # Static reaction
        elif success_probability > np.random.randint(100):
            return result[1], result[2] # Successful reaction
        else:
            return result[3], result[4] # Failed reaction
    else:
        return element1, element2 # No reaction

@njit
def apply_alchemy_to_neighborhood(top_left: np.ubyte, top_right: np.ubyte, bottom_left: np.ubyte, bottom_right: np.ubyte) -> NeighborhoodTuple:
    top_left, bottom_left = apply_alchemy(top_left, bottom_left)
    top_right, bottom_right = apply_alchemy(top_right, bottom_right)
    top_left, top_right = apply_alchemy(top_left, top_right)
    bottom_left, bottom_right = apply_alchemy(bottom_left, bottom_right)

    return top_left, top_right, bottom_left, bottom_right

# Define alchemical reactions


define_reaction(el["water"], el["salt"], (el["salt_water"], el["nothing"]))

define_reaction(el["torch"], el["nothing"], (el["torch"], el["fire_start"]))

define_reaction(el["spout"], el["nothing"], (el["spout"], el["water"]))

define_reaction(el["plant"], el["water"], random_outcome(
    (el["plant"], el["plant"]), (el["plant"], el["water"]), p=0.5))

define_reaction(el["ice"], el["water"], random_outcome(
    (el["ice"], el["ice"]), (el["ice"], el["water"]), p=0.07))

define_reaction(el["ice"], el["salt_water"], random_outcome(
    (el["water"], el["salt_water"]), (el["ice"], el["salt_water"]), p=0.08))

define_reaction(el["ice"], el["salt"], random_outcome(
    (el["salt_water"], el["nothing"]), (el["ice"], el["salt"]), p=0.04))

# Define lava melting reactions

define_reaction(el["lava"], el["stone"], random_outcome(
    (el["lava"], el["lava"]), (el["lava"], el["stone"]), p=0.03))

define_reaction(el["lava"], el["metal"], random_outcome(
    (el["lava"], el["lava"]), (el["lava"], el["metal"]), p=0.01))

define_reaction(el["lava"], el["sand"], random_outcome(
    (el["lava"], el["lava"]), (el["lava"], el["sand"]), p=0.5))

define_reaction(el["lava"], el["salt"], random_outcome(
    (el["lava"], el["lava"]), (el["lava"], el["salt"]), p=0.5))

define_reaction(el["lava"], el["oil"], random_outcome(
    (el["lava"], el["fire_start"]), (el["lava"], el["oil"]), p=0.8))

define_reaction(el["lava"], el["plant"], random_outcome(
    (el["lava"], el["fire_start"]), (el["lava"], el["plant"]), p=0.5))

define_reaction(el["lava"], el["sand"], random_outcome(
    (el["lava"], el["lava"]), (el["lava"], el["sand"]), p=0.5))

define_reaction(el["lava"], el["ice"], (el["stone"], el["water"]))

define_reaction(el["lava"], el["water"], (el["stone"], el["nothing"]))

define_reaction(el["lava"], el["salt_water"], random_outcome(
    (el["stone"], el["salt"]), (el["stone"], el["nothing"]), p=0.2))

# Define acid erosion

define_reaction(el["acid"], el["sand"], random_outcome(
    (el["acid"], el["nothing"]), (el["nothing"], el["nothing"]), p=0.90))

define_reaction(el["acid"], el["stone"], random_outcome(
    (el["acid"], el["nothing"]), (el["nothing"], el["nothing"]), p=0.60))

define_reaction(el["acid"], el["plant"], random_outcome(
    (el["acid"], el["nothing"]), (el["nothing"], el["nothing"]), p=0.80))

define_reaction(el["acid"], el["salt"], random_outcome(
    (el["acid"], el["nothing"]), (el["nothing"], el["nothing"]), p=0.90))

define_reaction(el["acid"], el["metal"], random_outcome(
    (el["acid"], el["nothing"]), (el["nothing"], el["nothing"]), p=0.30))

define_reaction(el["acid"], el["water"], random_outcome(
    (el["water"], el["water"]), (el["acid"], el["water"]), p=0.10))

define_reaction(el["acid"], el["salt_water"], random_outcome(
    (el["water"], el["water"]), (el["acid"], el["salt_water"]), p=0.90))

define_reaction(el["acid"], el["sand"], (el["nothing"], el["nothing"]))

# Implement clone elements

for name, element in el.items():
    if element in cloneables:
        if element not in fire_stages or element == el["fire_start"]:
            clone_name = "clone_" + name
            # Define initial cloning
            define_reaction(el["clone_base"], element, (el[clone_name], element))
            # Define cloning spread
            define_reaction(el["clone_base"], el[clone_name], 
                            (el[clone_name], el[clone_name]))
            # Define actual element cloning
            define_reaction(el[clone_name], el["nothing"], (el[clone_name], element)) 

# Define fire reactions for every stage of fire

for fire_stage in fire_stages:
    define_reaction(el["oil"], fire_stage,
                    (el["fire_start"], el["fire_start"]))

    define_reaction(el["plant"], fire_stage, random_outcome(
        (el["fire_start"], el["sand"]), (el["fire_start"], el["fire_start"]), p=0.2))

    define_reaction(el["ice"], fire_stage, random_outcome(
        (el["water"], fire_stage), (el["ice"], fire_stage), p=0.15))

    clone_name = "clone_fire_start"

    # Define initial cloning
    define_reaction(el["clone_base"], fire_stage, (el[clone_name], el["fire_start"]))


