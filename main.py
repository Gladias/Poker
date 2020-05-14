# Poker
# 2 cards in hand, possibility to exchange cards at the beginning of a game.

from deck import Deck
from game import Game
from player import Player

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
