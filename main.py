# main while loop which starts the game 
import pygame
import os
import numpy as np
from island import *
from character import *
from variables import *
from inventory import *
from water import *
from trees import *

def resetScroll(character):
    character.scrollX = 0
    character.scrollY = 0
    character.cartScrollX = 0
    character.cartScrollY = 0


# draws the tan portion of the island with a border      
def drawIslandBase(blockArray):
    pointsLeft, pointsRight = findIslandBasePoints(blockArray)
    # color picked from here: https://htmlcolorcodes.com/color-picker/
    pygame.draw.polygon(screen, (204, 179, 90), pointsLeft)
    pygame.draw.polygon(screen, (204, 179, 90), pointsRight)
    pygame.draw.polygon(screen, (0, 0, 0), pointsRight, 2)
    pygame.draw.polygon(screen, (0, 0, 0), pointsLeft, 2)
    
def scrollIslands(blockArray, scrollX, scrollY, character):
    for row in range(blockArray.shape[0]):
        for col in range(blockArray.shape[1]):
            currBlock = blockArray[row, col]
            if (character.justMoved):
                currBlock.rect.x -= scrollX
                currBlock.rect.y -= scrollY

def scrollAll(blockArray1, blockArray2, scrollX, scrollY, cartScrollX, cartScrollY, character):
    # for sprite in waterSprites:
    #     if (character.justMoved):
    #         sprite.rect.x -= scrollX
    #         sprite.rect.y -= scrollY
    
    for sprite in charSprites:
        if (character.justMoved):
            # print("before scroll", sprite.rect.centerx, sprite.rect.centery)
            sprite.rect.centerx -= scrollX
            sprite.rect.centery -= scrollY

    for sprite in treeSprites:
        if (character.justMoved):
            sprite.rect.centerx -= scrollX
            sprite.rect.centery -= scrollY
    
    scrollIslands(blockArray1, scrollX, scrollY, character)
    # print("board bounds", getCartesianBoardBounds(cartesianBlockArray1))
    scrollIslands(cartesianBlockArray1, cartScrollX, cartScrollY, character)
    # print("board bounds after", getCartesianBoardBounds(cartesianBlockArray1))
    # print("blockArray2")
    scrollIslands(blockArray2, scrollX, scrollY, character)
    scrollIslands(cartesianBlockArray2, cartScrollX, cartScrollY, character)
    character.justMoved = False

# draws a border around each block
def drawBlockBorders(blockArray):
    for row in range(blockArray.shape[0]):
        for col in range(blockArray.shape[1]):
            block = blockArray[row, col]
            points = findGrassPoints(block)
            pygame.draw.polygon(screen, (0, 0, 0), points, 2)

def redrawAll(character):
    screen.fill((255, 255, 255))
    
    scrollX = character.scrollX
    scrollY = character.scrollY
    cartScrollX = character.cartScrollX
    cartScrollY = character.cartScrollY
    # print("scrollX scrollY", scrollX, scrollY)

    scrollAll(blockArray1, blockArray2, scrollX, scrollY, cartScrollX, cartScrollY, character)

    waterSprites.update()
    waterSprites.draw(screen)
    pygame.draw.rect(screen, (0, 255, 0),(200, 200, 50, 30))
    drawIslandBase(blockArray1)
    drawIslandBase(blockArray2)
    blockSprites1.update()
    blockSprites1.draw(screen)
    blockSprites2.update()
    blockSprites2.draw(screen)
    drawBlockBorders(blockArray1)
    drawBlockBorders(blockArray2)
    treeSprites.update()
    treeSprites.draw(screen)
    charSprites.update()
    charSprites.draw(screen)
    inventoryBarSprite.update(screen)
    inventoryBarSprite.draw(screen)
    resourceSprites.update(screen)
    resourceSprites.draw(screen)
    for sprite in resourceSprites:
        text, textRect = sprite.addCaption()
        screen.blit(text, textRect)
    # coordinates for first inventory box
    pygame.draw.rect(screen, (0, 255, 255),(265, 10, 90, 70), 3)
    pygame.display.flip()
    resetScroll(character)

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
    newOffsetX = offsetX + width // 2
    newOffsetY = offsetY - height // 3
    # offsetX += width // 2
    # offsetY -= height // 3
    make2DBoard(blockSprites2, blockArray2, cartesianBlockArray2, blockRows, blockCols, cellWidth, 
                cellHeight, startX, startY, newOffsetX, newOffsetY)
    makeBoardIsometric(blockArray2)

# makes Tree objects to place on the board
def makeTrees(character, blockArray, cartBlockArray, inventoryBar):
    for i in range(5):
        tree = Trees(character, blockArray, cartBlockArray, inventoryBar)
        treeSprites.add(tree)

def playGame():
    pygame.init()
    createIslands()

    # character picture from: https://ya-webdesign.com/imgdownload.html
    character = createCharacter("character.png", charSprites, cellWidth, cellHeight, blockArray1, cartesianBlockArray1)

    # water picture from: http://igm-tuto.blogspot.com/2014/06/pixel-art-draw-water-background.html
    waterImage = pygame.image.load("water.png").convert_alpha()
    rect = waterImage.get_rect()
    createWater(waterSprites, waterImage, rect)
    inventoryBar = Inventory()
    inventoryBarSprite.add(inventoryBar)
    makeTrees(character, blockArray1, cartesianBlockArray1, inventoryBar)
    # makeTrees(character, blockArray2, cartesianBlockArray2)

    clock = pygame.time.Clock()
    playing = True
    while playing:
        time = clock.tick(fps) # waits for next frame
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                playing = False
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                # character.mousePressed(event)
                count = 1
                for sprite in treeSprites:
                    print("SPRITE #", count)
                    if (sprite.removeTrees(event, offsetX, offsetY)):
                        break
                    count += 1
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
