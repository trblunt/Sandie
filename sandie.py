import sys, pygame, numpy

from board import Board

import draw

pygame.init()

width, height = 120, 90

zoom_factor = 4

timer_id = 25

screen = pygame.display.set_mode((width * zoom_factor, height * zoom_factor + 200))

board = Board(width, height, zoom_factor=zoom_factor)

draw.initialize(width, height, zoom_factor)

pygame.time.set_timer(25, board.tick_delay)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == timer_id:
            board.update()
            draw.frame(board, screen)
            pygame.display.flip()
            pygame.event.clear(eventtype = timer_id)

        # draw.draw_ui(board, screen)
