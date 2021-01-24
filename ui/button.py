from abc import ABC, abstractmethod

import board

import pygame


class Button(ABC):

    def __init__(self, position: tuple[float, float], size: tuple[float, float]):
        self.x, self.y = position

        self.width, self.height = size

    @abstractmethod
    def draw(self, board: board.Board, surface: pygame.Surface):
        pass

    def move(self, position: tuple[float, float]):
        self.x, self.y = position

    def resize(self, size: tuple[float, float]):
        self.width, self.height = size

    def in_bounds(self, position: tuple[float, float]) -> bool:
        pos_x, pos_y = position
        return not (self.x > pos_x or self.x + self.width < pos_x or self.y > pos_y or self.y + self.height < pos_y)
