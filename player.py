from timeit import default_timer
from copy import deepcopy

from const import sets_and_values, FIRST_HAND_CARD_X, HAND_CARDS_Y, SECOND_HAND_CARD_X
from deck import Deck

from hand_evaluation import hands_combinations


class Player:
    """Represent a hand of 2 cards"""

    def __init__(self, name, deck, money, AI, position, image_path=None):
        self.name = name
        self.card_1 = deck.draw()
        self.card_2 = deck.draw()
        self.money = money
        self.is_AI_controlled = AI
        self.position = position
        self.is_playing = True
        self.is_player_turn = False
        self.bet_size = 0
        # ToDo: self.image_path = image_path
        self.card_set = ()  # tuple with name and value of players 5 card set  # TODO: REMOVE PROBABLY

    def __str__(self):
        #print_card()
        return "{} your cards are {} AND {}, your bankroll is {}$".format(self.name, self.card_1, self.card_2, self.money)

    #def print_player(self):
    #    print_card(player.card_1.image_path, FIRST_HAND_CARD_X, HAND_CARDS_Y)
    #    print_card(player.card_2.image_path, SECOND_HAND_CARD_X, HAND_CARDS_Y)

    def adjust_cards_position(self):
        """Set right card position for main player"""
        if not self.is_AI_controlled:
            self.card_1.set_position(FIRST_HAND_CARD_X, HAND_CARDS_Y)
            self.card_2.set_position(SECOND_HAND_CARD_X, HAND_CARDS_Y)

    def select_cards(self):
        """Move players card up or down to indicate selection in exchange phase"""
        pass
        #if self.card_1.x == FIRST_HAND_CARD_X:
        #    self.card_1.x += 10


    def exchange(self, card, deck):
        """Exchange function for not AI controlled players"""

        if card == self.card_1:
            self.card_1 = deck.draw()

        elif card == self.card_2:
            self.card_2 = deck.draw()

        else:
            print("Exchange error")

    # TODO: move to game
    def exchange_simulation(self, deck):
        """Decide which cards to exchange in AI controlled players"""
        t_start = default_timer()
        N = 2000
        # Number of simulations per case, there are 4 cases because player can do 1 action from 4 available:
        # 1. Don't exchange cards
        # 2. Replace first card
        # 3. Replace second card
        # 4. Replace both cards

        simulation_deck = Deck()
        simulation_deck.generate()

        # remove 2 cards in player's hand from simulation deck
        simulation_deck.remove(self.card_1)
        simulation_deck.remove(self.card_2)

        card_1 = self.card_1
        card_2 = self.card_2

        sets_counter = {
            "ROYAL FLUSH":     0,
            "STRAIGHT FLUSH":  0,
            "FOUR OF A KIND":  0,
            "FULL HOUSE":      0,
            "FLUSH":           0,
            "STRAIGHT":        0,
            "THREE OF A KIND": 0,
            "TWO PAIRS":       0,
            "ONE PAIR":        0,
            "HIGH CARD":       0
        }

        arr = [deepcopy(sets_counter) for _ in range(4)]

        print("{} makes simulation...".format(self.name))

        # 1. Don't exchange cards

        for _ in range(N):
            simulation_deck.shuffle()
            table_cards = [simulation_deck.deck[i] for i in range(5)]

            hands_combinations(table_cards, self)
            arr[0][self.card_set[0]] += 1

        # 2. Exchange first card

        self.card_1 = simulation_deck.draw()

        for _ in range(N):
            simulation_deck.shuffle()
            table_cards = [simulation_deck.deck[i] for i in range(5)]

            hands_combinations(table_cards, self)
            arr[1][self.card_set[0]] += 1

        simulation_deck.push(self.card_1)
        self.card_1 = card_1

        # 3. Exchange second card

        self.card_2 = simulation_deck.draw()

        for _ in range(N):
            simulation_deck.shuffle()
            table_cards = [simulation_deck.deck[i] for i in range(5)]

            hands_combinations(table_cards, self)
            arr[2][self.card_set[0]] += 1

        simulation_deck.push(self.card_2)
        self.card_2 = card_2

        # 4. Exchange both cards

        self.card_1 = simulation_deck.draw()
        self.card_2 = simulation_deck.draw()

        for _ in range(N):
            simulation_deck.shuffle()
            table_cards = [simulation_deck.deck[i] for i in range(5)]

            hands_combinations(table_cards, self)
            arr[3][self.card_set[0]] += 1

        simulation_deck.push(self.card_1)
        simulation_deck.push(self.card_2)
        self.card_1 = card_1
        self.card_2 = card_2

        # Multiply set_counter by value of particular set, and add it to row values

        rows_values = [0, 0, 0, 0]

        for i in range(len(arr)):  # 4
            for j in range(len(sets_counter)):  # 9
                arr[i][sets_and_values[j][0]] *= sets_and_values[j][1]
                rows_values[i] += arr[i][sets_and_values[j][0]]

        best_variant = rows_values.index(max(rows_values))

        if best_variant == 0:
            print("{} doesn't exchange any cards.".format(self.name))
        elif best_variant == 1:
            print("{} exchanges first card.".format(self.name))
            self.card_1 = deck.draw()
        elif best_variant == 2:
            print("{} exchanges second card.".format(self.name))
            self.card_2 = deck.draw()
        else:
            print("{} exchanges both cards.".format(self.name))
            self.card_1 = deck.draw()
            self.card_2 = deck.draw()

        t_end = default_timer()
        print("|{} made a decision in {:.2f}s|".format(self.name, t_end-t_start))
