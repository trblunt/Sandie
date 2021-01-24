import sys, pygame, numpy

from board import Board

import draw

pygame.init()

width, height = 60, 40

zoom_factor = 8

screen = pygame.display.set_mode((width * zoom_factor, height * zoom_factor))

board = Board(width, height, zoom_factor=zoom_factor)

draw.initialize(width, height, zoom_factor)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    board.update()
    draw.frame(board, screen)
    pygame.display.flip()