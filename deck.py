from random import shuffle

from card import Card
from const import ASSETS


class Deck:
    """
    Represent a deck of 52 cards.
    Cards are numerated from 2 to 14, where:
    2 to 10 - normal cards
    11 - Jack
    12 - Queen
    13 - King
    14 - Ace
    """
    symbols = ["Hearts", "Spades", "Clubs", "Diamonds"]

    def __init__(self):
        self.deck = []

    def __str__(self):
        deck_str = ""
        for i, card in enumerate(self.deck):
            deck_str += "{}. {}\n".format(i + 1, card)

        return deck_str

    def generate(self):
        next_element = -1

        for i in range(52):
            if i % 13 == 0:
                next_element += 1

            n = i % 13 + 2  # numbers from 2 to 14
            image_path = ASSETS / "cards" / "{}{}.png".format(n, self.symbols[next_element][0])
            self.deck.append(Card(n, self.symbols[next_element], str(image_path)))

    def shuffle(self):
        shuffle(self.deck)

    def push(self, card_to_push):
        self.deck.append(card_to_push)

    def pop(self):
        return self.deck.pop()

    def remove(self, card_to_remove):
        for i, card in enumerate(self.deck):
            if card == card_to_remove:
                self.deck.remove(card)
