# pylint: disable=no-member
# pylint: disable=W0603     disable global variable warning
import sys
import pygame
import pygame.freetype
import os
from itertools import cycle
import manage_dictionnary

# imports from constants module
from constants import (
    WIN,
    WIDTH,
    HEIGHT,
    FPS,
    WIN_SIZE,
    YELLOW_ORANGE,
    DEEP_BLUE,
    GREEN_RIGHT,
    DARK_PURPLE,
    RED_WRONG,
    SOUND_KEYPAD,
    SOUND_KEYPAD_WRONG,
    SOUND_SELECT_MENU,
    IMG_BACKGROUND_LOADING_SCREEN,
    IMG_BACKGROUND_GAME_RIGHT,
    IMG_BACKGROUND_GAME_WRONG,
    IMG_BACKGROUND_RESULTS,
    FONT_HELVETICA,
    FONT_ARABOTO_50,
    FONT_ARABOTO_80,
    text_menu_welcome,
    text_menu_start_game,
    text_menu_dictionnary,
    text_menu_leaderboard,
    text_results_menu_save,
    text_results_menu_continue,
    start_game,
    dictionnary,
    leaderboard,
    MENU_SELECTED,
    linked_save_results,
    linkedback_to_menu,
    RESULTS_MENU_SELECTED,
    KeyPressResponse
)

# Initialize Pygame modules
pygame.freetype.init()
pygame.font.init()
pygame.mixer.init()


def draw_text_center(surface, text, x_ratio, y_ratio):
    surface.blit(
        text,
        (
            x_ratio * WIDTH - text.get_width() / 2,
            y_ratio * HEIGHT - text.get_height() / 2,
        ),
    )


def update_menu_selection(menu_selected, text_scroll):
    if text_scroll == "DOWN":
        menu_selected = menu_selected.next_text
        text_scroll = None
    elif text_scroll == "UP":
        menu_selected = menu_selected.prev_text
        text_scroll = None
    return menu_selected, text_scroll


def draw_menu(text_blink, text_scroll, surface):
    global MENU_SELECTED
    surface.blit(
        pygame.transform.scale(IMG_BACKGROUND_LOADING_SCREEN, WIN_SIZE), (0, 0)
    )
    text_blink = (text_blink + 1) % 350
    if text_blink <= 200:
        draw_text_center(surface, text_menu_welcome, 0.5, 0.1)

    start_game.draw(surface, text_menu_start_game, MENU_SELECTED)
    leaderboard.draw(surface, text_menu_leaderboard, MENU_SELECTED)
    dictionnary.draw(surface, text_menu_dictionnary, MENU_SELECTED)

    MENU_SELECTED, text_scroll = update_menu_selection(
        MENU_SELECTED, text_scroll)

    pygame.display.update()
    return text_blink, text_scroll


def draw_menu_results(text_scroll, maxtime_chrono, wpm, mode):
    global RESULTS_MENU_SELECTED

    WIN.blit(IMG_BACKGROUND_RESULTS, (0, 0))
    str_results_mod = "Temps limité: " + \
        str(round(maxtime_chrono / 1000, 1)
            ) if (mode == "MOD_CHRONO") else "Pas de temps indiqué"
    str_results_wpm = "Résultat: " + str(wpm)

    draw_text_center(WIN, FONT_ARABOTO_80.render(
        "Résultats", 1, DEEP_BLUE), 0.5, 0.25)
    draw_text_center(WIN, FONT_ARABOTO_50.render(
        str_results_mod, 1, DEEP_BLUE), 0.5, 0.37)
    draw_text_center(WIN, FONT_ARABOTO_50.render(
        str_results_wpm, 1, DEEP_BLUE), 0.5, 0.44)

    linked_save_results.draw(
        WIN, text_results_menu_save, RESULTS_MENU_SELECTED)
    linkedback_to_menu.draw(
        WIN, text_results_menu_continue, RESULTS_MENU_SELECTED)

    RESULTS_MENU_SELECTED, text_scroll = update_menu_selection(
        RESULTS_MENU_SELECTED, text_scroll)

    pygame.display.update()
    return text_scroll


def blit_text_to_window(text, position):
    WIN.blit(text, position)


def display_elapsed_time(time_start):
    time_atm = pygame.time.get_ticks()
    time_elapsed = time_atm - time_start
    str_time = str(round(time_elapsed / 1000, 1))
    text_time = FONT_ARABOTO_50.render(str_time, 1, DARK_PURPLE)
    blit_text_to_window(
        text_time, (WIDTH * 0.95 - text_time.get_width(), HEIGHT * 0.18))


def display_remaining_time(time_start, max_time):
    time_atm = pygame.time.get_ticks()
    time_elapsed = time_atm - time_start
    str_time = str(round((max_time - time_elapsed) / 1000, 1))
    text_time = FONT_ARABOTO_50.render(str_time, 1, DARK_PURPLE)
    blit_text_to_window(
        text_time, (WIDTH * 0.95 - text_time.get_width(), HEIGHT * 0.18))

    if max_time - time_elapsed <= 0:
        return True
    return False


def initialize_game():
    pygame.mixer.music.set_volume(0.05)
    dictio = manage_dictionnary.main("temp.txt", "dictionnary.txt")
    data = cycle(dictio)
    pygame.mixer.music.load(
        os.path.join("assets", "sound_effects", "background_music.mp3")
    )
    pygame.mixer.music.play(-1)
    return data


class GameState:
    def __init__(self):
        self.APP_RUN = True
        self.INIT_MENU = True
        self.MOD_CHRONO = True
        self.MOD_TRAINING = False
        self.run_game = False
        self.run_menu = True
        self.run_game_result = False
        self.time_start_game = 0
        # Add any other variables you need here

    def quit(self):
        self.APP_RUN = False


class BackgroundManager:
    def __init__(self):
        self.IMG_BACKGROUND_GAME = IMG_BACKGROUND_GAME_RIGHT

    def set_wrong(self):
        self.IMG_BACKGROUND_GAME = pygame.transform.scale(
            IMG_BACKGROUND_GAME_WRONG, WIN_SIZE)

    def set_right(self):
        self.IMG_BACKGROUND_GAME = pygame.transform.scale(
            IMG_BACKGROUND_GAME_RIGHT, WIN_SIZE)

    def display(self):
        WIN.blit(self.IMG_BACKGROUND_GAME, (0, 0))


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


class UIManager:
    def __init__(self, window):
        self.WIN = window

    def display_wpm(self, wpm):
        str_hud = "WPM : " + wpm
        text_wpm = FONT_ARABOTO_50.render(str_hud, 1, DARK_PURPLE)
        self.WIN.blit(text_wpm, (WIDTH * 0.95 -
                      text_wpm.get_width(), HEIGHT * 0.08))

    def display_next_text(self, next_text):
        next_text_game = FONT_HELVETICA.render(next_text, 1, DARK_PURPLE)
        next_text_game.set_alpha(180)
        self.WIN.blit(next_text_game, (WIDTH * 0.5 -
                      next_text_game.get_width() / 2, HEIGHT * 0.57))

    def draw_current_text(self, font, text_manager, current_index, test_letter, last_key_wrong):
        M_ADV_X = 4  # todo ??? Madv_x

        # calculate how big the entire line of text is
        text_surf_rect = font.get_rect(text_manager.current_text)
        text_surf_rect.size = (
            text_surf_rect.size[0] * 1.1,
            text_surf_rect.size[1]
        )  # todo more elegant?

        # This rect's y property is the baseline since we use the origin mode
        baseline = text_surf_rect.y

        # Create a surface to render the text on and center it on the screen
        text_surf = pygame.Surface(text_surf_rect.size)
        text_surf_rect.center = self.WIN.get_rect().center

        # Calculate the width (and other stuff) for each letter of the text
        metrics = font.get_metrics(text_manager.current_text)

        # Fill the surface
        text_surf.fill(YELLOW_ORANGE)

        x = 0
        for (idx, (letter, metric)) in enumerate(zip(text_manager.current_text, metrics)):
            # Set default color
            color = DARK_PURPLE

            # select the right color
            if idx == current_index:
                start_pos = (
                    text_surf_rect.x + x + 3,
                    text_surf_rect.y + text_surf_rect.height - 5,
                )
                end_pos = (
                    text_surf_rect.x + x + metric[M_ADV_X] - 5,
                    text_surf_rect.y + text_surf_rect.height - 5,
                )

                if test_letter in [KeyPressResponse.NO_TEST, KeyPressResponse.NO_ACTION]:
                    color = RED_WRONG if last_key_wrong else "lightblue"
                elif test_letter == KeyPressResponse.WRONG:
                    color = RED_WRONG
                elif test_letter == KeyPressResponse.CORRECT:
                    color = GREEN_RIGHT
                    
                else:
                    print(f"Error: {test_letter} not in enum")

                color_line = color
            elif idx < current_index:
                color = GREEN_RIGHT
            else:
                color = DARK_PURPLE

            # render the single letter
            font.render_to(text_surf, (x, baseline), letter, color)
            # and move the start position
            x += metric[M_ADV_X]

        self.WIN.blit(text_surf, text_surf_rect)
        self.draw_line_under_text(start_pos, end_pos, color_line)

    def draw_line_under_text(self, start_pos, end_pos, color):
        pygame.draw.line(self.WIN, color, start_pos, end_pos, width=5)


class EventHandler:
    def __init__(self, state, text_manager, background_manager, ui_manager):
        self.state = state
        self.text_manager = text_manager
        self.background_manager = background_manager
        self.ui_manager = ui_manager
        self.maxtime_chrono = 5000
        self.wpm = None

    def handle_key_press_event(self, text_target, current_index, last_key_wrong):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == text_target[current_index]:
                    pygame.mixer.Sound.play(SOUND_KEYPAD)
                    self.background_manager.set_right()
                    last_key_wrong = False
                    current_index += 1
                else:
                    pygame.mixer.Sound.play(SOUND_KEYPAD_WRONG)
                    self.background_manager.set_wrong()
                    last_key_wrong = True
        self.background_manager.display()
        return KeyPressResponse.NO_ACTION, last_key_wrong, current_index

    def handle_event(self, event, text_blink=0, text_scroll=None, current_index=0, last_key_wrong=False):
        if self.state.run_menu:
            return self._handle_menu_event(event, text_blink, text_scroll, current_index, last_key_wrong)
        elif self.state.run_game:
            return self._handle_game_event(event, text_blink, text_scroll, self.text_manager.current_text, current_index, last_key_wrong)
        elif self.state.run_game_result:
            return self.handle_game_result_event(event, text_blink, text_scroll, current_index, last_key_wrong)

    def _handle_menu_event(self, event, text_blink, text_scroll, current_index, last_key_wrong):
        if event.type == pygame.QUIT:
            self.state.run_menu = False
            self.state.APP_RUN = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                text_scroll = "UP"
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                text_blink, text_scroll = draw_menu(
                    text_blink - 1, text_scroll, WIN)

            elif event.key == pygame.K_DOWN:
                text_scroll = "DOWN"
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                text_blink, text_scroll = draw_menu(
                    text_blink - 1, text_scroll, WIN)

            elif event.key == pygame.K_RETURN and MENU_SELECTED == start_game:
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                self.state.run_menu = False
                self.state.run_game = True
                self.state.INIT_MENU = True
        return text_blink, text_scroll, current_index, last_key_wrong

    def _handle_game_event(self, event, text_blink, text_scroll, text_target, current_index, last_key_wrong):
        # Return these by default if no events change them
        new_text_blink = text_blink
        new_text_scroll = text_scroll

        if event.type == pygame.QUIT:
            self.state.run_game = False
            self.state.APP_RUN = False

        elif event.type == pygame.KEYDOWN:
            if event.unicode == text_target[current_index]:
                pygame.mixer.Sound.play(SOUND_KEYPAD)
                last_key_wrong = False
                current_index += 1
            else:
                pygame.mixer.Sound.play(SOUND_KEYPAD_WRONG)
                last_key_wrong = True

        return new_text_blink, new_text_scroll, current_index, last_key_wrong

    def handle_game_result_event(self, event, result_text_scroll, result_text_blink, current_index, last_key_wrong):
        result_text_scroll = None
        if event.type == pygame.QUIT:
            self.state.run_game_result, self.state.APP_RUN = False, False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                result_text_scroll = "UP"
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                # You might need to modify this to return or handle result_text_scroll if necessary
                draw_menu_results(result_text_scroll,
                                  self.maxtime_chrono, self.wpm, mode="MOD_CHRONO")

            elif event.key == pygame.K_DOWN:
                result_text_scroll = "DOWN"
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                # You might need to modify this to return or handle result_text_scroll if necessary
                draw_menu_results(result_text_scroll,
                                  self.maxtime_chrono, self.wpm, mode="MOD_CHRONO")

            elif event.key == pygame.K_RETURN:
                if RESULTS_MENU_SELECTED == linkedback_to_menu:
                    pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                    self.state.run_menu = True
                    self.state.run_game = False
                    self.state.run_game_result = False
                    self.state.INIT_MENU = False

                elif RESULTS_MENU_SELECTED == linked_save_results:
                    pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                    self.state.run_menu = True
                    self.state.run_game = False
                    self.state.run_game_result = False
                    self.state.INIT_MENU = False

        return result_text_scroll, result_text_blink, current_index, last_key_wrong


def main():
    state = GameState()
    bg_manager = BackgroundManager()
    text_manager = TextManager()
    ui_manager = UIManager(WIN)
    event_handler = EventHandler(state, text_manager, bg_manager, ui_manager)
    pygame.mixer.music.set_volume(0.05)

    clock = pygame.time.Clock()
    text_blink = 0
    wpm = str(0)
    text_scroll = None
    result_text_scroll = None
    current_index = 0
    last_key_wrong = False
    test_letter = KeyPressResponse.NO_TEST

    while state.APP_RUN:
        clock.tick(FPS)

        for event in pygame.event.get():
            text_blink, text_scroll, current_index, last_key_wrong = event_handler.handle_event(
                event, text_blink, text_scroll, current_index, last_key_wrong)

        if state.run_menu:
            if state.INIT_MENU:
                state.INIT_MENU = False
            text_blink, text_scroll = draw_menu(text_blink, text_scroll, WIN)

        elif state.run_game:
            if state.INIT_MENU:
                last_key_wrong = False
                state.INIT_MENU = False
                state.time_start_game = pygame.time.get_ticks()
                bg_manager.set_right()
                bg_manager.display()

                current_index = 0
                font = pygame.freetype.Font(
                    os.path.join("fonts", "Helvetica.ttf"), 50)
                font.origin = True
                # let's calculate how big the entire line of text is
                text_surf_rect = font.get_rect(text_manager.current_text)
                text_surf_rect.size = (
                    text_surf_rect.size[0] * 1.1,
                    text_surf_rect.size[1],
                )  # todo plus élégant
                text_surf_background_rect = font.get_rect(
                    text_manager.current_text)
                text_surf_background_rect.size = (
                    text_surf_rect.width * 1.15,
                    text_surf_rect.height * 1.7,
                )

                text_surf_background_rect.center = WIN.get_rect().center
                text_surf_rect.center = WIN.get_rect().center
                # calculate the width (and other stuff) for each letter of the text

            if text_manager.is_current_text_finished(current_index):
                # if the sentence is complete, let's prepare the  next surface
                current_index = 0
                text_manager.next_text_set()
                text_surf_rect = font.get_rect(text_manager.current_text)
                test_letter = 0

            ui_manager.display_wpm(wpm)

            ui_manager.draw_current_text(
                font, text_manager, current_index, test_letter, last_key_wrong)

            ui_manager.display_next_text(text_manager.next_text)

            if state.MOD_CHRONO:
                chrono_ended = display_remaining_time(
                    state.time_start_game, max_time=event_handler.maxtime_chrono)
                if chrono_ended:
                    state.run_game_result = True
                    state.run_game = False

            pygame.display.update()

            test_letter, last_key_wrong, current_index = event_handler.handle_key_press_event(
                text_manager.current_text, current_index, last_key_wrong
            )

        elif state.run_game_result:
            result_text_scroll = draw_menu_results(
                result_text_scroll, event_handler.maxtime_chrono, wpm, mode="MOD_CHRONO")


if __name__ == "__main__":
    main()
