import pygame

import deck
import game
import const
import player


def main():
    """Initializes Pygame, generates deck of cards, makes players and runs game."""
    pygame.init()
    screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))

    game_deck = deck.Deck()
    game_deck.generate()
    game_deck.shuffle()

    # Player with AI=False is main player and can occur only once in list of players
    alex = player.Player(name="Player", deck=game_deck, position=0, is_AI_controlled=False)
    bot_1 = player.Player(name="Bot_1", deck=game_deck, position=1)
    bot_2 = player.Player(name="Bot_2", deck=game_deck, position=2)
    bot_3 = player.Player(name="Bot_3", deck=game_deck, position=3)
    bot_4 = player.Player(name="Bot_4", deck=game_deck, position=4)

    poker = game.Game(game_deck, alex, [bot_1, bot_2, bot_3, bot_4], screen)
    poker.run()


if __name__ == '__main__':
    main()
