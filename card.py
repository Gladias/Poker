class Card:
    """Represent a single card."""

    def __init__(self, number, symbol):
        self.number = number
        self.symbol = symbol

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
        return self.number == other_card.number and self.symbol == other_card.number

    def __lt__(self, other_card):
        return self.number < other_card.number
