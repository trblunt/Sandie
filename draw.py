from numpy.core.arrayprint import BoolFormat
import math
from board import Board

from ui.element_picker import ElementPicker

import numpy as np

import pygame


class UserInterface():
    def __init__(self, width: int, height: int, zoom_factor: int, display: pygame.Surface):
        self.game_surface = pygame.Surface(
            (width * zoom_factor, height * zoom_factor))
        self.ui_surface = pygame.Surface((width * zoom_factor, 200))
        self.picker = ElementPicker()
        self.display = display

    def frame(self, board: Board):
        # board.render()
        self.display.blit(self.game_surface, (0, 0))

    def draw_ui(self, board: Board):
        # Render UI
        self.picker.draw(board, self.ui_surface)
        self.display.blit(
            self.ui_surface, (0, board.height * board.zoom_factor))

    def mouse_up(self, board: Board, x: float, y: float) -> None:
        if y >= board.height * board.zoom_factor:
            if self.picker.process_click(board, x, y - (board.height * board.zoom_factor)):
                self.draw_ui(board)
        else:
            pass

    def mouse_down(self, board: Board, x: float, y: float) -> None:
        if y < board.height * board.zoom_factor:
            board.paint(math.floor(y / board.zoom_factor),
                        math.floor(x / board.zoom_factor))

    def mouse_drag(self, board: Board, x: float, y: float) -> None:
        if y < board.height * board.zoom_factor:
            board.paint(math.floor(y / board.zoom_factor),
                        math.floor(x / board.zoom_factor))
