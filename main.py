# Poker
# 2 cards in hand, possibility to exchange cards at the beginning of a game.
from deck import Deck
from display import display_game
from game import Game
from player import Player


def main():
    display_game()
    deck = Deck()
    deck.generate()
    deck.shuffle()

    alex = Player(name="Alex", deck=deck, money=1000, AI=False)
    john = Player(name="John", deck=deck, money=1000, AI=False)
    bot_1 = Player(name="Bot_1", deck=deck, money=1000, AI=True)
    bot_2 = Player(name="Bot_2", deck=deck, money=1000, AI=True)

    game = Game(deck, [alex, john, bot_1, bot_2])

    game.print_players()
    game.exchange(deck)

    game.bet(deck)
    game.flop()

    game.bet(deck)
    game.turn()

    game.bet(deck)
    game.river()

    game.bet(deck)
    game.check_sets()
    game.result()


if __name__ == '__main__':
    main()
