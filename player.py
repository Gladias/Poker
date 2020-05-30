import const


class Player:
    """Represents a poker player.

    Player object contains:
    name, two cards, money, flags, position,
    bet_size - value of player's bet
    card_set - tuple with name and value of player's 5 cards set.
    """

    def __init__(self, name, deck, position, is_AI_controlled=True):
        self.name = name
        self.card_1 = deck.draw()
        self.card_2 = deck.draw()
        self.money = const.STARTING_MONEY
        self.flags = const.PLAYER_FLAGS
        self.flags["is_AI_controlled"] = is_AI_controlled
        self.position = position
        self.bet_size = 0
        self.card_set = ()

    def __str__(self):
        return "{} your cards are {} AND {}".format(self.name, self.card_1, self.card_2)

    def set_cards_position(self, x=const.FIRST_HAND_CARD_X, y=const.HAND_CARDS_Y):
        """Set card position for main player"""
        self.card_1.set_position(x, y)
        self.card_2.set_position(x, y)

    def replace_card(self, card_to_replace, game_deck):
        """Replace player's card with random card from deck."""

        if card_to_replace == self.card_1:
            self.card_1 = game_deck.draw()

        elif card_to_replace == self.card_2:
            self.card_2 = game_deck.draw()

        else:
            print("Card replacement error")

    def is_active(self):
        return self.flags["is_active"]

    def is_player_turn(self):
        return self.flags["is_player_turn"]
