import pygame


class Button:
    def __init__(self, rect, caption, font, bg_color=(212, 208, 200)):
        self.rect = rect
        self.caption = font.render(caption, True, (0, 0, 0))
        self.font = font
        self.bg_color = bg_color


# class Interface:
#    def __init__(self):
#        self.button_list = []
