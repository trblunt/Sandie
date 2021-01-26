import sys, pygame, numpy

from board import Board

import draw

pygame.init()

width, height = 160, 120

zoom_factor = 4

timer_id = 25

screen = pygame.display.set_mode((width * zoom_factor, height * zoom_factor + 200))

ui = draw.UserInterface(width, height, zoom_factor, screen)

board = Board(width, height, zoom_factor, ui.game_surface)

board.render()

ui.draw_ui(board)

pygame.time.set_timer(25, board.tick_delay)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == timer_id:
            board.update()
            ui.frame(board)
            pygame.event.clear(eventtype = timer_id)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            ui.mouse_up(board, event.pos[0], event.pos[1])
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ui.mouse_down(board, event.pos[0], event.pos[1])
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            ui.mouse_drag(board, event.pos[0], event.pos[1])

        # draw.draw_ui(board, screen)
    pygame.display.flip()
