from pathlib import Path

sets_and_values = [
    ("ROYAL FLUSH",     10),
    ("STRAIGHT FLUSH",  9),
    ("FOUR OF A KIND",  8),
    ("FULL HOUSE",      7),
    ("FLUSH",           6),
    ("STRAIGHT",        5),
    ("THREE OF A KIND", 4),
    ("TWO PAIRS",       3),
    ("ONE PAIR",        2),
    ("HIGH CARD",       1)
]

ASSETS = Path("assets/")

FONT_SIZE = 20

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

CARD_WIDTH = 112
CARD_HEIGHT = 152

FIRST_HAND_CARD_X = 503
SECOND_HAND_CARD_X = 632
HAND_CARDS_Y = 528
