# pylint: disable=no-member
# pylint: disable=W0603     disable global variable warning

import pygame
import pygame.freetype
import os
from classes.gamestate import GameState
from classes.backgroundmanager import BackgroundManager
from classes.textmanager import TextManager
from classes.uimanager import UIManager
from classes.eventhandler import EventHandler

# imports from constants module
from classes.constants import *

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
                font_path = os.path.join(os.path.dirname(
                    __file__), "assets", "fonts", "Helvetica.ttf")
                font = pygame.freetype.Font(font_path, 50)
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
