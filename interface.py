import pygame

from const import ORANGE, BLACK, BORDER_SIZE, FONT_SIZE, WINDOW_WIDTH, BOTS_POSITION, CHIPS_POSITION, CHIP_HEIGHT, \
    ASSETS


class Button:
    def __init__(self, rect, caption, font, bg_color=ORANGE, border_size=BORDER_SIZE, border_color=BLACK):
        self.rect = rect
        self.caption_str = caption
        self.caption = prepare_message(font, self.caption_str)
        self.font = font
        self.text_rect = self.caption.get_rect(center=(self.rect.x + self.rect.width/2, self.rect.y + self.rect.height/2))
        self.bg_color = bg_color
        self.border_rect = (rect.x - border_size, rect.y - border_size, rect.width + 2*border_size, rect.height + 2*border_size)
        self.border_color = border_color

    def update_text(self, letter, font):
        self.caption_str += letter
        self.caption = prepare_message(font, self.caption_str)
        self.text_rect.x = self.rect.x


class Text:
    def __init__(self, text, font, x=380, y=230, font_size=FONT_SIZE, color=BLACK):
        self.font = font
        self.text_str = text
        self.text = prepare_message(self.font, text)
        self.rect = self.text.get_rect(center=(x, y))


class Chip:
    def __init__(self, position, value: int, font, image_path=str(ASSETS / "casino.png")):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.chip_rect = self.image.get_rect(center=CHIPS_POSITION[position])
        #self.chip_rect.x, self.chip_rect.y = CHIPS_POSITION(position)
        self.value = value
        self.font = font
        self.text = prepare_message(self.font, str(self.value))

        self.text_rect = self.text.get_rect(center=(self.chip_rect.x + 12, self.chip_rect.y + 35))
        print(self.chip_rect.x, self.text_rect.x)

# TODO: Maybe move prepare def to classes


def get_chip_position(player_position):
    return CHIPS_POSITION(player_position)

def prepare_buttons(font):
    raise_button = Button(pygame.Rect(825, 645, 100, 40), "Raise", font, ORANGE)
    call_button = Button(pygame.Rect(825 + 150, 645, 100, 40), "Call", font, ORANGE)
    fold_button = Button(pygame.Rect(825 + 300, 645, 100, 40), "Fold", font, ORANGE)

    input_box = Button(pygame.Rect(825 + 260, 545, 140, 50), "", font, (255, 255, 255))

    return raise_button, call_button, fold_button, input_box


def prepare_text(name, money, round_pot, game_pot, bots, font):
    player_name = Text(name, font, 880, 555)
    player_money = Text("${}".format(money), font, 880, 595)
    round_pot = Text("Round pot: ${}".format(round_pot), font, WINDOW_WIDTH/2, 150)
    game_pot = Text("Game pot: ${}".format(game_pot), font, WINDOW_WIDTH/2, 120)

    text_list = [player_name, player_money, round_pot, game_pot]

    for index, bot in enumerate(bots):
        x, y = BOTS_POSITION[index]
        text_list.append(Text("{}    ${}".format(bot.name, bot.money), font, x, y))

    return text_list


def prepare_message(font, text, x=300, y=300):
    return font.render(text, True, (0, 0, 0))




# class Interface:
#    def __init__(self):
#        self.button_list = []
