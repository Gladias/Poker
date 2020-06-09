import copy
import sys
import time
import timeit

import pygame

import deck
import const
import interface
import hand_evaluation


class Game:
    """Controls game flow, handles user input, displays object on screen and invokes game stages.

    Game stages:
    1.Replacement of cards
    2.Bet
    3.Flop - 3 common cards are displayed on table
    4.Bet
    5.Turn - 1 common card is displayed on table
    6.Bet
    7.River - 1 common card is displayed on table
    8.Bet
    9.Cards showdown, player with best 5-card set wins.
    """

    def __init__(self, game_deck, main_player, bots, screen):
        self.game_deck = game_deck
        self.table = []  # list of cards on table
        self.stages = iter(const.GAME_STAGES)
        self.round_pot = 0
        self.game_pot = 0
        self.main_player = main_player
        self.bots = bots
        self.info = ""
        self.screen = screen
        self.font = pygame.font.Font(str(const.ASSETS / "FiraCode-Medium.ttf"), const.FONT_SIZE)

    def active_players(self):
        """Returns list of players that didn't fold this turn."""
        active_players = []

        if self.main_player.is_active:
            active_players.append(self.main_player)

        for bot in self.bots:
            if bot.is_active:
                active_players.append(bot)

        return active_players

    def next_player_turn(self):
        """Sets is_player_turn flag for next active player."""
        active_players = self.active_players()

        # List of format [false, false, false, true, false]
        players_turns = [player.flags.is_player_turn for player in active_players]

        if players_turns[-1]:  # If it's last player's turn, set turn to first player
            players_turns.reverse()
        else:
            true_index = players_turns.index(True)
            players_turns[true_index] = False
            players_turns[true_index + 1] = True  # Index out of range case is caught in if statement

        # Assign new turn value to each player
        for index, _ in enumerate(players_turns):
            active_players[index].flags.is_player_turn = players_turns[index]

    def previous_player(self, player):
        """Returns previous player to given player."""
        players_list = self.active_players()
        return players_list[players_list.index(player) - 1]

    def raise_pot(self, player, bet_value, chip_list):
        """Raise.

        Raises round pot, decreases player's money,
        adds chip with bet_value to chip_list and sets game info.
        """
        previous_bet = (self.previous_player(player)).bet_size
        bet_value = int(bet_value)

        # if player bet this turn subtract previous bet value
        # if player didn't bet player.bet_size is equal to 0
        bet = bet_value - player.bet_size

        if not previous_bet - player.bet_size < bet <= player.money:
            self.info = "Wrong bet value"

        else:
            player.money -= bet
            self.round_pot += bet
            player.bet_size += bet

            chip_list.append(interface.Chip(None, bet_value, self.font, player.position))

            self.info = "{} raises to ${}".format(player.name, bet_value)
            self.next_player_turn()

    def call(self, player, chip_list):
        """Call.

        Raises round pot by previous player bet_size, decreases player's money,
        adds chip with bet_value to chip_list and sets game info.
        """
        previous_player = self.previous_player(player)

        if previous_player.bet_size == 0 or self.round_pot == 0:
            self.info = "You cant call"

        if player.money + player.bet_size < previous_player.bet_size:
            self.info = "You don't have ${} to call".format(previous_player.bet_size)

        else:
            bet = previous_player.bet_size - player.bet_size
            player.money -= bet
            self.round_pot += bet
            player.bet_size = previous_player.bet_size

            chip_list.append(interface.Chip(player.position, previous_player.bet_size,
                                            self.font, player.position))

            self.info = "{} calls ${}".format(player.name, previous_player.bet_size)
            self.next_player_turn()

    def wait(self, player):
        """Sets is_player_turn to True for next player,

        If previous player didn't bet player can wait and not make any actions.
        """
        self.info = "{} waits".format(player.name)
        self.next_player_turn()

    def fold(self, player):
        """Sets player's is_active flag to false."""
        if player.is_active:
            self.next_player_turn()
            player.flags.is_active = False

            self.info = "{} folds".format(player.name)
        else:
            self.info = "You are not in game this turn"

    def replace(self, event, button_list):
        """Replaces cards clicked by player."""
        continue_button = interface.Button(pygame.Rect(const.CONTINUE), "Continue", self.font)

        # Add button to list only once
        if len(button_list) == const.BUTTON_LIST_LEN:
            button_list.append(continue_button)

        if event.type == pygame.MOUSEBUTTONUP:
            if self.main_player.card_1.rect.collidepoint(event.pos):
                self.main_player.card_1.click()

            elif self.main_player.card_2.rect.collidepoint(event.pos):
                self.main_player.card_2.click()

            elif continue_button.rect.collidepoint(event.pos):
                # Continue button has been clicked
                if self.main_player.card_1.is_clicked():
                    self.main_player.replace_card(self.main_player.card_1, self.game_deck)

                if self.main_player.card_2.is_clicked():
                    self.main_player.replace_card(self.main_player.card_2, self.game_deck)

                # Adjust cards, remove continue button, update card_list
                button_list.pop()
                self.main_player.set_cards_position()
                return True
        return False

    def replace_simulation(self, bot, game_deck):
        """Decide which cards to exchange in AI controlled players"""
        t_start = timeit.default_timer()
        N = 5000
        # Number of simulations per case, there are 4 cases because player can do 1 action from 4 available:
        # 1. Don't exchange cards
        # 2. Replace first card
        # 3. Replace second card
        # 4. Replace both cards

        simulation_deck = deck.Deck()
        simulation_deck.generate()

        # Remove 2 cards in player's hand from simulation deck
        simulation_deck.remove(bot.card_1)
        simulation_deck.remove(bot.card_2)

        card_1 = bot.card_1
        card_2 = bot.card_2

        sets_counter = {
            "ROYAL_FLUSH": 0,
            "STRAIGHT_FLUSH": 0,
            "FOUR_OF_A_KIND": 0,
            "FULL_HOUSE": 0,
            "FLUSH": 0,
            "STRAIGHT": 0,
            "THREE_OF_A_KIND": 0,
            "TWO_PAIRS": 0,
            "ONE_PAIR": 0,
            "HIGH_CARD": 0
        }

        arr = [copy.deepcopy(sets_counter) for _ in range(4)]

        # 1. Don't replace cards

        for _ in range(N):
            simulation_deck.shuffle()
            table_cards = [simulation_deck.deck[i] for i in range(5)]
            table_cards.append(bot.card_1)
            table_cards.append(bot.card_2)
            hand_evaluation.hands_combinations(table_cards, bot)
            arr[0][bot.card_set[0]] += 1

        # 2. Replace first card

        bot.card_1 = simulation_deck.draw()

        for _ in range(N):
            simulation_deck.shuffle()
            table_cards = [simulation_deck.deck[i] for i in range(5)]
            table_cards.append(bot.card_1)
            table_cards.append(bot.card_2)
            hand_evaluation.hands_combinations(table_cards, bot)
            arr[1][bot.card_set[0]] += 1

        simulation_deck.push(bot.card_1)
        bot.card_1 = card_1

        # 3. Replace second card

        bot.card_2 = simulation_deck.draw()

        for _ in range(N):
            simulation_deck.shuffle()
            table_cards = [simulation_deck.deck[i] for i in range(5)]
            table_cards.append(bot.card_1)
            table_cards.append(bot.card_2)
            hand_evaluation.hands_combinations(table_cards, bot)
            arr[2][bot.card_set[0]] += 1

        simulation_deck.push(bot.card_2)
        bot.card_2 = card_2

        # 4. Replace both cards

        bot.card_1 = simulation_deck.draw()
        bot.card_2 = simulation_deck.draw()

        for _ in range(N):
            simulation_deck.shuffle()
            table_cards = [simulation_deck.deck[i] for i in range(5)]
            table_cards.append(bot.card_1)
            table_cards.append(bot.card_2)
            hand_evaluation.hands_combinations(table_cards, bot)
            arr[3][bot.card_set[0]] += 1

        simulation_deck.push(bot.card_1)
        simulation_deck.push(bot.card_2)
        bot.card_1 = card_1
        bot.card_2 = card_2

        # Multiply set_counter by value of particular set, and add it to row values

        rows_values = [0, 0, 0, 0]

        for i, _ in enumerate(arr):  # 4
            for key, value in sets_counter.items():
                arr[i][key] *= const.SetsAndValues[key].value
                rows_values[i] += arr[i][key]

        best_variant = rows_values.index(max(rows_values))

        print(rows_values)

        if best_variant == 0:
            self.info = "{} doesn't exchange any cards.".format(bot.name)
        elif best_variant == 1:
            self.info = "{} exchanges first card.".format(bot.name)
            bot.card_1 = game_deck.draw()
        elif best_variant == 2:
            self.info = "{} exchanges second card.".format(bot.name)
            bot.card_2 = game_deck.draw()
        else:
            self.info = "{} exchanges both cards.".format(bot.name)
            bot.card_1 = game_deck.draw()
            bot.card_2 = game_deck.draw()

        t_end = timeit.default_timer()
        print("Bot made a decision in {:.2f}s|".format(t_end - t_start))

    def bet(self, event, active_players, fold_button, call_button, raise_button, chip_list, bet_input):
        if not active_players:
            pass  # TODO: new game

        if self.main_player.is_player_turn:
            self.info = "{} it's your turn".format(self.main_player.name)

        if event.type == pygame.MOUSEBUTTONUP and self.main_player.is_player_turn:
            if fold_button.rect.collidepoint(event.pos):
                self.fold(self.main_player)

            elif call_button.rect.collidepoint(event.pos):
                previous_bet_size = self.previous_player(self.main_player).bet_size

                if not previous_bet_size - self.main_player.bet_size:
                    self.wait(self.main_player)
                else:
                    self.call(self.main_player, chip_list)
                interface.text_init(self)

            elif raise_button.rect.collidepoint(event.pos):
                self.raise_pot(self.main_player, bet_input, chip_list)
                interface.text_init(self)

            return True
        return False

    def bet_simulation(self, bot, chip_list):
        """Decides to call, raise or fold in AI controlled players.

        Bot makes bet decision based on
        previous player bet size to bot's money ratio
        and simulations including bot's cards and cards on table.
        When number of cards on table is less than 5, bot draws random
        missing cards.
        """

        previous_bet_size = self.previous_player(bot).bet_size

        if not previous_bet_size - bot.bet_size:
            can_bot_wait = True
            bet_ratio = 5
        else:
            can_bot_wait = False
            bet_ratio = bot.money / (previous_bet_size - bot.bet_size)

        # Bot doesn't have enough money
        if previous_bet_size > bot.money + bot.bet_size:
            self.fold(bot)

        N = 5000  # number of simulations

        simulation_deck = deck.Deck()
        simulation_deck.generate()

        sets_counter = {
            "ROYAL_FLUSH": 0,
            "STRAIGHT_FLUSH": 0,
            "FOUR_OF_A_KIND": 0,
            "FULL_HOUSE": 0,
            "FLUSH": 0,
            "STRAIGHT": 0,
            "THREE_OF_A_KIND": 0,
            "TWO_PAIRS": 0,
            "ONE_PAIR": 0,
            "HIGH_CARD": 0
        }

        t_start = timeit.default_timer()

        for _ in range(N):
            simulation_deck.shuffle()
            simulation_table_cards = [simulation_deck.deck[i] for i in range(5 - len(self.table))]
            simulation_table_cards.extend(self.table)
            simulation_table_cards.append(bot.card_1)
            simulation_table_cards.append(bot.card_2)

            hand_evaluation.hands_combinations(simulation_table_cards, bot)
            sets_counter[bot.card_set[0]] += 1

        # Multiply sets by their value defined in const.py

        for key, value in sets_counter.items():
            value *= const.SetsAndValues[key].value

        print(sets_counter)

        simulation_value = sum(sets_counter.values())

        # Multiply simulation_value by bet_ratio
        # The lover the previous bet is
        # the bigger chance that bot will raise or call

        simulation_value *= bet_ratio
        simulation_value /= N

        # These values will be adjusted based on in-game tests

        if simulation_value >= 3.5:
            # Bot raises
            money_left = bot.money + bot.bet_size - previous_bet_size

            high_raise, medium_raise, low_raise = 0.8, 0.5, 0.3  # [%]

            if simulation_value >= 5:
                bet_size = int(high_raise * money_left) + previous_bet_size
                self.raise_pot(bot, bet_size, chip_list)

            elif 4 <= simulation_value < 5:
                bet_size = int(medium_raise * money_left) + previous_bet_size
                self.raise_pot(bot, bet_size, chip_list)

            else:
                bet_size = int(low_raise * money_left) + previous_bet_size
                self.raise_pot(bot, bet_size, chip_list)

        elif 3 < simulation_value < 3.5:
            # Bot calls or waits

            if can_bot_wait:
                self.wait(bot)
            else:
                self.call(bot, chip_list)

        else:
            # Bot folds
            self.fold(bot)

        t_end = timeit.default_timer()
        elapsed_time = t_end - t_start

        # Removes bot's instant moves
        if elapsed_time < 2:
            time.sleep(2)

        print("Bet simulation {:.2f}s".format(elapsed_time))

    def flop(self, card_list):
        """Display first 3 common cards on table."""
        if len(card_list) == 2:
            for i in range(3):
                card = self.game_deck.draw()
                card.downscale()

                card.set_position(
                    const.TABLE_CARD_1_X + (card.rect.width + const.TABLE_CARDS_OFFSET) * i,
                    const.TABLE_CARDS_Y)

                card_list.append(card)
                self.table.append(card)

    def turn(self, card_list):
        """Display fourth common card on table."""
        if len(card_list) == 5:
            card = self.game_deck.draw()
            card.downscale()

            card.set_position(
                const.TABLE_CARD_1_X + (card.rect.width + const.TABLE_CARDS_OFFSET) * 3,
                const.TABLE_CARDS_Y)

            card_list.append(card)
            self.table.append(card)

    def river(self, card_list):
        """Display last common card on table."""
        if len(card_list) == 6:
            card = self.game_deck.draw()
            card.downscale()

            card.set_position(
                const.TABLE_CARD_1_X + (card.rect.width + const.TABLE_CARDS_OFFSET) * 4,
                const.TABLE_CARDS_Y)

            card_list.append(card)
            self.table.append(card)

    def result(self):
        """Chooses round winner.

        Compares active players card sets and gives round pot to winner or splits pot in case of draw.
        """
        active_players = self.active_players()
        winner = active_players[0]
        winners_list = []  # draw case

        for player in active_players:
            if player.card_set[1] > winner.card_set[1]:
                winner = player
                winners_list = []

            elif player.card_set[1] == winner.card_set[1]:
                winners_list.append(player)

        if len(winners_list) > 1:
            self.info = "Draw, {} players have {}".format(
                len(winners_list),
                winners_list[0].card_set[0])

            split = int(self.game_pot / len(winners_list))
            for player in winners_list:
                player.money += split
                self.game_pot = 0
        else:
            self.info = "{} wins {}$ with {}".format(
                winner.name,
                self.game_pot,
                winner.card_set[0])

            winner.money += self.game_pot
            self.game_pot = 0

    def next_stage(self, button_list, card_list, text_list, chip_list, background):
        """Clears chips and adds round pot to game pot before moving to next stage."""
        self.game_pot += self.round_pot
        self.round_pot = 0
        interface.clear_stage(self.game_pot, self.round_pot, chip_list, text_list)
        interface.update_screen(button_list, card_list, text_list, chip_list, background, self.screen)

    def run(self):
        """Main function, controls game flow, user input and display."""
        icon = pygame.image.load(str(const.ASSETS / "icon.png"))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Poker")

        background = pygame.image.load(str(const.ASSETS / "table.png")).convert()

        stage = next(self.stages)  # First stage - cards replacement

        # Lists of objects rendered each frame
        card_list = [self.main_player.card_1, self.main_player.card_2]
        raise_button, call_button, fold_button, input_box = interface.buttons_init(self)
        button_list = [raise_button, call_button, fold_button, input_box]
        chip_list = []
        text_list = interface.text_init(self)

        bet_input = ""

        self.main_player.set_cards_position()
        self.main_player.flags.is_player_turn = True

        self.screen.blit(background, (0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Handle bet size box
                if event.type == pygame.TEXTINPUT and event.text.isdigit():
                    bet_input += event.text
                    input_box.update_text(bet_input)

                if event.type == pygame.MOUSEBUTTONUP:
                    if input_box.rect.collidepoint(event.pos):
                        pygame.key.start_text_input()
                    else:
                        pygame.key.stop_text_input()

                if stage == "bet":
                    active_players = self.active_players()

                    if self.main_player.bet_size == active_players[-1].bet_size \
                            and self.main_player.bet_size > 0:
                        stage = next(self.stages)

                    if self.bet(event, active_players, fold_button, call_button, raise_button, chip_list, bet_input):
                        text_list = interface.text_init(self)
                        interface.update_screen(button_list, card_list, text_list, chip_list,
                                                background, self.screen)
                        interface.update_info(self.info, self.font, self.screen)
                        pygame.display.flip()

                        # Run bet simulation for bots
                        if not self.main_player.flags.is_player_turn:
                            for bot in self.bots:
                                if bot.flags.is_active:
                                    self.bet_simulation(bot, chip_list)
                                    text_list = interface.text_init(self)
                                    interface.update_screen(button_list, card_list, text_list,
                                                            chip_list, background, self.screen)
                                    interface.update_info(self.info, self.font, self.screen)
                                    pygame.display.flip()
                                    if active_players[0].bet_size == active_players[-1].bet_size \
                                            and active_players[0].bet_size > 0:
                                        stage = next(self.stages)

                elif stage == "replace":
                    self.info = "{} click on cards you would like to replace".format(self.main_player.name)
                    interface.update_info(self.info, self.font, self.screen)
                    # Replace method returns True if player clicked continue button
                    if self.replace(event, button_list):
                        card_list = [self.main_player.card_1, self.main_player.card_2]

                        self.info = "Bots make replacement simulations"
                        interface.update_screen(button_list, card_list, text_list, chip_list,
                                                background, self.screen)
                        interface.update_info(self.info, self.font, self.screen)
                        pygame.display.flip()

                        # Run replacement simulation for bots
                        for bot in self.bots:
                            self.replace_simulation(bot, self.game_deck)

                        stage = next(self.stages)

                elif stage == "flop":
                    self.next_stage(button_list, card_list, text_list, chip_list, background)
                    self.flop(card_list)
                    stage = next(self.stages)

                elif stage == "turn":
                    self.next_stage(button_list, card_list, text_list, chip_list, background)
                    self.turn(card_list)
                    stage = next(self.stages)

                elif stage == "river":
                    self.next_stage(button_list, card_list, text_list, chip_list, background)
                    self.river(card_list)
                    print("NEW ROUND")
                    # stage = next(self.stages)

                interface.update_screen(button_list, card_list, text_list, chip_list, background, self.screen)
                interface.update_info(self.info, self.font, self.screen)
                pygame.display.flip()
