from hand_evaluation import hands_combinations


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

    def __init__(self, deck, players):
        self.deck = deck
        self.table = []  # list of cards on table
        self.round_pot = 0
        self.game_pot = 0
        self.players = players

    def exchange(self, deck):
        for player in self.players:
            if player.is_AI_controlled:
                player.exchange_simulation(deck)

            else:
                player.exchange(deck)

    def check_sets(self):
        for i in range(len(self.players)):
            hands_combinations(self.table, self.players[i])

    def print_players(self):
        for player in self.players:
            print(player)

    def print_table(self):
        for i in self.table:
            print(self.table[self.table.index(i)])

    def bet(self, deck):
        self.round_pot = 0

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
