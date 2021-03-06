from typing import OrderedDict
from numpy import ubyte
import numpy as np
from numba.typed import Dict
from numba.core import types

ElementPair = tuple[ubyte, ubyte]

NeighborhoodTuple = tuple[ubyte, ubyte, ubyte, ubyte]

elements: dict[str, ubyte] = {
    "nothing": 0x00,
    "water": 0x01,
    "oil": 0x02,
    "salt_water": 0x03,
    "sand": 0x04,
    "salt": 0x05,
    "stone": 0x06,
    "wall": 0x07,
    "torch": 0x08,
    "plant": 0x09,
    "spout": 0x0a,
    "metal": 0x0b,
    "lava": 0x0c,
    "acid": 0x0d,
    "ice": 0x0e,

    "clone_base": 0xA0,

    "fire_start": 0xF0,
    "fire_1": 0xF1,
    "fire_2": 0xF2,
    "fire_3": 0xF3,
    "fire_end": 0xF4,
}

# Dictionary of densities
densities: dict[ubyte, int] = {
    elements["fire_start"]: -1,
    elements["fire_1"]: -1,
    elements["fire_2"]: -1,
    elements["fire_3"]: -1,
    elements["fire_end"]: -1,
    elements["nothing"]: 0,
    elements["water"]: 2,
    elements["oil"]: 1,
    elements["salt_water"]: 3,
    elements["lava"]: 4,
    elements["acid"]: 4,
    elements["salt"]: 5,
    elements["sand"]: 5,
    elements["stone"]: 6,
}

# Set of all fluids
fluids: set[ubyte] = {
    elements["fire_start"],
    elements["fire_1"],
    elements["fire_2"],
    elements["fire_3"],
    elements["fire_end"],
    elements["nothing"],
    elements["water"],
    elements["oil"],
    elements["salt_water"],
    elements["lava"],
    elements["acid"],
}

cloneables: set[ubyte] = {
    elements["fire_start"],
    elements["fire_1"],
    elements["fire_2"],
    elements["fire_3"],
    elements["fire_end"],
    elements["water"],
    elements["oil"],
    elements["salt_water"],
    elements["sand"],
    elements["salt"],
    elements["stone"],
    elements["plant"],
    elements["lava"],
    elements["acid"],
    elements["ice"]
}

fire_stages: set[ubyte] = {
    elements["fire_start"],
    elements["fire_1"],
    elements["fire_2"],
    elements["fire_3"],
    elements["fire_end"]
}

colors: dict[ubyte, int] = {
    elements["nothing"]: 0x000000,
    elements["water"]: 0x4040FF,
    elements["oil"]: 0x803020,
    elements["salt_water"]: 0x3399FF,
    elements["sand"]: 0xF2BD6B,
    elements["salt"]: 0xFFFFFF,
    elements["stone"]: 0x808080,
    elements["wall"]: 0x606060,
    elements["torch"]: 0xFFA020,
    elements["spout"]: 0x003333,
    elements["plant"]: 0x00BB00,
    elements["metal"]: 0x404040,
    elements["lava"]: 0xFF6633,
    elements["acid"]: 0xCCFF00,
    elements["ice"]: 0xCAE0E4,
    elements["clone_base"]: 0x907010,

    elements["fire_start"]: 0xFEB815,
    elements["fire_1"]: 0xF47D1F,
    elements["fire_2"]: 0xF47A31,
    elements["fire_3"]: 0xEA5328,
    elements["fire_end"]: 0xCE312C
}

labels: OrderedDict[ubyte, str] = OrderedDict([
    (elements["sand"], "SAND"),
    (elements["salt"], "SALT"),
    (elements["water"], "WATER"),
    (elements["oil"], "OIL"),
    (elements["stone"], "STONE"),
    (elements["metal"], "METAL"),
    (elements["plant"], "PLANT"),
    (elements["fire_start"], "FIRE"),
    (elements["spout"], "SPOUT"),
    (elements["torch"], "TORCH"),
    (elements["lava"], "LAVA"),
    (elements["acid"], "ACID"),
    (elements["ice"], "ICE"),
    (elements["clone_base"], "CLONE")
])

# Implement clone elements

for name in list(elements.keys()):
    element = elements[name]
    if element in cloneables:
        if not element in fire_stages:
            clone_name = "clone_" + name
            elements[clone_name] = 0xA0 + element
            colors[elements[clone_name]] = 0x907010

elements["clone_fire_start"] = 0xA0 + 0x1F
colors[0xA0 + 0x1F] = 0x907010

# Implement Numba typed dict for densities

densities_array = np.full(256, -128, dtype=np.int8)
for key, value in densities.items():
    densities_array[key] = value

fluids_array = np.full(256, False, dtype=np.bool_)
for fluid in fluids:
    fluids_array[fluid] = True

colors_array = np.full(256, 0x000000, dtype=int)
for key, value in colors.items():
    colors_array[key] = value

