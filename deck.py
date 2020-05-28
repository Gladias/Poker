import random

import card
import const


class Deck:
    """Represents a deck of 52 cards.

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
        for i, card_object in enumerate(self.deck):
            deck_str += "{}. {}\n".format(i + 1, card_object)

        return deck_str

    def generate(self):
        """Generates sorted deck."""
        next_element = -1

        for i in range(52):
            if i % 13 == 0:
                next_element += 1

            number = i % 13 + 2  # numbers from 2 to 14
            image_path = const.ASSETS / "cards" / "{}{}.png".format(number, self.symbols[next_element][0])
            self.deck.append(card.Card(number, self.symbols[next_element], str(image_path)))

    def shuffle(self):
        """Shuffles whole deck."""
        random.shuffle(self.deck)

    def push(self, card_to_push):
        """Puts card at the end of deck."""
        self.deck.append(card_to_push)

    def draw(self):
        """Draws one card from deck."""
        return self.deck.pop()

    def remove(self, card_to_remove):
        """Removes card from deck."""
        self.deck.remove(card_to_remove)
