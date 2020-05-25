from pathlib import Path

# TODO: add consts

sets_and_values = [
    ("ROYAL FLUSH", 10),
    ("STRAIGHT FLUSH", 9),
    ("FOUR OF A KIND", 8),
    ("FULL HOUSE", 7),
    ("FLUSH", 6),
    ("STRAIGHT", 5),
    ("THREE OF A KIND", 4),
    ("TWO PAIRS", 3),
    ("ONE PAIR", 2),
    ("HIGH CARD", 1)
]

ASSETS = Path("assets/")

# Colors
ORANGE = (248, 152, 56)
BLACK = (0, 0, 0)

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

BOTS_POSITION = [(1100, 440),  # BOT_1
                 (910, 190),   # BOT_2
                 (350, 190),   # BOT_3
                 (170, 440)]   # BOT_4

# Table cards
TABLE_CARD_1_X = 400
TABLE_CARDS_Y = 300
TABLE_CARDS_OFFSET = 10


CHIP_WIDTH = 24
CHIP_HEIGHT = 24

CHIPS_POSITION = [(390, 535),  # Player's chip
                  (970, 475),  # Bot_1's chip
                  (820, 225),  # Bot_2's chip
                  (410, 225),  # Bot_3's chip
                  (285, 475)]  # Bot_4's chip
