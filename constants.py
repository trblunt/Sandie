elements = {
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

	"fire_start": 0xF0,
	"fire_1": 0xF1,
	"fire_2": 0xF2,
	"fire_3": 0xF3,
	"fire_4": 0xF4,
	"fire_end": 0xF5,
}

# Dictionary of densities
densities: { 
	elements["fire_start"]: -1,
	elements["fire_2"]: -1,
	elements["fire_3"]: -1,
	elements["fire_4"]: -1,
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
fluids: {
	elements["fire_start"],
	elements["fire_2"],
	elements["fire_3"],
	elements["fire_4"],
	elements["fire_end"],
	elements["nothing"],
	elements["water"],
	elements["oil"],
	elements["salt_water"],
	elements["lava"],
	elements["acid"],
}

fire_stages: [
	elements["fire_start"],
	elements["fire_2"],
	elements["fire_3"],
	elements["fire_4"],
	elements["fire_end"]
]