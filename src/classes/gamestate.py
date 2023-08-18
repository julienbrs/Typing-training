from enum import Enum

from .constants import linked_save_results, start_game


class GameMode(Enum):
    CHRONO = 1
    TRAINING = 2

class GameState(Enum):
    MAIN_MENU = 1
    IN_GAME = 2
    RESULTS_MENU = 3
    DICTIONNARY_MENU = 4

class Game:
    def __init__(self):
        self.gamestate = GameState.MAIN_MENU
        self.APP_RUN = True
        self.should_init_menu = True
        self.game_mode = GameMode.CHRONO
        self.time_start_game = 0
        self.main_menu_selected = start_game
        self.results_menu_selected = linked_save_results
        self.nb_char_typed = 0
        self.time_elapsed = 0.0001
        self.text_blink_tick = 0

    def quit(self):
        self.APP_RUN = False

    def calculate_wpm(self):
        time_elapsed_in_min = self.time_elapsed / 60000
        wpm = round((self.nb_char_typed / 5)/time_elapsed_in_min, 1)
        return str(wpm)