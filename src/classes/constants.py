import pygame
import pygame.freetype
import os
from enum import Enum
import json

pygame.mixer.init()
pygame.font.init()

# load config
PATH_TO_CONFIG = os.path.join("config.json")


def load_config():
    with open(PATH_TO_CONFIG, 'r') as file:
        config = json.load(file)
    return config


CONFIG = load_config()


# Constants
FPS = 240
WIN_SIZE = WIDTH, HEIGHT = 1500, 844

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (167, 190, 211)
YELLOW_ORANGE = (253, 184, 19)
YELLOW_ORANGE_DARK = (158, 148, 115)
DEEP_BLUE = (7, 27, 130)
GREY = (125, 125, 125)
LIGHT_GREY = (175, 175, 175)
GREEN_RIGHT = (8, 160, 69)
DARK_PURPLE = (96, 81, 109)
RED_WRONG = (240, 83, 101)

# Initialize Window
WIN = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("Typing Training")

# Load Sounds
SOUND_VOLUME = float(CONFIG['sound_volume'])
pygame.mixer.music.set_volume(SOUND_VOLUME)
SOUND_KEYPAD = pygame.mixer.Sound(os.path.join("src",
                                               "assets", "sound_effects", "keypad.mp3"))
SOUND_KEYPAD.set_volume(SOUND_VOLUME*1.5)
SOUND_KEYPAD_WRONG = pygame.mixer.Sound(
    os.path.join("src", "assets", "sound_effects", "wrong.wav")
)
SOUND_KEYPAD_WRONG.set_volume(SOUND_VOLUME*1.3)
SOUND_SELECT_MENU = pygame.mixer.Sound(
    os.path.join("src", "assets", "sound_effects", "menu.wav")
)
SOUND_SELECT_MENU.set_volume(SOUND_VOLUME/2.5)

# Load Images
IMG_BACKGROUND_LOADING_SCREEN = pygame.image.load(
    os.path.join("./src/assets/images/yellow_duck_wp.jpg"))
IMG_BACKGROUND_GAME_RIGHT = pygame.image.load(
    os.path.join("./src/assets/images/yellow_wallpaper_right.jpg")
)
IMG_BACKGROUND_GAME_SIMPLE = pygame.image.load(
    os.path.join("./src/assets/images/yellow_wallpaper_clean.jpg")
)
IMG_BACKGROUND_GAME_WRONG = pygame.image.load(
    os.path.join("./src/assets/images/yellow_wallpaper_wrong.jpg")
)
IMG_BACKGROUND_RESULTS = pygame.image.load(
    os.path.join("./src/assets/images/yellow_wp_results.jpg")
)

# Fonts
FONT_HELVETICA = pygame.font.SysFont("helvetica", 40)
FONT_ARABOTO_50 = pygame.font.SysFont("haraboto", 50)
FONT_ARABOTO_80 = pygame.font.SysFont("haraboto", 80)

# Pre-rendered Texts
text_menu_welcome = FONT_ARABOTO_80.render("Typing Session", 1, DEEP_BLUE)
text_menu_start_game = FONT_ARABOTO_50.render(
    "Start new session", 1, DEEP_BLUE)
text_menu_dictionnary = FONT_ARABOTO_50.render(
    "Dictionnary management (soon)", 1, DEEP_BLUE)
text_menu_progression_link = FONT_ARABOTO_50.render(
    "Show progression", 1, DEEP_BLUE)
text_results_menu_save = FONT_ARABOTO_50.render("Save Results", 1, DEEP_BLUE)
text_results_menu_continue = FONT_ARABOTO_50.render("Continue", 1, DEEP_BLUE)


class LinkedText:
    """Class to link text for a menu"""

    def __init__(self, x, y, next_text, prev_text, name=None):
        self.x = x
        self.y = y
        self.name = name
        self.next_text = next_text
        self.prev_text = prev_text

    def draw(self, surface, text, selected_menu):
        """Draw the text with line or not if selected."""
        if self == selected_menu:
            new_size = (text.get_width() * 1, text.get_height() * 1)
            new_text = pygame.transform.scale(text, new_size)
            surface.blit(
                new_text,
                (self.x - new_text.get_width() / 2,
                 self.y - new_text.get_height() / 2),
            )

            start_pos = (
                self.x - new_text.get_width() / 2,
                self.y + new_text.get_height() / 2,
            )
            end_pos = (
                self.x + new_text.get_width() / 2,
                self.y + new_text.get_height() / 2,
            )
            pygame.draw.line(
                surface, GREY, start_pos, end_pos, width=int(
                    text.get_height() * 0.08)
            )

        else:
            surface.blit(
                text, (self.x - text.get_width() / 2,
                       self.y - text.get_height() / 2)
            )


# LinkedText Instances
start_game = LinkedText(WIDTH / 2, HEIGHT / 3.6, None, None)
dictionnary = LinkedText(WIDTH / 2, HEIGHT / 2.2, start_game, None)
progression_link = LinkedText(WIDTH / 2, HEIGHT / 2.7, dictionnary, start_game)
dictionnary.prev_text = progression_link
start_game.prev_text, start_game.next_text = dictionnary, progression_link

linked_save_results = LinkedText(
    WIDTH / 2, HEIGHT * 0.6, None, None, "Save results"
)
linkedback_to_menu = LinkedText(
    WIDTH / 2, HEIGHT * 0.67, linked_save_results, linked_save_results, "Back menu"
)
linked_save_results.next_text, linked_save_results.prev_text = (
    linkedback_to_menu,
    linkedback_to_menu,
)


class KeyPressResponse(Enum):
    NO_TEST = 0
    WRONG = 1
    CORRECT = 2
    NO_ACTION = 3
