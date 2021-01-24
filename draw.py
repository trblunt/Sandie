from board import Board

from ui.element_picker import ElementPicker

import numpy as np

import pygame

class Renderer():
    def __init__(self, width: int, height: int, zoom_factor: int = 1):
        self.game_surface = pygame.Surface((width * zoom_factor, height * zoom_factor))
        self.ui_surface = pygame.Surface((width * zoom_factor, 200))
        self.ui = ElementPicker()

    def frame(self, board: Board, display: pygame.Surface):
        board.render(self.game_surface)
        display.blit(self.game_surface, (0, 0))

    def draw_ui(self, board: Board, display: pygame.Surface):
        # Render UI
        self.ui.draw(board, self.ui_surface)
        display.blit(self.ui_surface, (0, board.height * board.zoom_factor))
