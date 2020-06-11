import enum
import pathlib


class SetsAndValues(enum.Enum):
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def describe(self):
        return self.name, self.value


# Flags storing information about player
class PlayerFlags:
    def __init__(self, AI_controlled=True, active=True, player_turn=False, bankrupt=False):
        self.is_AI_controlled = AI_controlled
        self.is_active = active
        self.is_player_turn = player_turn
        self.is_bankrupt = bankrupt


CARD_NAMES = {
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace",
}

STARTING_MONEY = 1000

GAME_STAGES = ["replace", "bet", "flop", "bet", "turn", "bet", "river", "bet", "result"]

ASSETS = pathlib.Path("assets/")

# Colors
BUTTON_COLOR = (248, 152, 56)
FONT_COLOR = (0, 0, 0)
INPUT_COLOR = (255, 255, 255)

FONT_SIZE = 20

BORDER_SIZE = 5

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

CARD_WIDTH = 112
CARD_HEIGHT = 152

CARD_DOWNSCALE_WIDTH = 90
CARD_DOWNSCALE_HEIGHT = 122

FIRST_HAND_CARD_X = 503
SECOND_HAND_CARD_X = 632
HAND_CARDS_Y = 528

CARD_CLICK_OFFSET = 15

BOTS_POSITION = [(1100, 440),  # BOT_1
                 (910, 190),   # BOT_2
                 (360, 190),   # BOT_3
                 (170, 440)]   # BOT_4

# Table cards
TABLE_CARD_1_X = 400
TABLE_CARDS_Y = 300
TABLE_CARDS_OFFSET = 10


# Chips
CHIP_WIDTH = 24
CHIP_HEIGHT = 24

CHIP_CAPTION = (12, 12)

CHIPS_POSITION = [(440, 525),  # Player's chip
                  (970, 475),  # Bot_1's chip
                  (805, 235),  # Bot_2's chip
                  (410, 240),  # Bot_3's chip
                  (285, 475)]  # Bot_4's chip

# Text
INFO_POSITION = (625, 235)
TURN_INFO_POSITION = (625, 265)

PLAYER_NAME_POSITION = (870, 540)
PLAYER_MONEY_POSITION = (870, 575)

INPUT_INFO_POSITION = (1015, 610)

ROUND_POT_POSITION = (WINDOW_WIDTH / 2, 150)
GAME_POT_POSITION = (WINDOW_WIDTH / 2, 120)

TEXT_LIST_LEN = 9

# Buttons
CONTINUE = (WINDOW_WIDTH / 2 - 70, WINDOW_HEIGHT / 2 + 80, 120, 40)

FOLD = (825, 645, 100, 40)
CALL = (975, 645, 115, 40)
RAISE = (1125, 645, 100, 40)

INPUT_BOX = (1125, 590, 100, 40)

BUTTON_LIST_LEN = 4



