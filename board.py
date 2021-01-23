import numpy as np

class Board:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.array = np.fromfunction(lambda i, j: self.is_border(i, j), [width, height], dtype=np.ubyte)

	def is_border(self, x, y):
		return x==0 or y==0 or x==self.width or y==self.height