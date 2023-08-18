import pygame
import pygame.freetype
import sys
from .constants import WIN, SOUND_KEYPAD, SOUND_KEYPAD_WRONG, SOUND_SELECT_MENU, start_game, progression_link, dictionnary, linkedback_to_menu, linked_save_results, KeyPressResponse
from .uimanager import draw_menu, draw_menu_results
from .gamestate import GameState
from .track_record import write_record_to_file, save_wpm_results


class EventHandler:
    def __init__(self, state, text_manager, background_manager, ui_manager):
        self.state = state
        self.text_manager = text_manager
        self.background_manager = background_manager
        self.ui_manager = ui_manager
        self.maxtime_chrono = 2500

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

    def handle_event(self, event, current_index=0, last_key_wrong=False):
        if self.state.gamestate == GameState.MAIN_MENU:
            return self._handle_menu_event(event,  current_index, last_key_wrong)
        elif self.state.gamestate == GameState.IN_GAME:
            return self._handle_game_event(event,  self.text_manager.current_text, current_index, last_key_wrong)
        elif self.state.gamestate == GameState.RESULTS_MENU:
            return self.handle_game_result_event(event,  current_index, last_key_wrong)
        else:
            return current_index, last_key_wrong

    def _handle_menu_event(self, event,  current_index, last_key_wrong):
        if event.type == pygame.QUIT:
            self.state.APP_RUN = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                draw_menu(self.state, WIN)
                self.state.main_menu_selected = self.state.main_menu_selected.prev_text

            elif event.key == pygame.K_DOWN:
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                draw_menu(self.state, WIN)
                self.state.main_menu_selected = self.state.main_menu_selected.next_text

            elif event.key == pygame.K_RETURN and self.state.main_menu_selected == start_game:
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                self.state.gamestate = GameState.IN_GAME
                self.state.should_init_menu = True

            elif event.key == pygame.K_RETURN and self.state.main_menu_selected == progression_link:
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                save_wpm_results()


            elif event.key == pygame.K_RETURN and self.state.main_menu_selected == dictionnary:
                pygame.mixer.Sound.play(SOUND_KEYPAD_WRONG)
        return current_index, last_key_wrong

    def _handle_game_event(self, event,  text_target, current_index, last_key_wrong):
        # Return these by default if no events change them

        if event.type == pygame.QUIT:
            self.state.APP_RUN = False

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_CAPSLOCK):
                return current_index, last_key_wrong

            if event.unicode == text_target[current_index]:
                pygame.mixer.Sound.play(SOUND_KEYPAD)
                last_key_wrong = False
                current_index += 1
            else:
                pygame.mixer.Sound.play(SOUND_KEYPAD_WRONG)
                last_key_wrong = True
        return current_index, last_key_wrong

    def handle_game_result_event(self, event,  current_index, last_key_wrong):
        if event.type == pygame.QUIT:
            self.state.APP_RUN = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                self.state.results_menu_selected = self.state.results_menu_selected.prev_text
                draw_menu_results(self.maxtime_chrono,  gamestate=self.state)

            elif event.key == pygame.K_DOWN:
                self.state.results_menu_selected = self.state.results_menu_selected.next_text
                pygame.mixer.Sound.play(SOUND_SELECT_MENU)

                draw_menu_results(self.maxtime_chrono,  gamestate=self.state)

            elif event.key == pygame.K_RETURN:
                if self.state.results_menu_selected == linkedback_to_menu:
                    pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                    self.state.gamestate = GameState.MAIN_MENU

                elif self.state.results_menu_selected == linked_save_results:
                    pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                    write_record_to_file(self.state.wpm)
                    save_wpm_results()
                    self.state.gamestate = GameState.MAIN_MENU
        return current_index, last_key_wrong
