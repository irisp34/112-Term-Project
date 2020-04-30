# draws the game over page and calculates the final score. It also shows a 
# summary of all the things the user built and collected

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
    textCenterY = 200
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


