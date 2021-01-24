import pygame
import board, constants
from ui.element_button import ElementButton

button_width = 40
button_height = 20
button_spacing = 4
ui_height = 200
ui_margin = 15

class ElementPicker:
    
    def create_pickers(self):
        self.pickers: list[ElementButton] = []
        x = y = ui_margin
        for element in constants.labels.keys():
            self.pickers.append(ElementButton((x, y), (button_width, button_height), element))
            y += button_height + button_spacing
            if (y > ui_height - ui_margin - button_height):
                y = ui_margin
                x += button_width + button_spacing

    def __init__(self):
        self.create_pickers()

    def draw(self, board: board.Board, surface: pygame.Surface):
        surface.fill(0x272822)
        for button in self.pickers:
            button.draw(board, surface)
