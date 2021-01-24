from board import Board

import numpy as np

import pygame

game_surface: pygame.Surface = None

def initialize(width: int, height: int, zoom_factor: int = 1):
    global game_surface
    game_surface = pygame.Surface((width * zoom_factor, height * zoom_factor))

def frame(board: Board, display: pygame.Surface):
    global game_surface
    board.render(game_surface)
    display.blit(game_surface, (0, 0))
