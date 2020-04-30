# draws all instruction screens and start screens and controls which buttons
# are drawn when (such as start vs continue buttons)
# also detects when the user clicks one of these buttons to end the splash screens

import pygame
import numpy as np
import variables
from shopping import*

# draws the start screen environment (background and buttons)
def drawStartScreen():
    pygame.draw.rect(screen, (163, 196, 220), (baseX, baseY, width - baseX * 2, 
        height - baseY * 2))
    pygame.draw.rect(screen, (0, 52, 114), (baseX, baseY, width - baseX * 2, 
        height - baseY * 2), 4)
    textCenterX = width // 2
    textCenterY = height // 2
    createText("Townlet Enigma", textCenterX, textCenterY, 40)
    if (variables.isNewGame):
        drawStartButton()
    else:
        drawContinueButton()
    drawInstructionsButton()

# image and rect information for the start button
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

# draws the start button on the screen
def drawStartButton():
    startImage, startButtonRect = startButtonInfo()
    screen.blit(startImage, (startButtonRect.x, startButtonRect.y))

def continueButtonInfo():
    # pic from: http://pixelartmaker.com/gallery?after=909575
    continueImage = pygame.image.load("continueButton.png").convert_alpha()
    continueButtonRect = continueImage.get_rect()
    location = (int(continueButtonRect.width * .4), int(continueButtonRect.height * .4))
    continueImage = pygame.transform.scale(continueImage, location)
    continueButtonRect = continueImage.get_rect()
    continueButtonRect.x = width // 2 - continueButtonRect.width // 2
    continueButtonRect.y = height - 260
    return continueImage, continueButtonRect

def drawContinueButton():
    continueImage, continueButtonRect = continueButtonInfo()
    screen.blit(continueImage, (continueButtonRect.x, continueButtonRect.y))

# draws the instructions button in different places depending on which screen
# the user is on
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
        instructionsButtonRect.y = height - 150
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

# generates appropriate text based on the caption, the center of the text, and
# the text size
def createText(caption, textCenterX, textCenterY, fontSize):
    font = pygame.font.Font('freesansbold.ttf', fontSize)
    text = font.render(caption, True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = textCenterX
    textRect.centery = textCenterY
    screen.blit(text, textRect)

# creates text for the instructions screen. It draws the back button if the user
# came from the start screen and the exit button if they are coming from the 
# main game screen
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
    createText("Tip: factories and farms will produce resources for you", 
        textCenterX, textCenterY + 200, 24)
    if (variables.mainInstructionsButton):
        drawExitButton()
    elif (variables.startInstructionsButton):
        drawBackButton()

# checks to see if a mouse click falls in the instructions rect
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

# checks to see if the user's mouse click should take them away from the
# instructions screen
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

# checks to see if the user's mouse click should take them away from the
# start screen
def endStartScreen(event):
    startImage, startButtonRect = startButtonInfo()
    instructionsImage, instructionsButtonRect = instructionsButtonInfo()
    continueImage, continueButtonRect = continueButtonInfo()
    posX, posY = event.pos
    startMinX, startMinY = startButtonRect.x, startButtonRect.y
    startMaxX, startMaxY = startButtonRect.bottomright[0], startButtonRect.bottomright[1]
    instructionsMinX, instructionsMinY = instructionsButtonRect.x, instructionsButtonRect.y
    instructionsMaxX, instructionsMaxY = (instructionsButtonRect.bottomright[0],
        instructionsButtonRect.bottomright[1])
    continueMinX, continueMinY = continueButtonRect.x, continueButtonRect.y
    continueMaxX, continueMaxY = continueButtonRect.bottomright[0], continueButtonRect.bottomright[1]
    isInStartBounds = (posX >= startMinX and posX <= startMaxX 
        and posY >= startMinY and posY <= startMaxY)
    isInInstructionsBounds = (posX >= instructionsMinX and posX <= instructionsMaxX 
        and posY >= instructionsMinY and posY <= instructionsMaxY)
    isInContinueBounds = (posX >= continueMinX and posX <= continueMaxX 
        and posY >= continueMinY and posY <= continueMaxY)
    if (isInInstructionsBounds):
        variables.isSplashScreen = False
        variables.isInstructionsScreen = True
        variables.startInstructionsButton = True
    elif (variables.isNewGame):
        if (isInStartBounds):
            variables.isSplashScreen = False
    else:
        if (isInContinueBounds):
            variables.isSplashScreen = False
    
