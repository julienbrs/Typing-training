# pylint: disable=no-member
import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIN_SIZE = WIDTH, HEIGHT = 1200, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Training")


SOUND_SELECT_MENU = pygame.mixer.Sound(
    os.path.join('assets', 'sound_effects', 'menu.wav'))


# LOADING SCREEN
IMG_BACKGROUND_LOADING_SCREEN   = pygame.image.load(os.path.join("./assets/ciel.jpg"))
IMG_TEST                        = pygame.image.load(os.path.join("./assets/ciel2.jpg"))




WHITE   = (255, 255, 255)
GREY    = (125, 125, 125)
LIGHT_GREY = (175, 175, 175)

FONT_MENU_START = pygame.font.SysFont("comicsans", 55)
FONT_MENU_LOADING_SCREEN = pygame.font.SysFont("comicsans", 120)

text_menu_welcome       = FONT_MENU_LOADING_SCREEN.render("TYPING TRAINING", 1, LIGHT_GREY)
text_menu_start_game    = FONT_MENU_START.render("Start a new session", 1, GREY)
text_menu_dictionnary   = FONT_MENU_START.render("Dictionnary", 1, GREY)
text_menu_leaderboard   = FONT_MENU_START.render("Leaderboard", 1, GREY)


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
            new_size = (text.get_width() *1.8, text.get_height()*1.8)
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

start_game  = LinkedText(WIDTH /2, HEIGHT /2, None, None)
dictionnary  = LinkedText(WIDTH /2, HEIGHT /1.5, None, start_game)
leaderboard = LinkedText(WIDTH /2, HEIGHT / 1.3, start_game, dictionnary)
dictionnary.next_text = leaderboard
start_game.next_text, start_game.prev_text = dictionnary, leaderboard
MENU_SELECTED = start_game


def draw_menu(text_blink, text_scroll, surface):
    "draw the start menu, text_scroll can be up, down or none"

    surface.blit(pygame.transform.scale(IMG_BACKGROUND_LOADING_SCREEN, WIN_SIZE), (0,0))

    text_blink = (text_blink + 1) % 1000
    if text_blink <= 500 :
        surface.blit(text_menu_welcome,((WIDTH - text_menu_welcome.get_width())/2,
                    (HEIGHT/3 - text_menu_welcome.get_height())/2))

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

def draw_test_game(text_blink, text_scroll, surface):
    "draw the game test"

    surface.blit(pygame.transform.scale(IMG_BACKGROUND_LOADING_SCREEN, WIN_SIZE), (0,0))

    text_blink = (text_blink + 1) % 1000
    if text_blink <= 500 :
        surface.blit(text_menu_welcome,((WIDTH - text_menu_welcome.get_width())/2,
                    (HEIGHT/3 - text_menu_welcome.get_height())/2))

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

def main():
    APP_RUN = True
    INIT_MENU = True
    run_menu = True
    global IMG_BACKGROUND_LOADING_SCREEN

    text_blink = 0
    text_scroll = None
    while APP_RUN:
        while run_menu:

            if INIT_MENU:
                INIT_MENU = False
                pygame.mixer.music.load(os.path.join('assets','sound_effects', 'music', 'Menu_Screen.ogg'))
                pygame.mixer.music.play(-1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_menu, APP_RUN = False, False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        text_scroll = "UP"
                        pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        text_blink, text_scroll = draw_menu(text_blink - 1, text_scroll, WIN)

                    if event.key == pygame.K_DOWN:
                        text_scroll = "DOWN"
                        pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        text_blink, text_scroll = draw_menu(text_blink - 1, text_scroll, WIN)



                    if event.key == pygame.K_RETURN and MENU_SELECTED == start_game:
                        pygame.mixer.Sound.play(SOUND_SELECT_MENU)
                        run_menu = False
                        run_game = True
                        INIT_MENU = True

            text_blink, text_scroll = draw_menu(text_blink, text_scroll, WIN)

        while run_game:

            if INIT_MENU:
                INIT_MENU = False
                IMG_BACKGROUND_LOADING_SCREEN = IMG_TEST
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game, APP_RUN = False, False
                    INIT_MENU = True



if __name__ == "__main__":
    main()
