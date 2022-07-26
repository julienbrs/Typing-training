# pylint: disable=no-member
from matplotlib.pyplot import text
import pygame
import pygame.freetype
pygame.freetype.init()
import sys
import os
from itertools import cycle
import dico
import time

pygame.font.init()
pygame.mixer.init()
FPS = 240

WIN_SIZE = WIDTH, HEIGHT = 1500, 844
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Training")



SOUND_KEYPAD = pygame.mixer.Sound(
    os.path.join('assets', 'sound_effects', 'keypad.mp3')
)
SOUND_KEYPAD_WRONG = pygame.mixer.Sound(
    os.path.join('assets', 'sound_effects', 'wrong.wav')
)


# LOADING SCREEN
IMG_BACKGROUND_LOADING_SCREEN   = pygame.image.load(os.path.join("./assets/yellow_duck_wp.jpg"))

#IMG_TEST                        = pygame.image.load(os.path.join("./assets/yellow_wallpaper.jpg"))
IMG_BACKGROUND_GAME_RIGHT       = pygame.image.load(os.path.join("./assets/yellow_wallpaper_right.jpg"))
IMG_BACKGROUND_GAME_WRONG       = pygame.image.load(os.path.join("./assets/yellow_wallpaper_wrong.jpg"))



WHITE   = (255, 255, 255)
LIGHT_BLUE = (167, 190, 211)
YELLOW_ORANGE = (253, 184, 19)
LIGHT_PURPLE = (153, 93, 206)
GREY    = (125, 125, 125)
LIGHT_GREY = (175, 175, 175)
GREEN = (3, 221, 94)

FONT_HELVETICA  = pygame.font.SysFont("helvetica", 40)
FONT_ARABOTO_50  = pygame.font.SysFont("haraboto", 50)
FONT_ARABOTO_80  = pygame.font.SysFont("haraboto", 80)

text_menu_welcome       = FONT_ARABOTO_80.render("Typing Session", 1, LIGHT_PURPLE)
text_menu_start_game    = FONT_ARABOTO_50.render("start a new session", 1, LIGHT_PURPLE)
text_menu_dictionnary   = FONT_ARABOTO_50.render("dictionnary (soon)", 1, LIGHT_PURPLE)
text_menu_leaderboard   = FONT_ARABOTO_50.render("progression (soon)", 1, LIGHT_PURPLE)




# todo: mettre "progression au lieu de leaderboard"




class LinkedText():
    "Class to link text for a menu"

    def __init__(self, x, y, next_text, prev_text):
        self.x = x
        self.y = y
        self.next_text = next_text
        self.prev_text = prev_text


    def draw(self, surface, text):
        "draw the text with line or not if selected"
        if self == MENU_SELECTED:
            new_size = (text.get_width() *1, text.get_height()*1)
            new_text = pygame.transform.scale(text, new_size)
            surface.blit(new_text, (self.x - new_text.get_width()/2,
                     self.y - new_text.get_height()/2))

            start_pos   = (self.x - new_text.get_width()/2, self.y + new_text.get_height() /2 )
            end_pos     = (self.x + new_text.get_width()/2, self.y + new_text.get_height() /2 )
            pygame.draw.line(surface, GREY,
                             start_pos, end_pos, width = int(text.get_height() * 0.08))

        else:
            surface.blit(text, (self.x - text.get_width()/2,
                     self.y - text.get_height()/2))

start_game  = LinkedText(WIDTH /2, HEIGHT /5, None, None)
dictionnary  = LinkedText(WIDTH /2, HEIGHT /3.5, None, start_game)
leaderboard = LinkedText(WIDTH /2, HEIGHT / 2.7, start_game, dictionnary)
dictionnary.next_text = leaderboard
start_game.next_text, start_game.prev_text = dictionnary, leaderboard
MENU_SELECTED = start_game


def draw_menu(text_blink, text_scroll, surface):
    "draw the start menu, text_scroll can be up, down or none"

    surface.blit(pygame.transform.scale(IMG_BACKGROUND_LOADING_SCREEN, WIN_SIZE), (0,0))

    text_blink = (text_blink + 1) % 350
    if text_blink <= 200 :
        surface.blit(text_menu_welcome,((WIDTH - text_menu_welcome.get_width())/2,
                    (HEIGHT/5 - text_menu_welcome.get_height())/2))

    start_game.draw(surface, text_menu_start_game)
    leaderboard.draw(surface, text_menu_leaderboard)
    dictionnary.draw(surface, text_menu_dictionnary)
    global MENU_SELECTED
    if text_scroll == "DOWN":
        MENU_SELECTED = MENU_SELECTED.next_text
        text_scroll = None

    elif text_scroll == "UP":
        MENU_SELECTED = MENU_SELECTED.prev_text
        text_scroll = None

    pygame.display.update()
    return text_blink, text_scroll


def wait(text_target, index):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == text_target[index]:
                    pygame.mixer.Sound.play(SOUND_KEYPAD)
                    return 2
                pygame.mixer.Sound.play(SOUND_KEYPAD_WRONG)
                return 1

def main():
    APP_RUN = True
    INIT_MENU = True
    run_menu = True
    global IMG_BACKGROUND_LOADING_SCREEN

    text_blink = 0
    wpm = str(0)
    text_scroll = None
    clock = pygame.time.Clock()
    data = cycle(dico.main("temp.txt", "dictionnary.txt")) #todo: shuffle
    current_text = next(data)
    pygame.mixer.music.load(os.path.join('assets','sound_effects', 'background_music.mp3'))
    pygame.mixer.music.play(-1)
    while APP_RUN:
        clock.tick(FPS)
        while run_menu:

            if INIT_MENU:
                INIT_MENU = False
                #pygame.mixer.music.load(os.path.join('assets','sound_effects', 'music', 'Menu_Screen.ogg'))
                #pygame.mixer.music.play(-1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_menu, APP_RUN = False, False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        text_scroll = "UP"
                        #pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        text_blink, text_scroll = draw_menu(text_blink - 1, text_scroll, WIN)

                    if event.key == pygame.K_DOWN:
                        text_scroll = "DOWN"
                        #pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        text_blink, text_scroll = draw_menu(text_blink - 1, text_scroll, WIN)



                    if event.key == pygame.K_RETURN and MENU_SELECTED == start_game:
                        #pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        run_menu = False
                        run_game = True
                        INIT_MENU = True

            text_blink, text_scroll = draw_menu(text_blink, text_scroll, WIN)

        while run_game:

            if INIT_MENU:
                INIT_MENU = False
                char_typed = 0
                test_letter = 0 #0 by default, 1 when test = wrong key, 2 = right key
                IMG_BACKGROUND_LOADING_SCREEN = IMG_BACKGROUND_GAME_RIGHT

                WIN.blit(pygame.transform.scale(IMG_BACKGROUND_LOADING_SCREEN, WIN_SIZE), (0,0))
                #draw_text_target(text_target, WIN)
                pygame.display.update()

                current_index = 0
                font = pygame.freetype.Font(os.path.join("fonts", "Helvetica.ttf"), 50)
                font.origin = True
                M_ADV_X = 4 #todo ??? Madv_x
                    # let's calculate how big the entire line of text is
                text_surf_rect = font.get_rect(current_text)
                text_surf_rect.size = (text_surf_rect.size[0]*1.1, text_surf_rect.size[1]) #todo plus élégant
                text_surf_background_rect = font.get_rect(current_text)
                text_surf_background_rect.size = (text_surf_rect.width * 1.15, text_surf_rect.height * 1.7)
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
                #todo gérer fin de phrase

            time_elapsed = max(time.time() - start_time, 1)
            wpm = str(round((char_typed / (time_elapsed / 60)) / 5))
            if current_index >= len(current_text) - 1:
                # if the sentence is complete, let's prepare the
                # next surface
                current_index = 0
                current_text = next(data)
                text_surf_rect = font.get_rect(current_text)
                baseline = text_surf_rect.y

                text_surf = pygame.Surface(text_surf_rect.size)
                text_surf_rect.center = text_surf_background_rect.center
                metrics = font.get_metrics(current_text)
                test_letter = 0

            if test_letter == 0 or test_letter == 2:
                WIN.blit(pygame.transform.scale(IMG_BACKGROUND_GAME_RIGHT, WIN_SIZE), (0,0))
            else:
                WIN.blit(pygame.transform.scale(IMG_BACKGROUND_GAME_WRONG, WIN_SIZE), (0,0))
            str_hud = "WPM : " + wpm
            text_wpm = FONT_ARABOTO_50.render(str_hud, 1, LIGHT_PURPLE)
            WIN.blit(text_wpm, (WIDTH/5, HEIGHT/4))
            #text_surf_background.fill('white')
            text_surf.fill(YELLOW_ORANGE)


            x = 0
            for (idx, (letter, metric)) in enumerate(zip(current_text, metrics)):
                # select the right color
                if idx == current_index:
                    if test_letter == 0:        # no test atm
                        color = 'lightblue'
                    elif test_letter == 1:      # test wrong key
                        color = 'red'
                    else:
                        color = 'GREEN'
                        current_index += 1
                        char_typed += 1
                        test_letter = 0
                elif idx < current_index:
                    color = 'GREEN'
                else:
                    color = (96, 81, 109)
                # render the single letter
                font.render_to(text_surf, (x, baseline), letter, color)
                # and move the start position
                x += metric[M_ADV_X]
            #text_surf_background.set_alpha(90)
            #WIN.blit(text_surf_background, text_surf_background_rect)
            WIN.blit(text_surf, text_surf_rect)
            pygame.display.update()

            pygame.event.clear()
            test_letter = wait(current_text, current_index)




if __name__ == "__main__":
    main()
