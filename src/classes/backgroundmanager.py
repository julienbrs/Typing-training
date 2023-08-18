import pygame

from .constants import WIN_SIZE, IMG_BACKGROUND_GAME_RIGHT, IMG_BACKGROUND_GAME_WRONG, IMG_BACKGROUND_GAME_SIMPLE, WIN

class BackgroundManager:
    def __init__(self):
        self.IMG_BACKGROUND_GAME = IMG_BACKGROUND_GAME_RIGHT

    def set_wrong(self):
        self.IMG_BACKGROUND_GAME = pygame.transform.scale(
            IMG_BACKGROUND_GAME_WRONG, WIN_SIZE)

    def set_right(self):
        self.IMG_BACKGROUND_GAME = pygame.transform.scale(
            IMG_BACKGROUND_GAME_RIGHT, WIN_SIZE)
    
    def set_simple(self):
        self.IMG_BACKGROUND_GAME = pygame.transform.scale(
            IMG_BACKGROUND_GAME_SIMPLE, WIN_SIZE)

    def display(self):
        WIN.blit(self.IMG_BACKGROUND_GAME, (0, 0))
