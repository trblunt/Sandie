from board import Board

import numpy as np

import pygame

game_surface: pygame.Surface = None

ui_surface: pygame.Surface = None

def initialize(width: int, height: int, zoom_factor: int = 1):
    global game_surface, ui_surface
    game_surface = pygame.Surface((width * zoom_factor, height * zoom_factor))
    ui_surface = pygame.Surface((width * zoom_factor, 200))

def frame(board: Board, display: pygame.Surface):
    global game_surface
    board.render(game_surface)
    display.blit(game_surface, (0, 0))

def draw_ui(board: Board, display: pygame.Surface):
    # Render UI
    global ui_surface
    ui_surface.fill(0x272822)
    display.blit(ui_surface, (0, display.get_height() - 200))
