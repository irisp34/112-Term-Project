# creates a dictionary of the actions that the player can gain points from and 
# sums all the points to be constantly updated as the player plays

import pygame
import numpy as np
import variables
from startScreen import *

# dictionary initialized which contains all the things the user can score points
# from 
pointsDict = dict()
pointsDict["trees collected"] = 0
pointsDict["iron collected"] = 0
pointsDict["enemies killed"] = 0
pointsDict["bridges built"] = 0
pointsDict["hammers created"] = 0
pointsDict["farms built"] = 0
pointsDict["factories built"] = 0

# weights the score calculation of a certain action and returns the total score
def calculateScore():
    treePoints = pointsDict["trees collected"] * 2
    ironPoints = pointsDict["iron collected"] * 2
    enemyPoints = pointsDict["enemies killed"] * 10
    bridgePoints = pointsDict["bridges built"] * 15
    hammerPoints = pointsDict["hammers created"] * 3
    farmPoints = pointsDict["farms built"] * 20
    factoryPoints = pointsDict["factories built"] * 25
    allPoints = (treePoints + ironPoints + enemyPoints + bridgePoints + hammerPoints
        + farmPoints + factoryPoints)
    return allPoints

# finds the current score and draws this score on the screen
def displayScore():
    score = calculateScore()
    pygame.draw.rect(screen, (163, 196, 220), (20, 20, 120, 100))
    pygame.draw.rect(screen, (0, 52, 114), (20, 20, 120, 100), 4)
    caption = f"Score: {score}"
    textCenterX = 70
    textCenterY = 60
    createText(caption, textCenterX, textCenterY, 18)