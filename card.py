import pygame

from const import CARD_WIDTH, CARD_HEIGHT, FIRST_HAND_CARD_X, HAND_CARDS_Y, CARD_DOWNSCALE_HEIGHT, CARD_DOWNSCALE_WIDTH


class Card(pygame.sprite.Sprite):
    """Represent a single card."""
    width = CARD_WIDTH
    height = CARD_HEIGHT

    def __init__(self, number, symbol, image_path):
        super().__init__()

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

    # methods used for card comparison in sorting
    def __eq__(self, other_card):
        return self.number == other_card.number and self.symbol == other_card.symbol

    def __lt__(self, other_card):
        return self.number < other_card.number

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def downscale(self):
        self.rect.width = CARD_DOWNSCALE_WIDTH
        self.rect.height = CARD_DOWNSCALE_HEIGHT
        self.image = pygame.transform.smoothscale(self.image, (self.rect.width, self.rect.height))
        #self.image = pygame.image.load(image_path).convert_alpha()

    def click(self):
        if self.rect.y == HAND_CARDS_Y:
            self.rect.y -= 15
        else:
            self.rect.y += 15

    def is_clicked(self):
        if self.rect.y != HAND_CARDS_Y:
            return True
        else:
            return False
