import pygame
import os
from itertools import cycle
from utils.manage_dictionnary import add_new_word_list_to_dest, create_list_for_game, add_words_to_file

PATH_TO_DICTIONNARY = os.path.join("src", "utils", "dictionnary.txt")
PATH_TO_NEW_WORDS = os.path.join("src", "utils", "new_words.txt")
PATH_TO_TEMP_GAME_DICT = os.path.join(
    "src", "utils", "temp_game_dictionnary.txt")


def initialize_game():
    pygame.mixer.music.set_volume(0.05)
    params = {
        'capital_letters': True,
        'accents': False,
        'punctuation': False,
        'numbers': True
    }
    words = create_list_for_game(
        params=params, source=PATH_TO_DICTIONNARY, dest=PATH_TO_TEMP_GAME_DICT)
    words = cycle(words)
    pygame.mixer.music.load(os.path.join(
        "src", "assets", "sound_effects", "background_music.mp3"))
    pygame.mixer.music.play(-1)
    return words


class TextManager:
    def __init__(self):
        self.data = initialize_game()
        self.current_text = next(self.data)
        self.next_text = next(self.data)

    def next_text_set(self):
        self.current_text = self.next_text
        try:
            self.next_text = next(self.data)
        except StopIteration:
            self.next_text = None  # or some default text

    def is_current_text_finished(self, current_index):
        return current_index > len(self.current_text) - 1
