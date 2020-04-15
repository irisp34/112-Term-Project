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
        for yPixel in range(0, height, rect.height):
            water = Water(image, (xPixel, yPixel))
            waterSprites.add(water)
            
def drawIslandBase(blockArray):
    pointsLeft, pointsRight = findIslandBasePoints(blockArray)
    # color picked from here: https://htmlcolorcodes.com/color-picker/
    pygame.draw.polygon(screen, (204, 179, 90), pointsLeft, 5)
    pygame.draw.polygon(screen, (255, 0, 255), pointsRight, 5)
    
def scrollIslands(blockArray, scrollX, scrollY, character):
    for row in range(blockArray.shape[0]):
        for col in range(blockArray.shape[1]):
            currBlock = blockArray[row, col]
            if (character.justMoved):
                currBlock.rect.x -= scrollX
                currBlock.rect.y -= scrollY

def scrollAll(blockArray1, blockArray2, scrollX, scrollY, character):
    # for sprite in waterSprites:
    #     if (character.justMoved):
    #         sprite.rect.x -= scrollX
    #         sprite.rect.y -= scrollY
    
    for sprite in charSprites:
        if (character.justMoved):
            sprite.rect.centerx -= scrollX
            sprite.rect.centery -= scrollY

    scrollIslands(blockArray1, scrollX, scrollY, character)
    scrollIslands(cartesianBlockArray1, scrollX, scrollY, character)
    scrollIslands(blockArray2, scrollX, scrollY, character)
    scrollIslands(cartesianBlockArray2, scrollX, scrollY, character)
    character.justMoved = False


def redrawAll(character):
    screen.fill((255, 255, 255))
    # screen.blit(background.image, background.rect)
    pygame.draw.rect(screen, (0, 255, 0),(200, 200, 50, 30))
    scrollX = character.scrollX
    scrollY = character.scrollY

    scrollAll(blockArray1, blockArray2, scrollX, scrollY, character)
    # for sprite in blockSprites1:
    #     if (character.justMoved):
    #         sprite.rect.x -= scrollX
    #         sprite.rect.y -= scrollY
    
    # for sprite in blockSprites2:
    #     if (character.justMoved):
    #         sprite.rect.x -= scrollX
    #         sprite.rect.y -= scrollY

    waterSprites.update()
    waterSprites.draw(screen)
    drawIslandBase(blockArray1)
    drawIslandBase(blockArray2)
    # screen.create_polygon(pointsLeft)
    blockSprites1.update()
    blockSprites1.draw(screen)
    blockSprites2.update()
    blockSprites2.draw(screen)
    charSprites.update()
    charSprites.draw(screen)
    pygame.display.flip()

def createIslands():
    # global startX
    # global startY
    global offsetX
    global offsetY
    # making 1st island
    print("drawing island 1")
    make2DBoard(blockSprites1, blockArray1, cartesianBlockArray1, blockRows, blockCols, cellWidth, 
                cellHeight, startX, startY, offsetX, offsetY)
    makeBoardIsometric(blockArray1)
    print("drawing island 2")
    
    offsetX += width // 2
    offsetY -= height // 3
    make2DBoard(blockSprites2, blockArray2, cartesianBlockArray2, blockRows, blockCols, cellWidth, 
                cellHeight, startX, startY, offsetX, offsetY)
    makeBoardIsometric(blockArray2)

def playGame():
    pygame.init()
    createIslands()
 
    # for row in range(cartesianBlockArray1.shape[0]):
    #     for col in range(cartesianBlockArray1.shape[1]):
    #         print("x,y", cartesianBlockArray1[row, col].rect.x, cartesianBlockArray1[row, col].rect.y)
    # print("in main", cartesianBlockArray1)

    # character picture from: https://ya-webdesign.com/imgdownload.html
    character = createCharacter("character.png", charSprites, cellWidth, cellHeight, blockArray1, cartesianBlockArray1)

    # water picture from: http://igm-tuto.blogspot.com/2014/06/pixel-art-draw-water-background.html
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
    
        redrawAll(character)
        
    pygame.quit()
    os._exit(0)


playGame()
