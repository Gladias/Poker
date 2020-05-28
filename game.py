import sys
from copy import deepcopy
from timeit import default_timer

import pygame
import time

import const
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

        #print(playing_players)
        return playing_players

    def next_player_turn(self):
        playing_players = self.playing_players()

        # List of format [false, false, false, true, false]
        players_turns = [player.is_player_turn for player in playing_players]
        print(players_turns)

        # If it's last player's turn, set turn to first player
        if players_turns[-1]:
            players_turns.reverse()

        else:
            true_index = players_turns.index(True)
            players_turns[true_index] = False
            players_turns[true_index + 1] = True  # Index out of range is removed in if statement

        # Assign new turn value to each player
        for index, _ in enumerate(players_turns):
            playing_players[index].is_player_turn = players_turns[index]

        #print("player {}, bot1 {}, bot2 {}, bot3 {}, bot4 {}".format(self.player.is_player_turn, self.bots[0].is_player_turn,
         #                                                            self.bots[1].is_player_turn, self.bots[2].is_player_turn,
         #                                                            self.bots[3].is_player_turn,))


    def previous_player(self, player):
        players_list = self.playing_players()

        if player in players_list:
            return players_list[players_list.index(player) - 1]

        else:
            print("Player doesnt exist in game")

    def raise_pot(self, player, bet_value, chip_list, font):
        print("raise")
        previous_bet_size = self.previous_player(player).bet_size
        bet_value = int(bet_value)
        print(bet_value)

        if not previous_bet_size - player.bet_size < bet_value - player.bet_size <= player.money:
            print("Wrong bet value")

        else:
            difference = bet_value - player.bet_size
            player.money -= difference
            self.round_pot += difference
            player.bet_size += difference
            self.next_player_turn()
            chip_list.append(Chip(player.position, bet_value, font))

            return "{} raises to ${}".format(player.name, bet_value)

    def call(self, player, chip_list, font):  # TODO: global font
        print("call")
        previous_player = self.previous_player(player)
        #print(previous_player.name)

        if previous_player.bet_size == 0 or self.round_pot == 0:
            print(previous_player.bet_size, self.round_pot)
            return "You cant call"

        if player.money + player.bet_size < previous_player.bet_size:
            return "You don't have ${} to call".format(previous_player.bet_size)

        else:
            difference = previous_player.bet_size - player.bet_size
            player.money -= difference
            self.round_pot += difference
            player.bet_size += difference
            self.next_player_turn()
            chip_list.append(Chip(player.position, previous_player.bet_size, font))

            return "{} calls ${}".format(player.name, previous_player.bet_size)


    def fold(self, player):
        print("fold")
        if player.is_playing:
            self.next_player_turn()
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

    def bet_simulation(self, bot, chip_list, font):
        """
        Bot makes bet decision based on
        previous player bet size to bot's money ratio
        and simulations including bot's cards and cards on table.
        When number of cards on table is less than 5, bots simulates
        missing cards.
        """


        message = ""
        previous_bet_size = self.previous_player(bot).bet_size

        if previous_bet_size - bot.bet_size == 0:
            can_bot_wait = True
        else:
            can_bot_wait = False

        if can_bot_wait:
            bet_ratio = 5
        else:
            print(previous_bet_size - bot.bet_size)
            bet_ratio = bot.money / (previous_bet_size - bot.bet_size)

        print(can_bot_wait)
        #print("bet ratio: ", bet_ratio)
        # TODO: ratio is veeery high, both should risk

        # Bot doesn't have enough money
        if previous_bet_size - bot.bet_size > bot.money:
            message = self.fold(bot)

        N = 5000  # number of simulations

        simulation_deck = deck.Deck()
        simulation_deck.generate()

        sets_counter = {
            "ROYAL FLUSH": 0,
            "STRAIGHT FLUSH": 0,
            "FOUR OF A KIND": 0,
            "FULL HOUSE": 0,
            "FLUSH": 0,
            "STRAIGHT": 0,
            "THREE OF A KIND": 0,
            "TWO PAIRS": 0,
            "ONE PAIR": 0,
            "HIGH CARD": 0
        }

        t_start = default_timer()

        for _ in range(N):
            simulation_deck.shuffle()
            simulation_table_cards = [simulation_deck.deck[i] for i in range(5 - len(self.table))]
            simulation_table_cards.extend(self.table)
            simulation_table_cards.append(bot.card_1)
            simulation_table_cards.append(bot.card_2)
            # print(len(simulation_table_cards))

            hands_combinations(simulation_table_cards, bot)  # TODO: change parameters
            sets_counter[bot.card_set[0]] += 1

        # Multiply sets by their value defined in const.py

        for i in range(len(sets_counter)):
            sets_counter[const.sets_and_values[i][0]] *= const.sets_and_values[i][1]

        simulation_value = sum(sets_counter.values())

        # Multiply simulation_value by bet_ratio
        # The lover the previous bet is
        # the bigger chance that bot will raise or call

        # TODO: game pot include
        simulation_value *= bet_ratio
        simulation_value /= N

        # These values will be adjusted based on in-game tests

        if simulation_value >= 3.5:
            # Bot raises
            money_left = bot.money + bot.bet_size - previous_bet_size

            high_raise, medium_raise, low_raise = 0.8, 0.5, 0.3  # [%]

            if simulation_value >= 5:
                bet_size = int(high_raise * money_left) + previous_bet_size
                message = self.raise_pot(bot, bet_size, chip_list, font)

            elif 4 <= simulation_value < 5:
                bet_size = int(medium_raise * money_left) + previous_bet_size
                message = self.raise_pot(bot, bet_size, chip_list, font)

            else:
                bet_size = int(low_raise * money_left) + previous_bet_size
                message = self.raise_pot(bot, bet_size, chip_list, font)

        elif 3 < simulation_value < 3.5:
            # Bot calls or waits

            if can_bot_wait:
                message = "{} waits".format(bot.name)
            else:
                message = self.call(bot, chip_list, font)

        else:
            # Bot folds
            message = self.fold(bot)

        #print(simulation_value)

        t_end = default_timer()
        elapsed_time = t_end - t_start

        # Made to remove bots instant moves
        if elapsed_time < 2:
            time.sleep(2)

        #print("{:.2f}s".format(elapsed_time))
        print(message)
        return message

    def flop(self, card_list):
        # Run function only once
        if len(card_list) == 2:
            for i in range(3):
                card = self.deck.draw()
                card.downscale()

                card.set_position(TABLE_CARD_1_X + (card.rect.width + TABLE_CARDS_OFFSET)*i, TABLE_CARDS_Y)

                card_list.append(card)
                self.table.append(card)

    def turn(self, card_list):
        if len(card_list) == 5:
            card = self.deck.draw()
            card.downscale()

            card.set_position(TABLE_CARD_1_X + (card.rect.width + TABLE_CARDS_OFFSET)*3, TABLE_CARDS_Y)

            card_list.append(card)
            self.table.append(card)

    def river(self, card_list):
        if len(card_list) == 6:
            card = self.deck.draw()
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

    def next_round(self, stage, player):
        pass

    def stage_clear(self, chip_list, text_list, font):
        self.game_pot += self.round_pot
        self.round_pot = 0
        chip_list.clear()
        text_list.pop()
        text_list[2].text_str = str(self.round_pot)
        text_list[3].text_str = str(self.game_pot)

        text_list[2].text_str = prepare_message(font, str(self.round_pot))
        text_list[3].text_str = prepare_message(font, str(self.game_pot))


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

        self.player.is_player_turn = True  # TODO: Change

        standard_text_list_len = len(text_list)

        #pl = self.previous_player(self.player)
        #pl.bet_size = 800
        #self.round_pot = 800

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

                    playing_players = self.playing_players()

                    if len(playing_players):
                        pass  # TODO: new game

                    # TODO: implement wait

                    if self.player.bet_size == playing_players[-1].bet_size and self.player.bet_size > 0:
                        stage = next(self.stages)

                    screen_update(button_list, card_list, text_list, chip_list, background, self.screen)

                    if self.player.is_player_turn:
                        message = Text("{} it's your turn".format(self.player.name), font)
                        #print(len(text_list), standard_text_list_len + 1, "AAAAAAAAAAA")
                        if len(text_list) == standard_text_list_len + 1:
                            text_list.pop()
                            text_list.append(message)

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

                    screen_update(button_list, card_list, text_list, chip_list, background, self.screen)

                    if not self.player.is_player_turn:
                        for bot in self.bots:
                            if bot.is_playing:
                                message = Text(self.bet_simulation(bot, chip_list, font), font)
                                # TODO: Make update method
                                text_list = prepare_text(self.player.name, self.player.money, self.round_pot, self.game_pot, self.bots, font)
                                text_list.append(message)
                                screen_update(button_list, card_list, text_list, chip_list, background, self.screen)

                                if playing_players[0].bet_size == playing_players[-1].bet_size and playing_players[0].bet_size > 0:
                                    stage = next(self.stages)

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
                    #self.stage_clear(chip_list, text_list, font)
                    screen_update(button_list, card_list, text_list, chip_list, background, self.screen)
                    self.flop(card_list)
                    stage = next(self.stages)

                elif stage == "turn":
                    #self.stage_clear(chip_list, text_list, font)
                    screen_update(button_list, card_list, text_list, chip_list, background, self.screen)
                    self.turn(card_list)
                    stage = next(self.stages)

                elif stage == "river":
                    #self.stage_clear(chip_list, text_list, font)
                    screen_update(button_list, card_list, text_list, chip_list, background, self.screen)
                    self.river(card_list)
                    print("NEW ROUND")
                    #stage = next(self.stages)

                screen_update(button_list, card_list, text_list, chip_list, background, self.screen)





def screen_update(button_list, card_list, text_list, chip_list, background, screen):
    screen.blit(background, (0, 0))

    for button in button_list:
        pygame.draw.rect(screen, button.border_color, button.border_rect, border_radius=BORDER_SIZE)
        pygame.draw.rect(screen, button.bg_color, button.rect, border_radius=BORDER_SIZE)
        screen.blit(button.caption, button.text_rect)

    for card in card_list:
        screen.blit(card.image, card.rect)
        screen.blit(card.image, card.rect)

    for text in text_list:
        screen.blit(text.text, text.rect)

    for chip in chip_list:
        screen.blit(chip.image, chip.chip_rect)
        screen.blit(chip.text, chip.text_rect)

    pygame.display.flip()
