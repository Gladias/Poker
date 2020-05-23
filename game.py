import sys

import pygame

import deck
from hand_evaluation import hands_combinations
from const import ASSETS, WINDOW_WIDTH, WINDOW_HEIGHT, FONT_SIZE, SECOND_HAND_CARD_X, FIRST_HAND_CARD_X, HAND_CARDS_Y, \
    BORDER_SIZE
from interface import Button, prepare_interface, prepare_message


class Game:
    """
    Invoke stages of game:
    1.Exchange of cards
    2.Bet
    3.Flop - 3 cards from deck are shown to all players
    4.Bet
    5.Turn - 1 card -||-
    6.Bet
    7.River - 1 card -||-
    8.Bet
    9.Cards showdown, player with best 5-card set wins.
    """

    # message = ""
    stages = iter(["exchange", "bet", "flop", "bet", "turn", "bet", "river", "bet", "result"])


    def __init__(self, deck, player, bots, screen):
        self.deck = deck
        self.table = []  # list of cards on table
        self.round_pot = 0
        self.game_pot = 0
        self.player = player
        self.bots = bots
        self.screen = screen

        # Add class variables
        #Game.screen =
        #Game.game_font =

    def exchange(self, deck):
        self.player.exchange(deck)
        #for player in self.players:
        #    if player.is_AI_controlled:
        #        player.exchange_simulation(deck)

         #   else:
          #      player.exchange(deck)

    def check_sets(self):
        for i in range(len(self.players)):
            hands_combinations(self.table, self.players[i])

    def print_table(self):
        for i in self.table:
            print(self.table[self.table.index(i)])

    def bet(self, deck):
        self.round_pot = 0

        self.player

        for player in self.players:
            if player.is_AI_controlled:
                player.bet_simulation(deck)

            else:
                print(player)
                print("{} enter bet size:".format(player.name))
                bet_size = int(input())

                if 0 < bet_size < player.money:
                    player.money -= bet_size
                    self.round_pot += bet_size
                    self.game_pot += bet_size

                    print("| ROUND POT IS {}$ |".format(self.round_pot))

                else:
                    print("Invalid value!")

    def flop(self):
        print("-----Flop-----Game pot = {}$-----".format(self.game_pot))
        for i in range(1, 4):
            card = self.deck.pop()
            self.table.append(card)
            print("{}. {}".format(i, card))

    def turn(self):
        print("-----Turn-----Game pot = {}$-----".format(self.game_pot))
        card = self.deck.pop()
        self.table.append(card)
        print("{}. {}".format(4, card))

    def river(self):
        print("-----River-----Game pot = {}$-----".format(self.game_pot))
        card = self.deck.pop()
        self.table.append(card)
        print("{}. {}".format(5, card))

    def result(self):
        winner = self.players[0]
        winners_list = []  # draw case

        for player in self.players:
            print("Player {} has {} with value of {}".format(player.name, player.card_set[0], player.card_set[1]))

            if player.card_set[1] > winner.card_set[1]:
                winner = player
                winners_list = []

            elif player.card_set[1] == winner.card_set[1]:
                winners_list.append(player)

        if len(winners_list) > 1:
            print("Draw, {}$ split between {} players".format(self.game_pot, len(winners_list)))

            split = round(self.game_pot / len(winners_list), 2)
            for player in winners_list:
                print("{} wins {}$".format(player.name, split))

        else:
            print("{} wins {}$".format(winner.name, self.game_pot))

    def run(self):
        # Window init
        icon = pygame.image.load(str(ASSETS / "icon.png"))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Poker")
        font = pygame.font.Font(str(ASSETS / "FiraCode-Medium.ttf"), FONT_SIZE)

        background = pygame.image.load(str(ASSETS / "table.png")).convert()

        stage = next(self.stages)  # First stage - cards exchange
        message = font.render("", True, (0, 0, 0))

        # List of objects to render, obj.image and obj.rect is required
        card_list = [self.player.card_1, self.player.card_2]
        button_list = []

        self.screen.blit(background, (0, 0))

        self.player.adjust_cards_position()

        # TODO: all_cards = pygame.sprite.Group()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                pygame.display.flip()

                if stage == "bet":
                    if len(button_list) == 0:
                        button_list.extend(prepare_interface(font))
                    #self.bet(self.deck)

                    #for bot in self.bots:
                    #    bot.bet_simulation()

                elif stage == "exchange":
                    message = prepare_message(font, "{} click on cards you would like to replace".format(self.player.name))
                    button = Button(pygame.Rect(WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2 + 100, 100, 40), "Continue", font)
                    # TODO: Change
                    if len(button_list) == 0:
                        button_list.append(button)

                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.player.card_1.rect.collidepoint(event.pos):
                            self.player.card_1.click()

                        elif self.player.card_2.rect.collidepoint(event.pos):
                            self.player.card_2.click()

                        elif button.rect.collidepoint(event.pos):
                            # Continue button has been clicked

                            if self.player.card_1.is_clicked():
                                self.player.exchange(self.player.card_1, self.deck)

                            if self.player.card_2.is_clicked():
                                self.player.exchange(self.player.card_2, self.deck)

                            # Clear message, adjust cards, remove continue button
                            button_list.pop()
                            message = prepare_message(font, "")
                            self.player.adjust_cards_position()

                            # Run exchange simulation for bots
                            # TODO: Threads maybe
                            # TODO: UNCOMMENT
                            #for bot in self.bots:
                            #   bot.exchange_simulation(self.deck)

                            stage = next(self.stages)

                elif stage == "flop":
                    self.flop()
                    stage = next(self.stages)

                elif stage == "turn":
                    self.turn()
                    stage = next(self.stages)

                elif stage == "river":
                    self.river()
                    stage = next(self.stages)

                # Render background and objects
                self.screen.blit(background, (0, 0))

                #for card in card_list:
                #    self.screen.blit(card.image, card.rect)

                for button in button_list:
                    pygame.draw.rect(self.screen, button.border_color, button.border_rect, border_radius=BORDER_SIZE)
                    pygame.draw.rect(self.screen, button.bg_color, button.rect, border_radius=BORDER_SIZE)
                    self.screen.blit(button.caption, button.text_rect)

                self.screen.blit(self.player.card_1.image, self.player.card_1.rect)
                self.screen.blit(self.player.card_2.image, self.player.card_2.rect)


                # Render text
                self.screen.blit(message, (380, 230))

                pygame.display.flip()

