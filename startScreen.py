import pygame
import numpy as np
import variables
from shopping import*

def drawStartScreen():
    pygame.draw.rect(screen, (163, 196, 220), (baseX, baseY, width - baseX * 2, 
        height - baseY * 2))
    pygame.draw.rect(screen, (0, 52, 114), (baseX, baseY, width - baseX * 2, 
        height - baseY * 2), 4)
    textCenterX = width // 2
    textCenterY = height // 2
    createText("Game Title", textCenterX, textCenterY, 40)
    drawStartButton()
    drawInstructionsButton()

def startButtonInfo():
    # pic from: http://pixelartmaker.com/art/6f07b2c253f4fd6
    startImage = pygame.image.load("startButton.png").convert_alpha()
    startButtonRect = startImage.get_rect()
    location = (int(startButtonRect.width * .4), int(startButtonRect.height * .4))
    startImage = pygame.transform.scale(startImage, location)
    startButtonRect = startImage.get_rect()
    startButtonRect.x = width // 2 - startButtonRect.width // 2
    startButtonRect.y = height - 260
    return startImage, startButtonRect

def drawStartButton():
    startImage, startButtonRect = startButtonInfo()
    screen.blit(startImage, (startButtonRect.x, startButtonRect.y))

def instructionsButtonInfo():
    # pic from: http://pixelartmaker.com/art/5ec3a229d482e70
    instructionsImage = pygame.image.load("instructionsButton.png").convert_alpha()
    instructionsButtonRect = instructionsImage.get_rect()
    location = (int(instructionsButtonRect.width * .6),
        int(instructionsButtonRect.height * .6))
    instructionsImage = pygame.transform.scale(instructionsImage, location)
    instructionsButtonRect = instructionsImage.get_rect()
    if (variables.isSplashScreen):
        instructionsButtonRect.x = width // 2 - instructionsButtonRect.width // 2
        instructionsButtonRect.y = height - 185
        variables.startInstructionsButton = instructionsButtonRect
    else:
        instructionsButtonRect.x = width - 25 - instructionsButtonRect.width
        instructionsButtonRect.y = height - 185
        variables.mainInstructionsButton = instructionsButtonRect
    return instructionsImage, instructionsButtonRect

def drawInstructionsButton():
    instructionsImage, instructionsButtonRect = instructionsButtonInfo()
    screen.blit(instructionsImage, (instructionsButtonRect.x, instructionsButtonRect.y))

def backButtonInfo():
    # pic from: http://pixelartmaker.com/art/fe696dcfb337a49
    backImage = pygame.image.load("backButton.png").convert_alpha()
    backButtonRect = backImage.get_rect()
    location = (int(backButtonRect.width * .4), int(backButtonRect.height * .4))
    backImage = pygame.transform.scale(backImage, location)
    backButtonRect = backImage.get_rect()
    backButtonRect.x = width // 2 - backButtonRect.width // 2
    backButtonRect.y = height - 210
    return backImage, backButtonRect

def drawBackButton():
    backImage, backButtonRect = backButtonInfo()
    screen.blit(backImage, (backButtonRect.x, backButtonRect.y))

def createText(caption, textCenterX, textCenterY, fontSize):
    font = pygame.font.Font('freesansbold.ttf', fontSize)
    text = font.render(caption, True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = textCenterX
    textRect.centery = textCenterY
    screen.blit(text, textRect)

def drawInstructionsScreen():
    pygame.draw.rect(screen, (163, 196, 220), (baseX, baseY, width - baseX * 2, 
        height - baseY * 2))
    pygame.draw.rect(screen, (0, 52, 114), (baseX, baseY, width - baseX * 2, 
        height - baseY * 2), 4)
    textCenterX = width // 2
    textCenterY = 300
    createText("Instructions", textCenterX, textCenterY - 50, 24)
    createText("Use arrow keys to move right, left, up, and down", textCenterX, 
        textCenterY, 24)
    createText("Click on trees to collect them", textCenterX, textCenterY + 50, 24)
    createText("Click on enemies to kill them", textCenterX, textCenterY + 100, 24)
    createText("Game over if you bump into them!", textCenterX, textCenterY + 150, 24)
    if (variables.mainInstructionsButton):
        drawExitButton()
    elif (variables.startInstructionsButton):
        drawBackButton()

def beginInstructionsScreen(event):
    instructionsImage, instructionsButtonRect = instructionsButtonInfo()
    posX, posY = event.pos
    instructionsMinX, instructionsMinY = instructionsButtonRect.x, instructionsButtonRect.y
    instructionsMaxX, instructionsMaxY = (instructionsButtonRect.bottomright[0],
    instructionsButtonRect.bottomright[1])
    isInInstructionsBounds = (posX >= instructionsMinX and posX <= instructionsMaxX 
        and posY >= instructionsMinY and posY <= instructionsMaxY)
    if (isInInstructionsBounds):
        variables.isInstructionsScreen = True
        variables.mainInstructionsButton = True

def endInstructionsScreen(event):
    exitImage, exitButtonRect = exitButtonInfo()
    backImage, backButtonRect = backButtonInfo()
    posX, posY = event.pos
    exitMinX, exitMinY = exitButtonRect.x, exitButtonRect.y
    exitMaxX, exitMaxY = (exitButtonRect.bottomright[0],
    exitButtonRect.bottomright[1])
    backMinX, backMinY = backButtonRect.x, backButtonRect.y
    backMaxX, backMaxY = (backButtonRect.bottomright[0],
    backButtonRect.bottomright[1])
    isInExitBounds = (posX >= exitMinX and posX <= exitMaxX 
        and posY >= exitMinY and posY <= exitMaxY)
    isInBackBounds = (posX >= backMinX and posX <= backMaxX 
        and posY >= backMinY and posY <= backMaxY)
    if (isInExitBounds and variables.mainInstructionsButton):
        variables.isInstructionsScreen = False
    elif (isInBackBounds and variables.startInstructionsButton):
        variables.isSplashScreen = True
        variables.isInstructionsScreen = False

def endStartScreen(event):
    startImage, startButtonRect = startButtonInfo()
    instructionsImage, instructionsButtonRect = instructionsButtonInfo()
    posX, posY = event.pos
    startMinX, startMinY = startButtonRect.x, startButtonRect.y
    startMaxX, startMaxY = startButtonRect.bottomright[0], startButtonRect.bottomright[1]
    instructionsMinX, instructionsMinY = instructionsButtonRect.x, instructionsButtonRect.y
    instructionsMaxX, instructionsMaxY = (instructionsButtonRect.bottomright[0],
        instructionsButtonRect.bottomright[1])
    isInStartBounds = (posX >= startMinX and posX <= startMaxX 
        and posY >= startMinY and posY <= startMaxY)
    isInInstructionsBounds = (posX >= instructionsMinX and posX <= instructionsMaxX 
        and posY >= instructionsMinY and posY <= instructionsMaxY)
    print("in instructiosn bound", isInInstructionsBounds)
    if (isInStartBounds):
        variables.isSplashScreen = False
    elif (isInInstructionsBounds):
        # print("set instructions to true")
        variables.isSplashScreen = False
        variables.isInstructionsScreen = True
        variables.startInstructionsButton = True
