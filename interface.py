import pygame

import const


class GameObject:
    """Base class for game objects."""
    def __init__(self, rect, text, font):
        self.rect = rect

        self.text = text
        self.font = font
        self.rendered_text = self.render_text(text)
        self.text_rect = self.rendered_text.get_rect()

    def render_text(self, text, color=const.FONT_COLOR):
        """Renders Pygame text object with given text value."""
        return self.font.render(text, True, color)

    def update_text(self, new_text):
        """Updates text value and invokes render_text method."""
        self.text = new_text
        self.rendered_text = self.render_text(new_text)

    def update_rect_position(self, is_center_update, x, y):
        """Updates object's rect position."""
        if is_center_update:
            self.rect.center = (x, y)
        else:
            self.rect.x = x
            self.rect.y = y


class Text(GameObject):
    """Represents text object."""
    def __init__(self, text, font, position=const.INFO_POSITION, rect=None):
        super().__init__(rect, text, font)
        self.text_rect.center = position


class Button(GameObject):
    """Represents button with position, centered caption, color and border."""
    def __init__(self, rect, text, font,
                 bg_color=const.BUTTON_COLOR,
                 border_size=const.BORDER_SIZE,
                 border_color=const.FONT_COLOR):

        super().__init__(rect, text, font)
        self.text_rect.center = (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2)

        self.bg_color = bg_color
        self.border_rect = (
            rect.x - border_size, rect.y - border_size,
            rect.width + 2 * border_size, rect.height + 2 * border_size)
        self.border_color = border_color


class Chip(GameObject):
    """Represents chip with position, image and caption with value."""
    def __init__(self, rect, value, font, position):
        super().__init__(rect, str(value), font)
        self.image = pygame.image.load(str(const.ASSETS / "chip.png")).convert_alpha()
        self.rect = self.image.get_rect(center=const.CHIPS_POSITION[position])

        self.value = value
        self.text_rect.center = (self.rect.centerx, self.rect.y - const.CHIP_CAPTION[1])


def text_init(game):
    """Initializes texts: round and game pot, name and money for every player."""
    game_info = Text(game.info, game.font, const.INFO_POSITION)

    player_name = Text(game.main_player.name, game.font, const.PLAYER_NAME_POSITION)
    player_money = Text("${}".format(game.main_player.money), game.font, const.PLAYER_MONEY_POSITION)
    input_info = Text("Enter bet size ->", game.font, const.INPUT_INFO_POSITION)
    input_info.rendered_text = input_info.render_text(input_info.text, const.BUTTON_COLOR)

    round_pot = Text("Round pot: ${}".format(game.round_pot), game.font, const.ROUND_POT_POSITION)
    game_pot = Text("Game pot: ${}".format(game.game_pot), game.font, const.GAME_POT_POSITION)

    text_list = [player_name, player_money, round_pot, game_pot, input_info]

    for index, bot in enumerate(game.bots):
        text_list.append(Text("{}    ${}".format(bot.name, bot.money), game.font, const.BOTS_POSITION[index]))

    return text_list


def buttons_init(game):
    """Initializes raise, call, fold and input buttons."""
    raise_button = Button(pygame.Rect(const.RAISE), "Raise", game.font, const.BUTTON_COLOR)
    call_button = Button(pygame.Rect(const.CALL), "Call|Wait", game.font, const.BUTTON_COLOR)
    fold_button = Button(pygame.Rect(const.FOLD), "Fold", game.font, const.BUTTON_COLOR)

    input_box = Button(pygame.Rect(const.INPUT_BOX), "", game.font, const.INPUT_COLOR)

    return raise_button, call_button, fold_button, input_box


def clear_stage(game_pot, round_pot, chip_list, text_list):
    """Clears chip_list and updates game and round pot display."""
    chip_list.clear()
    # text_list.pop()

    for obj in text_list:
        if "Round" in obj.text:
            obj.update_text(str("Round pot: ${}".format(round_pot)))
        elif "Game" in obj.text:
            obj.update_text(str("Game pot: ${}".format(game_pot)))


def update_info(info, font, screen):
    text = Text(info, font, const.INFO_POSITION)
    screen.blit(text.rendered_text, text.text_rect)


def player_turn_info(font, screen):
    return Text("It's your turn", font, const.TURN_INFO_POSITION)


def update_screen(button_list, card_list, text_list, chip_list, background, screen):
    """Renders buttons, texts, cards and chips objects"""
    screen.blit(background, (0, 0))

    for button in button_list:
        # Pygame version >= 2.0.0.dev8 is required for border_radius rect parameter.
        pygame.draw.rect(screen, button.border_color, button.border_rect, border_radius=const.BORDER_SIZE)
        pygame.draw.rect(screen, button.bg_color, button.rect, border_radius=const.BORDER_SIZE)
        screen.blit(button.rendered_text, button.text_rect)

    for card in card_list:
        screen.blit(card.image, card.rect)
        screen.blit(card.image, card.rect)

    for text in text_list:
        screen.blit(text.rendered_text, text.text_rect)

    for chip in chip_list:
        screen.blit(chip.image, chip.rect)
        screen.blit(chip.rendered_text, chip.text_rect)
