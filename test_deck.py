import pygame
import unittest

import card
import deck
import const


class TestDeck(unittest.TestCase):
    def setUp(self):
        # pygame is used in image loading
        pygame.init()
        pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))

        self.deck = deck.Deck()
        self.deck.generate()

    def test_generate(self):
        numbers_sum = sum([game_card.number for game_card in self.deck.deck])
        expected_sum = sum(range(2, 15)) * 4

        self.assertEqual(len(self.deck.deck), 52)
        self.assertEqual(numbers_sum, expected_sum)

    def test_push(self):
        begin_len = len(self.deck.deck)
        test_card = card.Card(5, "Hearts",  str(const.ASSETS / "cards" / "5H.png"))

        self.deck.push(test_card)

        self.assertEqual(len(self.deck.deck), begin_len + 1)
        self.assertEqual(self.deck.deck[-1], test_card)

    def test_draw(self):
        begin_len = len(self.deck.deck)
        last_card = self.deck.deck[-1]
        taken_card = self.deck.draw()

        self.assertEqual(len(self.deck.deck), begin_len - 1)
        self.assertEqual(taken_card, last_card)

    def test_remove(self):
        remove_card = card.Card(5, "Hearts",  str(const.ASSETS / "cards" / "5H.png"))
        begin_len = len(self.deck.deck)

        self.assertIn(remove_card, self.deck.deck)

        self.deck.remove(remove_card)

        self.assertNotIn(remove_card, self.deck.deck)
        self.assertEqual(len(self.deck.deck), begin_len - 1)


if __name__ == '__main__':
    unittest.main()
