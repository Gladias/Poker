# Poker
# 2 cards in hand, possibility to exchange cards at the beginning of a game.
import random
from itertools import combinations  # used in hands_ranking()
import pygame
import sys


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

    def generate(self):
        next_element = -1

        for i in range(52):
            if i % 13 == 0:
                next_element += 1

            self.deck.append(Card(i % 13 + 2, self.symbols[next_element]))  # numbers from 2 to 14

    def shuffle(self):
        random.shuffle(self.deck)

    def pop(self):
        return self.deck.pop()

    def print(self):
        for i in range(len(self.deck)):
            print(self.deck[i])


class Player:
    """Represent a hand of 2 cards"""

    def __init__(self, name, deck):
        self.name = name
        self.card_1 = deck.pop()
        self.card_2 = deck.pop()
        self.card_set = ()  # tuple with name and value of players 5 card set

    def __str__(self):
        return "{} has: {} AND {}\n".format(self.name, self.card_1, self.card_2)

    def exchange(self, deck):
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
        return "ROYAL FLUSH", 10

    elif flush and straight:
        return "STRAIGHT FLUSH", 9

    elif len(pairs) > 4:
        return "FOUR OF A KIND", 8

    elif len(pairs) == 4:
        return "FULL HOUSE", 7

    elif flush:
        return "FLUSH", 6

    elif straight:
        return "STRAIGHT", 5

    elif len(pairs) == 3:
        return "THREE OF A KIND", 4

    elif len(pairs) == 2:
        return "TWO PAIRS", 3

    elif len(pairs) == 1:
        return "ONE PAIR", 2

    else:
        return "HIGH CARD", 1


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

    def exchange(self, deck):
        for player in self.players:
            player.exchange(deck)

    def hands_combinations(self):
        """
        Check all 5 elements combinations of players cards and cards on table
        and set each players card_set tuple to the best combination they have.
        """
        for i in range(len(self.players)):
            cards = []
            cards.extend(self.table)
            cards.append(self.players[i].card_1)
            cards.append(self.players[i].card_2)

            comb_list = list(combinations(cards, 5))

            best_value = 0

            for j in range(len(comb_list)):
                combination = hand_ranking(list(comb_list[j]))

                if combination[1] > best_value:
                    self.players[i].card_set = combination
                    best_value = combination[1]

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


def main():
    display_game()
    print("xd")
    deck = Deck()
    deck.generate()
    deck.shuffle()
    # deck.print()

    alex = Player("Alex", deck)
    computer = Player("Computer", deck)

    game = Game(deck, [alex, computer])

    game.print_players()
    game.exchange(deck)
    game.flop()
    game.turn()
    game.river()
    game.hands_combinations()
    game.print_players()
    game.result()


if __name__ == '__main__':
    main()
