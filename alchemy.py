from constants import elements as el, fire_stages

import random

alchemy_dict = []

# Return the equivalent to a defined result for a reaction with elements in swapped positions.


def converse_reaction(result):
    if callable(result):
        def reversed_reaction():
            # Return reversed result
            return result()[::-1]
        return reversed_reaction
    # Return reversed result
    return result[::-1]


def define_reaction(element1, element2, result):

    alchemy_key = (element1 << 8) + element2
    alchemy_reverse_key = (element2 << 8) + element1

    alchemy_dict[alchemy_key] = result
    alchemy_dict[alchemy_reverse_key] = converse_reaction(result)


def random_outcome(outcome_success, outcome_failure, p=0.5):
    def result():
        if random.random() <= p:
            return outcome_success
        else:
            return outcome_failure
    return result

# Define alchemical reactions


define_reaction(el["water"], el["salt"], (el["salt_water"], el["nothing"]))

define_reaction(el["torch"], el["nothing"], (el["torch"], el["fire_start"]))

define_reaction(el["spout"], el["nothing"], (el["spout"], el["water"]))

define_reaction(el["plant"], el["water"], random_outcome(
    (el["plant"], el["plant"]), (el["plant"], el["water"]), p=0.5))

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
    (el["lava"], el["lava"]), (el["lava"], el["oild"]), p=0.8))

define_reaction(el["lava"], el["plant"], random_outcome(
    (el["lava"], el["lava"]), (el["lava"], el["plant"]), p=0.5))

define_reaction(el["lava"], el["sand"], random_outcome(
    (el["lava"], el["lava"]), (el["lava"], el["sand"]), p=0.5))

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

# Define fire reactions for every stage of fire

for fire_stage in fire_stages:
    define_reaction(el["oil"], fire_stage,
                    (el["fire_start"], el["fire_start"]))
    define_reaction(el["plant"], fire_stage, random_outcome(
        (el["fire_start"], el["sand"]), (el["fire_start"], el["fire_start"]), p=0.2))
