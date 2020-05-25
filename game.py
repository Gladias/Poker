import sys

import pygame

import deck
from hand_evaluation import hands_combinations
from const import ASSETS, WINDOW_WIDTH, WINDOW_HEIGHT, FONT_SIZE, SECOND_HAND_CARD_X, FIRST_HAND_CARD_X, HAND_CARDS_Y, \
    BORDER_SIZE, TABLE_CARD_1_X, TABLE_CARDS_Y, TABLE_CARDS_OFFSET, CARD_WIDTH
from interface import Button, prepare_message, prepare_buttons, prepare_text, Text, Chip


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

    def playing_players(self):
        playing_players = []

        if self.player.is_playing:
            playing_players.append(self.player)

        for bot in self.bots:
            if bot.is_playing:
                playing_players.append(bot)

        return playing_players

    def next_player_turn(self, player):
        players_list_iter = iter(self.playing_players())

        player.is_player_turn = False
        next(players_list_iter).is_player_turn = True

    def previous_player(self, player):
        players_list = self.playing_players()

        if player in players_list:
            return players_list[players_list.index(player) - 1]

        else:
            print("Player doesnt exist in game")

    def raise_pot(self, player, bet_value, chip_list, font):
        previous_bet_size = self.previous_player(self.player).bet_size
        bet_value = int(bet_value)
        print(bet_value)

        if not previous_bet_size < bet_value <= self.player.money:
            print("Wrong bet value")

        else:
            player.money -= bet_value
            self.round_pot += bet_value
            self.next_player_turn(player)
            chip_list.append(Chip(player.position, bet_value, font))

            return "{} raises to ${}".format(player.name, bet_value)

    def call(self, player, chip_list, font):  # TODO: global font
        previous_player = self.previous_player(self.player)

        if previous_player.bet_size == 0 or self.round_pot == 0:
            return "You cant call"

        if self.player.money < previous_player.bet_size:
            return "You don't have ${} to call".format(previous_player.bet_size)

        else:
            player.money -= previous_player.bet_size
            self.round_pot += previous_player.bet_size
            self.next_player_turn(player)
            chip_list.append(Chip(player.position, previous_player.bet_size, font))

            return "{} call ${}".format(player.name, previous_player.bet_size)


    def fold(self, player):
        if player.is_playing:
            player.is_playing = False
            return "{} folds".format(player.name)
        else:
            return "You are not in game this turn"

    def bet(self, deck):
        self.round_pot = 0

        for bot in self.bots:
            bot.bet_simulation(deck)

        if self.player.is_playing:
            if 0 < bet_size < player.money:
                player.money -= bet_size
                self.round_pot += bet_size
                self.game_pot += bet_size

            print("| ROUND POT IS {}$ |".format(self.round_pot))


    def flop(self, card_list):
        # Run function only once
        if len(card_list) == 2:
            for i in range(3):
                card = self.deck.pop()
                card.downscale()

                card.set_position(TABLE_CARD_1_X + (card.rect.width + TABLE_CARDS_OFFSET)*i, TABLE_CARDS_Y)

                card_list.append(card)
                self.table.append(card)

    def turn(self, card_list):
        if len(card_list) == 5:
            card = self.deck.pop()
            card.downscale()

            card.set_position(TABLE_CARD_1_X + (card.rect.width + TABLE_CARDS_OFFSET)*3, TABLE_CARDS_Y)

            card_list.append(card)
            self.table.append(card)

    def river(self, card_list):
        if len(card_list) == 6:
            card = self.deck.pop()
            card.downscale()

            card.set_position(TABLE_CARD_1_X + (card.rect.width + TABLE_CARDS_OFFSET)*4, TABLE_CARDS_Y)

            card_list.append(card)
            self.table.append(card)

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

        # List of objects to render
        card_list = [self.player.card_1, self.player.card_2]
        raise_button, call_button, fold_button, input_box = prepare_buttons(font)
        button_list = [raise_button, call_button, fold_button, input_box]
        text_list = prepare_text(self.player.name, self.player.money, self.round_pot, self.game_pot, self.bots, font)
        chip_list = []

        self.screen.blit(background, (0, 0))

        bet_input = ""

        self.player.adjust_cards_position()

        # TODO: all_cards = pygame.sprite.Group()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Handle bet size box
                if event.type == pygame.TEXTINPUT and event.text.isdigit():
                    bet_input += event.text
                    button_list[3].update_text(event.text, font)

                if event.type == pygame.MOUSEBUTTONUP:
                    # TODO: CHANGE INDEX
                    if input_box.rect.collidepoint(event.pos):
                        pygame.key.start_text_input()

                    else:
                        pygame.key.stop_text_input()


                #pygame.display.flip()

                if stage == "bet":

                    self.player.is_player_turn = True  # TODO: Change

                    # Buttons

                    # Testing
                    self.previous_player(self.player).bet_size = 50
                    self.round_pot = 50

                    if event.type == pygame.MOUSEBUTTONUP and self.player.is_player_turn:
                        if fold_button.rect.collidepoint(event.pos):
                            self.fold(self.player)

                        elif call_button.rect.collidepoint(event.pos):
                            message = Text(self.call(self.player, chip_list, font), font)
                            # TODO: Make update method
                            text_list = prepare_text(self.player.name, self.player.money, self.round_pot, self.game_pot, self.bots, font)
                            text_list.append(message)

                        elif raise_button.rect.collidepoint(event.pos):
                            message = Text(self.raise_pot(self.player, bet_input, chip_list, font), font)
                            # TODO: Make update method
                            text_list = prepare_text(self.player.name, self.player.money, self.round_pot, self.game_pot, self.bots, font)
                            text_list.append(message)
                            print(len(chip_list))

                    # stage = next(self.stages)

                    #print(pygame.event.event_name(event.type))

                    #if event.type == pygame.TEXTINPUT:
                    #    print("{}".format(event.text))
                    #self.bet(self.deck)

                    #for bot in self.bots:
                    #    bot.bet_simulation()

                elif stage == "exchange":
                    message = Text("{} click on cards you would like to replace".format(self.player.name), font)
                    if len(text_list) == 8:
                        text_list.append(message)

                    button = Button(pygame.Rect(WINDOW_WIDTH/2 - 70, WINDOW_HEIGHT/2 + 80, 120, 40), "Continue", font)
                    # TODO: Change
                    if len(button_list) == len(prepare_buttons(font)):
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

                            # Clear message, adjust cards, remove continue button, update card_list
                            button_list.pop()
                            text_list.pop()
                            self.player.adjust_cards_position()
                            card_list = [self.player.card_1, self.player.card_2]

                            # Run exchange simulation for bots
                            # TODO: Threads maybe
                            # TODO: UNCOMMENT
                            #for bot in self.bots:
                            #   bot.exchange_simulation(self.deck)

                            stage = next(self.stages)

                elif stage == "flop":
                    self.flop(card_list)
                    stage = next(self.stages)

                elif stage == "turn":
                    self.turn(card_list)
                    stage = next(self.stages)

                elif stage == "river":
                    self.river(card_list)
                    #stage = next(self.stages)

                # Render background and objects
                self.screen.blit(background, (0, 0))

                #for card in card_list:
                #    self.screen.blit(card.image, card.rect)

                for button in button_list:
                    pygame.draw.rect(self.screen, button.border_color, button.border_rect, border_radius=BORDER_SIZE)
                    pygame.draw.rect(self.screen, button.bg_color, button.rect, border_radius=BORDER_SIZE)
                    self.screen.blit(button.caption, button.text_rect)

                for card in card_list:
                    self.screen.blit(card.image, card.rect)
                    self.screen.blit(card.image, card.rect)

                for text in text_list:
                    self.screen.blit(text.text, text.rect)

                for chip in chip_list:
                    self.screen.blit(chip.image, chip.chip_rect)
                    self.screen.blit(chip.text, chip.text_rect)

                pygame.display.flip()

