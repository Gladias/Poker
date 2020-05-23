# Poker
# 2 cards in hand, possibility to exchange cards at the beginning of a game.
import pygame

from deck import Deck
from game import Game
from player import Player
from const import ASSETS, WINDOW_WIDTH, WINDOW_HEIGHT, FONT_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    deck = Deck()
    deck.generate()
    deck.shuffle()

    # Only one player can be AI=False, this is user
    alex = Player(name="Alex", deck=deck, money=1000, AI=False, position=0)
    bot_1 = Player(name="Bot_1", deck=deck, money=1000, AI=True, position=1)
    bot_2 = Player(name="Bot_2", deck=deck, money=1000, AI=True, position=2)
    bot_3 = Player(name="Bot_3", deck=deck, money=1000, AI=True, position=3)
    bot_4 = Player(name="Bot_4", deck=deck, money=1000, AI=True, position=4)

    game = Game(deck, alex, [bot_1, bot_2, bot_3, bot_4], screen)
    game.run()


if __name__ == '__main__':
    main()
