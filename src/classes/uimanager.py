from .constants import *
from .gamestate import GameMode


def blit_text_to_window(text, position):
    WIN.blit(text, position)


def display_remaining_time(state, max_time):
    time_atm = pygame.time.get_ticks()
    time_elapsed = time_atm - state.time_start_game
    state.time_elapsed = time_elapsed
    time = round((max_time - time_elapsed) / 1000, 1)
    if time < 0:
        str_time = "0s"
    else:
        str_time = str(time) + "s"
    text_time = FONT_ARABOTO_50.render(str_time, 1, DARK_PURPLE)
    blit_text_to_window(
        text_time, (WIDTH * 0.95 - text_time.get_width(), HEIGHT * 0.18))

    if max_time - time_elapsed <= 0:
        return True
    return False


def update_menu_selection(menu_selected, text_scroll):
    if text_scroll == "DOWN":
        menu_selected = menu_selected.next_text
        text_scroll = None
    elif text_scroll == "UP":
        menu_selected = menu_selected.prev_text
        text_scroll = None
    return menu_selected, text_scroll


def draw_text_center(surface, text, x_ratio, y_ratio):
    surface.blit(
        text,
        (
            x_ratio * WIDTH - text.get_width() / 2,
            y_ratio * HEIGHT - text.get_height() / 2,
        ),
    )


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


def draw_menu_results(text_scroll, maxtime_chrono, gamestate):
    wpm = gamestate.calculate_wpm()
    WIN.blit(IMG_BACKGROUND_RESULTS, (0, 0))
    str_results_mod = "Temps limité: " + \
        str(round(maxtime_chrono / 1000, 1)
            ) if (gamestate.game_mode == GameMode.CHRONO) else "Pas de temps indiqué"
    str_results_wpm = "Résultat: " + str(wpm)

    draw_text_center(WIN, FONT_ARABOTO_80.render(
        "Résultats", 1, DEEP_BLUE), 0.5, 0.25)
    draw_text_center(WIN, FONT_ARABOTO_50.render(
        str_results_mod, 1, DEEP_BLUE), 0.5, 0.37)
    draw_text_center(WIN, FONT_ARABOTO_50.render(
        str_results_wpm, 1, DEEP_BLUE), 0.5, 0.44)

    linked_save_results.draw(
        WIN, text_results_menu_save, gamestate.results_menu_selected)
    linkedback_to_menu.draw(
        WIN, text_results_menu_continue, gamestate.results_menu_selected)

    gamestate.results_menu_selected, text_scroll = update_menu_selection(
        gamestate.results_menu_selected, text_scroll)

    pygame.display.update()
    return text_scroll

def draw_dictionnary_menu(text_scroll, gamestate):
    WIN.blit(IMG_BACKGROUND_RESULTS, (0, 0))
    draw_text_center(WIN, FONT_ARABOTO_80.render(
        "Dictionnaire", 1, DEEP_BLUE), 0.5, 0.25)
    draw_text_center(WIN, FONT_ARABOTO_50.render(
        "Dictionnaire", 1, DEEP_BLUE), 0.5, 0.37)
    draw_text_center(WIN, FONT_ARABOTO_50.render(
        "Dictionnaire", 1, DEEP_BLUE), 0.5, 0.44)

    linked_save_results.draw(
        WIN, text_results_menu_save, gamestate.results_menu_selected)
    linkedback_to_menu.draw(
        WIN, text_results_menu_continue, gamestate.results_menu_selected)

    gamestate.results_menu_selected, text_scroll = update_menu_selection(
        gamestate.results_menu_selected, text_scroll)

    pygame.display.update()
    return text_scroll


class UIManager:
    def __init__(self, window):
        self.WIN = window

    def display_wpm(self, state):
        wpm = state.calculate_wpm()
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
        M_ADV_X = 4

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
                    text_surf_rect.y + text_surf_rect.height - 2,
                )
                end_pos = (
                    text_surf_rect.x + x + metric[M_ADV_X] - 5,
                    text_surf_rect.y + text_surf_rect.height - 2,
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
