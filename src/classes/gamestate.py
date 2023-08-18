from enum import Enum

from .constants import linked_save_results


class GameMode(Enum):
    CHRONO = 1
    TRAINING = 2


class GameState:
    def __init__(self):
        self.APP_RUN = True
        self.should_init_menu = True
        self.game_mode = GameMode.CHRONO
        self.run_game = False
        self.run_dictionnary_menu = False
        self.run_menu = True
        self.run_game_result = False
        self.time_start_game = 0
        self.results_menu_selected = linked_save_results
        self.nb_char_typed = 0
        self.time_elapsed = 0.0001

    def quit(self):
        self.APP_RUN = False

    def calculate_wpm(self):
        time_elapsed_in_min = self.time_elapsed / 60000
        wpm = round((self.nb_char_typed / 5)/time_elapsed_in_min, 1)
        return str(wpm)