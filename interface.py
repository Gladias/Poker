import pygame

from const import ORANGE, BLACK, BORDER_SIZE


class Button:
    def __init__(self, rect, caption, font, bg_color=ORANGE, border_size=BORDER_SIZE, border_color=BLACK):
        self.rect = rect
        self.caption = prepare_message(font, caption)
        self.font = font
        self.text_rect = self.caption.get_rect(center=(self.rect.x + self.rect.width/2, self.rect.y + self.rect.height/2))
        self.bg_color = bg_color
        self.border_rect = (rect.x - border_size, rect.y - border_size, rect.width + 2*border_size, rect.height + 2*border_size)
        self.border_color = border_color


def prepare_interface(font):
    raise_button = Button(pygame.Rect(825, 645, 100, 40), "Raise", font, ORANGE)
    call_button = Button(pygame.Rect(825 + 150, 645, 100, 40), "Call", font, ORANGE)
    fold_button = Button(pygame.Rect(825 + 300, 645, 100, 40), "Fold", font, ORANGE)

    return [raise_button, call_button, fold_button]


def prepare_message(font, text, x=300, y=300):
    return font.render(text, True, (0, 0, 0))


# class Interface:
#    def __init__(self):
#        self.button_list = []
