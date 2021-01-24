from ui.button import Button

import constants, board

import pygame, numpy as np

inactive_color = 0x464646

active_color = 0xB8B8B8

font_size = 12

class ElementButton(Button):

    def __init__(self, position: tuple[float, float], size: tuple[float, float], element: np.ubyte):
        super().__init__(position, size)
        self.element = element
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)

    def draw(self, board: board.Board, surface: pygame.Surface):
        label = constants.labels[self.element]
        color = active_color if board.selected_element == self.element else inactive_color

        pygame.draw.rect(surface, color, pygame.Rect(self.x, self.y, self.width, self.height))

        center_x, center_y = self.x + (self.width / 2), self.y + (self.height / 2)

        for x in [center_x - 1, center_x + 1]:
            for y in [center_y - 1, center_y + 1]:
                outline_text = self.font.render(label, True, 0x00000000)
                outline_textbox = outline_text.get_rect()
                outline_textbox.center = (x, y)
                surface.blit(outline_text, outline_textbox)

        text = self.font.render(label, True, constants.colors[self.element] << 8)
        textbox = text.get_rect()
        textbox.center = (center_x, center_y)
        surface.blit(text, textbox)
