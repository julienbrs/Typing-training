# pylint: disable=no-member
from matplotlib.pyplot import text
import pygame
import pygame.freetype

pygame.freetype.init()
import sys
import os
from itertools import cycle
import manage_dictionnary
import time
import random

pygame.font.init()
pygame.mixer.init()
FPS = 240

WIN_SIZE = WIDTH, HEIGHT = 1500, 844
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Training")


SOUND_KEYPAD = pygame.mixer.Sound(os.path.join("assets", "sound_effects", "keypad.mp3"))
SOUND_KEYPAD.set_volume(0.08)

SOUND_KEYPAD_WRONG = pygame.mixer.Sound(
    os.path.join("assets", "sound_effects", "wrong.wav")
)
SOUND_KEYPAD_WRONG.set_volume(0.08)

SOUND_SELECT_MENU = pygame.mixer.Sound(
    os.path.join("assets", "sound_effects", "menu.wav")
)
SOUND_SELECT_MENU.set_volume(0.03)


# LOADING SCREEN
IMG_BACKGROUND_LOADING_SCREEN = pygame.image.load(
    os.path.join("./assets/yellow_duck_wp.jpg")
)

# IMG_TEST                        = pygame.image.load(os.path.join("./assets/yellow_wallpaper.jpg"))
IMG_BACKGROUND_GAME_RIGHT = pygame.image.load(
    os.path.join("./assets/yellow_wallpaper_right.jpg")
)
IMG_BACKGROUND_GAME_WRONG = pygame.image.load(
    os.path.join("./assets/yellow_wallpaper_wrong.jpg")
)
IMG_BACKGROUND_RESULTS = pygame.image.load(
    os.path.join("./assets/yellow_wp_results.jpg")
)


WHITE = (255, 255, 255)
LIGHT_BLUE = (167, 190, 211)
YELLOW_ORANGE = (253, 184, 19)
YELLOW_ORANGE_DARK = (158, 148, 115)
LIGHT_PURPLE = (7, 27, 130)  # todo changer nom (pas du prurple)
GREY = (125, 125, 125)
LIGHT_GREY = (175, 175, 175)
GREEN_RIGHT = (8, 160, 69)
DARK_PURPLE = (96, 81, 109)
RED_WRONG = (240, 83, 101)

FONT_HELVETICA = pygame.font.SysFont("helvetica", 40)
FONT_ARABOTO_50 = pygame.font.SysFont("haraboto", 50)
FONT_ARABOTO_80 = pygame.font.SysFont("haraboto", 80)


text_menu_welcome = FONT_ARABOTO_80.render("Typing Session", 1, LIGHT_PURPLE)
text_menu_start_game = FONT_ARABOTO_50.render("Start new session", 1, LIGHT_PURPLE)
text_menu_dictionnary = FONT_ARABOTO_50.render("Dictionnary (soon)", 1, LIGHT_PURPLE)
text_menu_leaderboard = FONT_ARABOTO_50.render("Progression (soon)", 1, LIGHT_PURPLE)
text_results_menu_save = FONT_ARABOTO_50.render("Save Results", 1, LIGHT_PURPLE)
text_results_menu_continue = FONT_ARABOTO_50.render("Continue", 1, LIGHT_PURPLE)


# todo: mettre "progression au lieu de leaderboard"


class LinkedText:
    "Class to link text for a menu"

    def __init__(self, x, y, next_text, prev_text, name=None):
        self.x = x
        self.y = y
        self.name = name
        self.next_text = next_text
        self.prev_text = prev_text

    def draw(self, surface, text, menu):
        "draw the text with line or not if selected"
        if self == menu:
            new_size = (text.get_width() * 1, text.get_height() * 1)
            new_text = pygame.transform.scale(text, new_size)
            surface.blit(
                new_text,
                (self.x - new_text.get_width() / 2, self.y - new_text.get_height() / 2),
            )

            start_pos = (
                self.x - new_text.get_width() / 2,
                self.y + new_text.get_height() / 2,
            )
            end_pos = (
                self.x + new_text.get_width() / 2,
                self.y + new_text.get_height() / 2,
            )
            pygame.draw.line(
                surface, GREY, start_pos, end_pos, width=int(text.get_height() * 0.08)
            )

        else:
            surface.blit(
                text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2)
            )


start_game = LinkedText(WIDTH / 2, HEIGHT / 3.6, None, None)
dictionnary = LinkedText(WIDTH / 2, HEIGHT / 2.7, None, start_game)
leaderboard = LinkedText(WIDTH / 2, HEIGHT / 2.2, start_game, dictionnary)
dictionnary.next_text = leaderboard
start_game.next_text, start_game.prev_text = dictionnary, leaderboard
MENU_SELECTED = start_game


linked_save_results = LinkedText(
    WIDTH / 2, HEIGHT * 0.6, None, None, "Save results"
)  # todo enlever .name
linkedback_to_menu = LinkedText(
    WIDTH / 2, HEIGHT * 0.67, linked_save_results, linked_save_results, "Back menu"
)
linked_save_results.next_text, linked_save_results.prev_text = (
    linkedback_to_menu,
    linkedback_to_menu,
)
RESULTS_MENU_SELECTED = linked_save_results


def draw_menu(text_blink, text_scroll, surface):
    "draw the start menu, text_scroll can be up, down or none"
    global MENU_SELECTED
    surface.blit(
        pygame.transform.scale(IMG_BACKGROUND_LOADING_SCREEN, WIN_SIZE), (0, 0)
    )

    text_blink = (text_blink + 1) % 350
    if text_blink <= 200:
        surface.blit(
            text_menu_welcome,
            (
                (WIDTH - text_menu_welcome.get_width()) / 2,
                (HEIGHT / 5 - text_menu_welcome.get_height()) / 2,
            ),
        )

    start_game.draw(surface, text_menu_start_game, MENU_SELECTED)
    leaderboard.draw(surface, text_menu_leaderboard, MENU_SELECTED)
    dictionnary.draw(surface, text_menu_dictionnary, MENU_SELECTED)

    if text_scroll == "DOWN":
        MENU_SELECTED = MENU_SELECTED.next_text
        text_scroll = None

    elif text_scroll == "UP":
        MENU_SELECTED = MENU_SELECTED.prev_text
        text_scroll = None

    pygame.display.update()
    return text_blink, text_scroll


def draw_menu_results(text_scroll, maxtime_chrono, wpm):
    global IMG_BACKGROUND_GAME  # todo img_bckground
    global RESULTS_MENU_SELECTED
    IMG_BACKGROUND_GAME = IMG_BACKGROUND_RESULTS
    WIN.blit(IMG_BACKGROUND_GAME, (0, 0))
    MOD_CHRONO = True  # todo MOD_CHRONO
    if MOD_CHRONO:
        str_results_mod = "Temps limité: " + str(round(maxtime_chrono / 1000, 1))
    else:
        str_results_mod = str("Pas de temps indiqué")
    str_results_wpm = "Résultat: " + str(wpm)

    text_results_title = FONT_ARABOTO_80.render("Résultats", 1, LIGHT_PURPLE)
    text_results_mod = FONT_ARABOTO_50.render(str_results_mod, 1, LIGHT_PURPLE)
    text_results_wpm = FONT_ARABOTO_50.render(str_results_wpm, 1, LIGHT_PURPLE)

    WIN.blit(
        text_results_title,
        (WIDTH * 0.5 - text_results_title.get_width() / 2, HEIGHT * 0.25),
    )
    WIN.blit(
        text_results_mod,
        (WIDTH * 0.5 - text_results_mod.get_width() / 2, HEIGHT * 0.37),
    )
    WIN.blit(
        text_results_wpm,
        (WIDTH * 0.5 - text_results_wpm.get_width() / 2, HEIGHT * 0.44),
    )

    linked_save_results.draw(WIN, text_results_menu_save, RESULTS_MENU_SELECTED)
    linkedback_to_menu.draw(WIN, text_results_menu_continue, RESULTS_MENU_SELECTED)

    if text_scroll == "DOWN":
        RESULTS_MENU_SELECTED = RESULTS_MENU_SELECTED.next_text
        text_scroll = None

    elif text_scroll == "UP":
        RESULTS_MENU_SELECTED = RESULTS_MENU_SELECTED.prev_text
        text_scroll = None

    pygame.display.update()
    return text_scroll


def wait(text_target, index, last_key_wrong):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.unicode == text_target[index]:
                pygame.mixer.Sound.play(SOUND_KEYPAD)
                last_key_wrong = False
                return 2, last_key_wrong
            pygame.mixer.Sound.play(SOUND_KEYPAD_WRONG)
            last_key_wrong = True
            return 1, last_key_wrong
    return 3, last_key_wrong


def display_chrono_training(time_start):
    time_atm = pygame.time.get_ticks()
    time_elapsed = time_atm - time_start
    str_time = str(round(time_elapsed / 1000, 1))
    text_time = FONT_ARABOTO_50.render(str_time, 1, DARK_PURPLE)
    WIN.blit(text_time, (WIDTH * 0.95 - text_time.get_width(), HEIGHT * 0.18))


def display_chrono_chrono(time_start, max_time):
    time_atm = pygame.time.get_ticks()
    time_elapsed = time_atm - time_start
    str_time = str(round((max_time - time_elapsed) / 1000, 1))
    text_time = FONT_ARABOTO_50.render(str_time, 1, DARK_PURPLE)
    WIN.blit(text_time, (WIDTH * 0.95 - text_time.get_width(), HEIGHT * 0.18))
    if max_time - time_elapsed <= 0:
        return True
    return False


def main():
    APP_RUN = True
    INIT_MENU = True
    run_menu = True
    MOD_CHRONO = True
    MOD_TRAINING = False
    run_game_result = False
    pygame.mixer.music.set_volume(0.05)
    IMG_BACKGROUND_GAME = IMG_BACKGROUND_GAME_RIGHT

    text_blink = 0
    wpm = str(0)
    text_scroll = None
    result_text_scroll = None
    clock = pygame.time.Clock()
    dictio = manage_dictionnary.main("temp.txt", "dictionnary.txt")
    data = cycle(dictio)  # todo: shuffle

    current_text = next(data)
    next_text = next(data)
    pygame.mixer.music.load(
        os.path.join("assets", "sound_effects", "background_music.mp3")
    )
    pygame.mixer.music.play(-1)
    while APP_RUN:
        clock.tick(FPS)
        while run_menu:

            if INIT_MENU:
                INIT_MENU = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_menu, APP_RUN = False, False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        text_scroll = "UP"
                        pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        text_blink, text_scroll = draw_menu(
                            text_blink - 1, text_scroll, WIN
                        )

                    if event.key == pygame.K_DOWN:
                        text_scroll = "DOWN"
                        pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        text_blink, text_scroll = draw_menu(
                            text_blink - 1, text_scroll, WIN
                        )

                    if event.key == pygame.K_RETURN and MENU_SELECTED == start_game:
                        pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        run_menu = False
                        run_game = True
                        INIT_MENU = True

            text_blink, text_scroll = draw_menu(text_blink, text_scroll, WIN)

        while run_game:

            if INIT_MENU:
                last_key_wrong = False
                INIT_MENU = False
                maxtime_chrono = 30000
                time_start_game = pygame.time.get_ticks()
                char_typed = 0
                test_letter = 0  # 0 by default, 1 when test = wrong key, 2 = right key
                IMG_BACKGROUND_GAME = IMG_BACKGROUND_GAME_RIGHT

                WIN.blit(pygame.transform.scale(IMG_BACKGROUND_GAME, WIN_SIZE), (0, 0))

                current_index = 0
                font = pygame.freetype.Font(os.path.join("fonts", "Helvetica.ttf"), 50)
                font.origin = True
                M_ADV_X = 4  # todo ??? Madv_x
                # let's calculate how big the entire line of text is
                text_surf_rect = font.get_rect(current_text)
                text_surf_rect.size = (
                    text_surf_rect.size[0] * 1.1,
                    text_surf_rect.size[1],
                )  # todo plus élégant
                text_surf_background_rect = font.get_rect(current_text)
                text_surf_background_rect.size = (
                    text_surf_rect.width * 1.15,
                    text_surf_rect.height * 1.7,
                )
                # in this rect, the y property is the baseline
                # we use since we use the origin mode
                baseline = text_surf_rect.y

                # now let's create a surface to render the text on
                # and center it on the screen
                text_surf = pygame.Surface(text_surf_rect.size)
                text_surf_background = pygame.Surface(text_surf_background_rect.size)

                text_surf_background_rect.center = WIN.get_rect().center
                text_surf_rect.center = WIN.get_rect().center
                # calculate the width (and other stuff) for each letter of the text
                metrics = font.get_metrics(current_text)
                start_time = time.time()
                # todo gérer fin de phrase

            time_elapsed = max(time.time() - start_time, 1)
            wpm = str(round((char_typed / (time_elapsed / 60)) / 5))
            # if test_letter !=3:
            if current_index >= len(current_text) - 1:
                # if the sentence is complete, let's prepare the
                # next surface
                current_index = 0
                current_text = next_text
                next_text = next(data)
                text_surf_rect = font.get_rect(current_text)
                baseline = text_surf_rect.y

                text_surf = pygame.Surface(text_surf_rect.size)
                text_surf_rect.center = text_surf_background_rect.center
                metrics = font.get_metrics(current_text)
                test_letter = 0

            if test_letter == 0 or test_letter == 2:
                IMG_BACKGROUND_GAME = pygame.transform.scale(
                    IMG_BACKGROUND_GAME_RIGHT, WIN_SIZE
                )
                WIN.blit(IMG_BACKGROUND_GAME, (0, 0))
            elif test_letter == 1:
                IMG_BACKGROUND_GAME = pygame.transform.scale(
                    IMG_BACKGROUND_GAME_WRONG, WIN_SIZE
                )
                WIN.blit(IMG_BACKGROUND_GAME, (0, 0))
            else:
                WIN.blit(IMG_BACKGROUND_GAME, (0, 0))

            str_hud = "WPM : " + wpm
            text_wpm = FONT_ARABOTO_50.render(str_hud, 1, DARK_PURPLE)
            WIN.blit(text_wpm, (WIDTH * 0.95 - text_wpm.get_width(), HEIGHT * 0.08))
            # text_surf_background.fill('white')
            text_surf.fill(YELLOW_ORANGE)

            x = 0
            for (idx, (letter, metric)) in enumerate(zip(current_text, metrics)):
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
                    if (
                        test_letter == 0 or test_letter == 3
                    ):  # means "no test atm", todo in method
                        if last_key_wrong:
                            color = RED_WRONG
                        else:
                            color = "lightblue"
                    elif test_letter == 1:  # test wrong key
                        color = RED_WRONG
                    elif test_letter == 2:
                        color = GREEN_RIGHT
                        current_index += 1
                        char_typed += 1
                        test_letter = 0
                    else:  # todo error mieux
                        print("ERROR")
                    color_line = color
                elif idx < current_index:
                    color = GREEN_RIGHT
                else:
                    color = DARK_PURPLE
                # render the single letter
                font.render_to(text_surf, (x, baseline), letter, color)
                # and move the start position
                x += metric[M_ADV_X]
            # text_surf_background.set_alpha(90)
            # WIN.blit(text_surf_background, text_surf_background_rect)
            WIN.blit(text_surf, text_surf_rect)
            pygame.draw.line(WIN, color_line, start_pos, end_pos, width=5)

            next_text_game = FONT_HELVETICA.render(next_text, 1, DARK_PURPLE)
            next_text_game.set_alpha(180)
            WIN.blit(
                next_text_game,
                (WIDTH * 0.5 - next_text_game.get_width() / 2, HEIGHT * 0.57),
            )

            if MOD_CHRONO:
                chrono_ended = display_chrono_chrono(
                    time_start_game, max_time=maxtime_chrono
                )
                if chrono_ended:
                    run_game_result = True
                    run_game = False

            pygame.display.update()

            test_letter, last_key_wrong = wait(
                current_text, current_index, last_key_wrong
            )

        while run_game_result:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game_result, APP_RUN = False, False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        result_text_scroll = "UP"
                        pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        result_text_scroll = draw_menu_results(
                            result_text_scroll, maxtime_chrono, wpm
                        )

                    if event.key == pygame.K_DOWN:
                        result_text_scroll = "DOWN"
                        pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        result_text_scroll = draw_menu_results(
                            result_text_scroll, maxtime_chrono, wpm
                        )

                    if (
                        event.key == pygame.K_RETURN
                        and RESULTS_MENU_SELECTED == linkedback_to_menu
                    ):
                        pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        run_menu = True
                        run_game = False
                        run_game_result = False
                        INIT_MENU = False

                    if (
                        event.key == pygame.K_RETURN
                        and RESULTS_MENU_SELECTED == linked_save_results
                    ):
                        pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        run_menu = True
                        run_game = False
                        run_game_result = False
                        INIT_MENU = False

            result_text_scroll = draw_menu_results(
                result_text_scroll, maxtime_chrono, wpm
            )


if __name__ == "__main__":
    main()
