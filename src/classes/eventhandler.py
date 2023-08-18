import pygame
import pygame.freetype
import sys

from .constants import WIN, SOUND_KEYPAD, SOUND_KEYPAD_WRONG, SOUND_SELECT_MENU, MENU_SELECTED, start_game, linkedback_to_menu, linked_save_results, KeyPressResponse
from .uimanager import draw_menu, draw_menu_results
from .gamestate import GameMode


class EventHandler:
    def __init__(self, state, text_manager, background_manager, ui_manager):
        self.state = state
        self.text_manager = text_manager
        self.background_manager = background_manager
        self.ui_manager = ui_manager
        self.maxtime_chrono = 25000

    def handle_key_press_event(self, text_target, current_index, last_key_wrong):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_CAPSLOCK):
                    return KeyPressResponse.NO_ACTION, last_key_wrong, current_index

                if event.unicode == text_target[current_index]:
                    pygame.mixer.Sound.play(SOUND_KEYPAD)
                    self.background_manager.set_right()
                    last_key_wrong = False
                    current_index += 1
                    self.state.nb_char_typed += 1
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
                self.state.should_init_menu = True
        return text_blink, text_scroll, current_index, last_key_wrong

    def _handle_game_event(self, event, text_blink, text_scroll, text_target, current_index, last_key_wrong):
        # Return these by default if no events change them
        new_text_blink = text_blink
        new_text_scroll = text_scroll

        if event.type == pygame.QUIT:
            self.state.run_game = False
            self.state.APP_RUN = False

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_CAPSLOCK):
                return new_text_blink, new_text_scroll, current_index, last_key_wrong

            if event.unicode == text_target[current_index]:
                pygame.mixer.Sound.play(SOUND_KEYPAD)
                last_key_wrong = False
                current_index += 1
            else:
                pygame.mixer.Sound.play(SOUND_KEYPAD_WRONG)
                last_key_wrong = True

        return new_text_blink, new_text_scroll, current_index, last_key_wrong

    def handle_game_result_event(self, event, result_text_scroll, result_text_blink, current_index, last_key_wrong):
        if event.type == pygame.QUIT:
            self.state.run_game_result, self.state.APP_RUN = False, False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                result_text_scroll = "UP"
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                # You might need to modify this to return or handle result_text_scroll if necessary
                draw_menu_results(result_text_scroll,
                                  self.maxtime_chrono,  gamestate=self.state)

            elif event.key == pygame.K_DOWN:
                result_text_scroll = "DOWN"
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                # You might need to modify this to return or handle result_text_scroll if necessary
                draw_menu_results(result_text_scroll,
                                  self.maxtime_chrono,  gamestate=self.state)

            elif event.key == pygame.K_RETURN:
                if self.state.results_menu_selected == linkedback_to_menu:
                    pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                    self.state.run_menu = True
                    self.state.run_game = False
                    self.state.run_game_result = False
                    self.state.should_init_menu = False

                elif self.state.results_menu_selected == linked_save_results:
                    pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                    self.state.run_menu = True
                    self.state.run_game = False
                    self.state.run_game_result = False
                    self.state.should_init_menu = False

            if result_text_blink is None:
                result_text_blink = 0

        return result_text_blink, result_text_scroll, current_index, last_key_wrong
