# Poker
# 2 cards in hand, possibility to exchange cards at the beginning of a game.
import random


class Card:
    """Represent a single card."""

    def __init__(self, number, symbol):
        self.number = number
        self.symbol = symbol

    def __str__(self):
        return "{} of {}".format(self.number, self.symbol)


class Deck:
    """
    Represent a deck of 52 cards.
    Cards are numerated from 1 to 13, where:
    1 - Ace
    2 to 10 - normal cards
    11 - Jack
    12 - Queen
    13 - King
    """
    symbols = ["Hearts", "Spades", "Clubs", "Diamonds"]

    def __init__(self):
        self.deck = []

    def generate(self):
        next_element = -1

        for i in range(52):
            if i % 13 == 0:
                next_element += 1

            # add cards and replace numbers 1, 11, 12, 13 with names
            if i % 13 + 1 == 1:
                self.deck.append(Card("Ace", self.symbols[next_element]))

            elif i % 13 + 1 == 11:
                self.deck.append(Card("Jack", self.symbols[next_element]))

            elif i % 13 + 1 == 12:
                self.deck.append(Card("Queen", self.symbols[next_element]))

            elif i % 13 + 1 == 13:
                self.deck.append(Card("King", self.symbols[next_element]))

            else:
                self.deck.append(Card(i % 13 + 1, self.symbols[next_element]))

    def shuffle(self):
        random_list = random.sample(range(52), 52)

        for i in range(52):
            swap = self.deck[i]
            random_element = random_list.pop()

            self.deck[i] = self.deck[random_element]
            self.deck[random_element] = swap

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

    def __str__(self):
        return "{} has: {} AND {}\n".format(self.name, self.card_1, self.card_2)

    def exchange(self):
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


class Game:
    """
    Invokes phases of game:
    1.Exchange of cards
    2.Flop - 3 cards from deck are shown to all players
    3.Turn - 1 card -||-
    4.River - 1 card -||-
    5.Cards showdown, player with best 5-card set wins.
    """

    def __init__(self, deck, player_1, player_2):
        self.deck = deck
        self.player_1 = player_1
        self.player_2 = player_2

    def exchange(self):
        self.player_1.exchange()
        self.player_2.exchange()

    def flop(self):
        print("------------------Flop------------------")
        for i in range(1, 4):
            print("{}. {}".format(i, self.deck.pop()))

    def turn(self):
        print("------------------Turn------------------")
        print("{}. {}".format(4, self.deck.pop()))

    def river(self):
        print("------------------River------------------")
        print("{}. {}".format(5, self.deck.pop()))


deck = Deck()
deck.generate()
deck.shuffle()

game = Game(deck, Player("Alex", deck), Player("Computer", deck))

print(game.player_1)
print(game.player_2)

game.exchange()

print(game.player_1)
print(game.player_2)

game.flop()
game.turn()
game.river()
