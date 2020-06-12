import pygame
import unittest

import deck
import game
import const
import player


class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))

        game_deck = deck.Deck()
        game_deck.generate()
        game_deck.shuffle()

        alex = player.Player(name="Alex", deck=game_deck, position=0, is_AI_controlled=False)
        bot_1 = player.Player(name="Bot_1", deck=game_deck, position=1)
        bot_2 = player.Player(name="Bot_2", deck=game_deck, position=2)

        self.game = game.Game(game_deck, alex, [bot_1, bot_2], screen)

    def test_flop(self):
        card_list = [self.game.main_player.card_1,
                     self.game.main_player.card_2]

        self.game.flop(card_list)
        self.assertEqual(len(self.game.table), 3)

    def test_active_players(self):
        # All players are active by default
        active_players = self.game.active_players()

        self.assertEqual(len(active_players), 3)

    def test_next_player_turn(self):
        # is_player_turn flag is false by default
        # is_player_turn flag should "move" from last bot to main player
        self.game.bots[-1].flags.is_player_turn = True

        self.assertFalse(self.game.main_player.is_player_turn())

        self.game.next_player_turn()

        self.assertTrue(self.game.main_player.is_player_turn())
        self.assertFalse(self.game.bots[-1].is_player_turn())

    def test_raise_pot(self):
        chip_list = []
        begin_player_money = self.game.main_player.money
        self.game.main_player.flags.is_player_turn = True

        self.game.raise_pot(self.game.main_player, 500, chip_list)

        self.assertEqual(self.game.main_player.money, begin_player_money - 500)
        self.assertEqual(len(chip_list), 1)
        self.assertEqual(self.game.round_pot, 500)

    def test_fold(self):
        self.game.bots[0].flags.is_player_turn = True

        self.game.fold(self.game.bots[0])

        self.assertFalse(self.game.bots[0].is_active())


if __name__ == '__main__':
    unittest.main()
