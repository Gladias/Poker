import pygame
import sys
from pathlib import Path

from const import ASSETS, WINDOW_WIDTH, WINDOW_HEIGHT

def display_game():
    pygame.init()

    pygame.display.set_caption("Poker")
    icon = pygame.image.load(str(ASSETS / "icon.png"))
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    bg = pygame.image.load("assets/table.png").convert()
    card = pygame.image.load('assets/cards/2D.png').convert_alpha()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(bg, (0, 0))
        screen.blit(card, (632, 528))
        pygame.display.flip()
        clock.tick(30)
