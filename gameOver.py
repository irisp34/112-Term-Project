import pygame
import numpy as np
from variables import *
from startScreen import *
import score

def drawGameOver():
    pygame.draw.rect(screen, (163, 196, 220), (width // 4, 100, width // 2, 
        height - 200))
    pygame.draw.rect(screen, (0, 52, 114), (width // 4, 100, width // 2, 
        height - 200), 4)
    textCenterX = width / 2
    textCenterY = 100
    createText("Game Over", textCenterX, textCenterY, 40)
    textCenterY += 60
    totalScore = score.calculateScore()
    createText(f"Total Score: {totalScore}", textCenterX, textCenterY, 30)
    textCenterY += 60
    createText("Summary:", textCenterX, textCenterY, 30)
    for key in score.pointsDict:
        textCenterY += 40
        caption = f"{key[0].upper() + key[1:]}: {score.pointsDict[key]}"
        createText(caption, textCenterX, textCenterY, 20)

    # font = pygame.font.Font('freesansbold.ttf', 40)
    # caption = "Game Over"
    # text = font.render(caption, True, (0, 0, 0))
    # textRect = text.get_rect()
    # textRect.centerx = width / 2
    # textRect.centery = 300
    # screen.blit(text, textRect)


