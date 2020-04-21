# Poker
# 2 cards in hand, possibility to exchange cards at the beginning of a game.
import random
from itertools import combinations
from copy import deepcopy
from timeit import default_timer
# import pygame
import sys

sets_and_values = [
    ("ROYAL FLUSH",     10),
    ("STRAIGHT FLUSH",  9),
    ("FOUR OF A KIND",  8),
    ("FULL HOUSE",      7),
    ("FLUSH",           6),
    ("STRAIGHT",        5),
    ("THREE OF A KIND", 4),
    ("TWO PAIRS",       3),
    ("ONE PAIR",        2),
    ("HIGH CARD",       1)
]


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

            self.deck.append(Card(i % 13 + 2, self.symbols[next_element]))  # numbers from 2 to 14

    def shuffle(self):
        random.shuffle(self.deck)

    def push(self, card_to_push):
        self.deck.append(card_to_push)

    def pop(self):
        return self.deck.pop()

    def remove(self, card_to_remove):
        for i, card in enumerate(self.deck):
            if card == card_to_remove:
                self.deck.remove(card)


class Player:
    """Represent a hand of 2 cards"""

    def __init__(self, name, deck, AI):
        self.name = name
        self.card_1 = deck.pop()
        self.card_2 = deck.pop()
        self.is_AI_controlled = AI
        self.card_set = ()  # tuple with name and value of players 5 card set

    def __str__(self):
        return "{} has: {} AND {}\n".format(self.name, self.card_1, self.card_2)

    def exchange(self, deck):
        """Exchange function for not AI controlled players"""

        print("{} how many cards would you like to exchange: ".format(self.name))
        number = int(input())

        if number == 1:
            choice = int(input("Card 1 or Card 2: \n"))

            if choice == 1:
                self.card_1 = deck.pop()
            elif choice == 2:
                self.card_2 = deck.pop()
            else:
                print("No cards have been exchanged.")

            print("One card has been exchanged.")

        elif number == 2:
            print("Both cards have been exchanged.")
            self.card_1 = deck.pop()
            self.card_2 = deck.pop()

        else:
            print("No cards have been exchanged.")

    def exchange_simulation(self, deck):
        """Decide which cards to exchange in AI controlled players"""
        t_start = default_timer()
        N = 5000
        # Number of simulations per case, there are 4 cases because player can do 1 action from 4 available:
        # 1. Don't exchange cards
        # 2. Replace first card
        # 3. Replace second card
        # 4. Replace both cards

        simulation_deck = Deck()
        simulation_deck.generate()

        # remove 2 cards in players hand from simulation deck
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

        self.card_1 = simulation_deck.pop()

        for _ in range(N):
            simulation_deck.shuffle()
            table_cards = [simulation_deck.deck[i] for i in range(5)]

            hands_combinations(table_cards, self)
            arr[1][self.card_set[0]] += 1

        simulation_deck.push(self.card_1)
        self.card_1 = card_1

        # 3. Exchange second card

        self.card_2 = simulation_deck.pop()

        for _ in range(N):
            simulation_deck.shuffle()
            table_cards = [simulation_deck.deck[i] for i in range(5)]

            hands_combinations(table_cards, self)
            arr[2][self.card_set[0]] += 1

        simulation_deck.push(self.card_2)
        self.card_2 = card_2

        # 4. Exchange both cards

        self.card_1 = simulation_deck.pop()
        self.card_2 = simulation_deck.pop()

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
            self.card_1 = deck.pop()
        elif best_variant == 2:
            print("{} exchanges second card.".format(self.name))
            self.card_2 = deck.pop()
        else:
            print("{} exchanges both cards.".format(self.name))
            self.card_1 = deck.pop()
            self.card_2 = deck.pop()

        t_end = default_timer()
        print("|{} made a decision in {:.2f}s|".format(self.name, t_end-t_start))


def hand_ranking(combination: []):
    """Return tuple (name,value) of combination of 5 cards passed as list"""

    combination.sort()

    flush = True
    straight = True
    pairs = []

    for i in range(len(combination)):
        for j in range(i + 1, len(combination)):

            if combination[i].symbol != combination[j].symbol:
                flush = False

            # cards are sorted, for straight check if next card - 1 is equal to previous one
            if combination[i].number - i != combination[j].number - j:
                straight = False

            if combination[i].number == combination[j].number:
                pairs.append(combination[i].number)

    if flush and straight and combination[0].number == 10:
        return sets_and_values[0]

    elif flush and straight:
        return sets_and_values[1]

    elif len(pairs) > 4:
        return sets_and_values[2]

    elif len(pairs) == 4:
        return sets_and_values[3]

    elif flush:
        return sets_and_values[4]

    elif straight:
        return sets_and_values[5]

    elif len(pairs) == 3:
        return sets_and_values[6]

    elif len(pairs) == 2:
        return sets_and_values[7]

    elif len(pairs) == 1:
        return sets_and_values[8]

    else:
        return sets_and_values[9]


def hands_combinations(table, player):
    """
    Check all 5 elements combinations of players cards and cards on table
    and set each players card_set tuple to the best combination they have.
    """

    cards = []
    cards.extend(table)
    cards.append(player.card_1)
    cards.append(player.card_2)

    comb_list = list(combinations(cards, 5))

    best_value = 0

    for j in range(len(comb_list)):
        combination = hand_ranking(list(comb_list[j]))

        if combination[1] > best_value:
            player.card_set = combination
            best_value = combination[1]


class Game:
    """
    Invokes phases of game:
    1.Exchange of cards
    2.Flop - 3 cards from deck are shown to all players
    3.Turn - 1 card -||-
    4.River - 1 card -||-
    5.Cards showdown, player with best 5-card set wins.
    """

    def __init__(self, deck, players):
        self.deck = deck
        self.table = []  # list of cards on table
        self.players = players

    def exchange(self, deck, game):
        for player in self.players:
            if player.is_AI_controlled:
                player.exchange_simulation(deck)
            else:
                player.exchange(deck)

    def check_sets(self):
        for i in range(len(self.players)):
            hands_combinations(self.table, self.players[i])

    def print_players(self):
        for player in self.players:
            print(player)

    def print_table(self):
        for i in self.table:
            print(self.table[self.table.index(i)])

    def flop(self):
        print("------------------Flop------------------")
        for i in range(1, 4):
            card = self.deck.pop()
            self.table.append(card)
            print("{}. {}".format(i, card))

    def turn(self):
        print("------------------Turn------------------")
        card = self.deck.pop()
        self.table.append(card)
        print("{}. {}".format(4, card))

    def river(self):
        print("------------------River------------------")
        card = self.deck.pop()
        self.table.append(card)
        print("{}. {}".format(5, card))

    def result(self):
        winner = self.players[0]
        count = 0

        for player in self.players:
            print("Player {} has {} with value of {}".format(player.name, player.card_set[0], player.card_set[1]))
            if player.card_set[1] > winner.card_set[1]:
                winner = player
                count = 0
            elif player.card_set[1] == winner.card_set[1]:
                count += 1

        if count == len(self.players):
            print("Draw!")
        else:
            print("{} wins the pot!".format(winner.name))


"""
def display_game():
    pygame.init()
    screen = pygame.display.set_mode((1181, 695))
    clock = pygame.time.Clock()
    bg = pygame.image.load("assets/table.png")
    card = pygame.image.load('assets/2C.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(bg, (0, 0))
        screen.blit(card, (464, 510))
        pygame.display.flip()
        clock.tick(30)
"""


def main():
    deck = Deck()
    deck.generate()
    deck.shuffle()

    alex = Player(name="Alex", deck=deck, AI=False)
    bot_1 = Player(name="Bot_1", deck=deck, AI=True)
    bot_2 = Player(name="Bot_2", deck=deck, AI=True)

    game = Game(deck, [alex, bot_1, bot_2])

    game.print_players()
    game.exchange(deck, game)

    game.flop()
    game.turn()
    game.river()

    game.check_sets()
    game.result()


if __name__ == '__main__':
    main()
