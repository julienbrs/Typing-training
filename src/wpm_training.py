# pylint: disable=no-member
# pylint: disable=W0603     disable global variable warning

import pygame
import pygame.freetype
import os
from classes.gamestate import GameState, GameMode
from classes.backgroundmanager import BackgroundManager
from classes.textmanager import TextManager
from classes.uimanager import UIManager, draw_menu, draw_menu_results, display_remaining_time
from classes.eventhandler import EventHandler

# imports from constants module
from classes.constants import *

# Initialize Pygame modules
pygame.freetype.init()
pygame.font.init()
pygame.mixer.init()


def main():
    state = GameState()
    bg_manager = BackgroundManager()
    text_manager = TextManager()
    ui_manager = UIManager(WIN)
    event_handler = EventHandler(state, text_manager, bg_manager, ui_manager)
    pygame.mixer.music.set_volume(0.05)

    clock = pygame.time.Clock()
    text_blink = 0
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
            if state.should_init_menu:
                state.nb_char_typed = 0
                state.time_elapsed = 0.0001
                state.should_init_menu = False
            text_blink, text_scroll = draw_menu(text_blink, text_scroll, WIN)

        elif state.run_game:
            if state.should_init_menu:
                state.nb_char_typed = 0
                state.time_elapsed = 0.0001
                last_key_wrong = False
                state.should_init_menu = False
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
                test_letter = KeyPressResponse.CORRECT

            ui_manager.display_wpm(state)

            ui_manager.draw_current_text(
                font, text_manager, current_index, test_letter, last_key_wrong)

            ui_manager.display_next_text(text_manager.next_text)

            if state.game_mode == GameMode.CHRONO:
                is_chrono_ended = display_remaining_time(
                    state, max_time=event_handler.maxtime_chrono)
                if is_chrono_ended:
                    state.run_game_result = True
                    state.run_game = False

            pygame.display.update()

            test_letter, last_key_wrong, current_index = event_handler.handle_key_press_event(
                text_manager.current_text, current_index, last_key_wrong
            )

        elif state.run_game_result:
            result_text_scroll = draw_menu_results(
                result_text_scroll, event_handler.maxtime_chrono, gamestate=state)
        
        elif state.run_dictionnary_menu:
            print("dictionnary menu")


if __name__ == "__main__":
    main()
