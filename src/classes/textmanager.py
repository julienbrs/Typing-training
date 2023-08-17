import pygame
import os
from itertools import cycle
from utils.manage_dictionnary import main as manage_dictionnary_main


def initialize_game():
    pygame.mixer.music.set_volume(0.05)
    dictio = manage_dictionnary_main("temp.txt", "dictionnary.txt")
    data = cycle(dictio)
    pygame.mixer.music.load(
        os.path.join("src", "assets", "sound_effects", "background_music.mp3")
    )
    pygame.mixer.music.play(-1)
    return data


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
        return current_index >= len(self.current_text) - 1
