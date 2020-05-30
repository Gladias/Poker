import pygame

import const


class Card:
    """Represents a single card.

    Card object contains:
    number, symbol, image, and rect - coordinates used for click detection and positioning.
    """
    width = const.CARD_WIDTH
    height = const.CARD_HEIGHT

    def __init__(self, number, symbol, image_path):
        self.number = number
        self.symbol = symbol
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

    def __str__(self):
        if self.number == 11:
            card = "{} of {}".format("Jack", self.symbol)
        elif self.number == 12:
            card = "{} of {}".format("Queen", self.symbol)
        elif self.number == 13:
            card = "{} of {}".format("King", self.symbol)
        elif self.number == 14:
            card = "{} of {}".format("Ace", self.symbol)
        else:
            card = "{} of {}".format(self.number, self.symbol)

        return card

    def __eq__(self, other_card):
        return self.number == other_card.number and self.symbol == other_card.symbol

    def __lt__(self, other_card):
        return self.number < other_card.number

    def set_position(self, x, y):
        """Sets card top left corner position to x, y coordinates."""
        self.rect.x = x
        self.rect.y = y

    def downscale(self):
        """Sets card's new width and height and downscales card's image."""
        self.rect.width = const.CARD_DOWNSCALE_WIDTH
        self.rect.height = const.CARD_DOWNSCALE_HEIGHT
        self.image = pygame.transform.smoothscale(self.image, (self.rect.width, self.rect.height))

    def click(self):
        """Moves card up or down by 15 pixels."""
        if self.rect.y == const.HAND_CARDS_Y:
            self.rect.y -= 15
        else:
            self.rect.y += 15

    def is_clicked(self):
        """Returns true if card position is different from standard."""
        return self.rect.y != const.HAND_CARDS_Y
