# main while loop which starts the game 
import pygame
import os
import numpy as np
from island import *
from character import *
from variables import *

class Water(pygame.sprite.Sprite):
    def __init__(self, image, location):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        # self.rect.x, self.rect.y = location

def createWater(waterSprites, image, rect):
    rect.width, rect.height = rect[2], rect[3]
    for xPixel in range(0, width, rect.width):
        for yPixel in range(int(height/2), height, rect.height):
            water = Water(image, (xPixel, yPixel))
            waterSprites.add(water)

def redrawAll():
    screen.fill((255, 255, 255))
    # screen.blit(background.image, background.rect)
    pygame.draw.rect(screen, (0, 255, 0),(200, 200, 50, 30))


    waterSprites.update()
    waterSprites.draw(screen)
    pointsLeft, pointsRight = findIslandBasePoints(blockArray)
    # print("left", pointsLeft)
    # print("right", pointsRight)
    # color picked from here: https://htmlcolorcodes.com/color-picker/
    pygame.draw.polygon(screen, (204, 179, 90), pointsLeft, 5)
    pygame.draw.polygon(screen, (255, 0, 255), pointsRight, 5)
    blockSprites.update()
    blockSprites.draw(screen)
    charSprites.update()
    charSprites.draw(screen)
    pygame.display.flip()

def playGame():
    pygame.init()
    make2DBoard(blockSprites, blockArray, cartesianBlockArray, blockRows, blockCols, cellWidth, 
                cellHeight, startX, startY)
    # global cartesianBlockArray
    # cartesianBlockArray = np.copy(blockArray)
 
    change(cartesianBlockArray)
    for row in range(cartesianBlockArray.shape[0]):
        for col in range(cartesianBlockArray.shape[1]):
            print("x,y", cartesianBlockArray[row, col].rect.x, cartesianBlockArray[row, col].rect.y)
    # print("in main", cartesianBlockArray)
    makeBoardIsometric(blockArray)
    # for row in range(cartesianBlockArray.shape[0]):
    #     for col in range(cartesianBlockArray.shape[1]):
    #         print("x,y", cartesianBlockArray[row, col].rect.x, cartesianBlockArray[row, col].rect.y)
    # character picture from: https://ya-webdesign.com/imgdownload.html
    character = createCharacter("character.png", charSprites, cellWidth, cellHeight, cartesianBlockArray)

    waterImage = pygame.image.load("water.png").convert_alpha()
    rect = waterImage.get_rect()
    createWater(waterSprites, waterImage, rect)

    clock = pygame.time.Clock()
    playing = True
    while playing:
        time = clock.tick(fps) # waits for next frame
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                playing = False
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                character.mousePressed(event)
                # character.jump(posX, posY)
            # elif (event.type == pygame.KEYDOWN):
            #     if (event.key == pygame.K_DOWN):
            #         character.moveDown()
            #     elif (event.key == pygame.K_UP):
            #         character.moveUp()
            #     elif (event.key == pygame.K_LEFT):
            #         character.moveLeft()
            #     elif (event.key == pygame.K_RIGHT):
            #         character.moveRight()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_DOWN]):
            character.moveDown()
        elif (keys[pygame.K_UP]):
            character.moveUp()
        elif (keys[pygame.K_RIGHT]):
            character.moveRight()
        elif (keys[pygame.K_LEFT]):
            character.moveLeft()
    
        redrawAll()
        
    pygame.quit()
    os._exit(0)


playGame()
