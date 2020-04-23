import pygame
import numpy as np
from variables import *

def drawGameOver():
    pygame.draw.rect(screen, (163, 196, 220), (width // 4, 100, width // 2, 
        height - 200))
    pygame.draw.rect(screen, (0, 52, 114), (width // 4, 100, width // 2, 
        height - 200), 4)
    font = pygame.font.Font('freesansbold.ttf', 40)
    caption = "Game Over"
    text = font.render(caption, True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = width / 2
    textRect.centery = 300
    screen.blit(text, textRect)
