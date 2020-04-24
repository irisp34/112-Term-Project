# main while loop which starts the game 
import pygame
import os
import numpy as np
from island import *
from character import *
# from variables import *
import variables
from inventory import *
from water import *
from rawResources import *
from shopping import *
from bridge import *
from enemy import *
from gameOver import *
from startScreen import *

def resetScroll(character):
    character.scrollX = 0
    character.scrollY = 0
    character.cartScrollX = 0
    character.cartScrollY = 0

def scrollIslands(blockArray, scrollX, scrollY, character):
    for row in range(blockArray.shape[0]):
        for col in range(blockArray.shape[1]):
            currBlock = blockArray[row, col]
            if (character.justMoved):
                currBlock.rect.x -= scrollX
                currBlock.rect.y -= scrollY

def scrollSprites(character, spriteGroup, scrollX, scrollY):
    for sprite in spriteGroup:
        if (character.justMoved):
            sprite.rect.centerx -= scrollX
            sprite.rect.centery -= scrollY

def scrollAll(blockArray1, blockArray2, scrollX, scrollY, cartScrollX, cartScrollY, character):
    # for sprite in charSprites:
    #     if (character.justMoved):
    #         # print("before scroll", sprite.rect.centerx, sprite.rect.centery)
    #         sprite.rect.centerx -= scrollX
    #         sprite.rect.centery -= scrollY

    # for sprite in treeSprites:
    #     if (character.justMoved):
    #         sprite.rect.centerx -= scrollX
    #         sprite.rect.centery -= scrollY
    scrollSprites(character, charSprites, scrollX, scrollY)
    scrollSprites(character, treeSprites, scrollX, scrollY)
    scrollSprites(character, ironSprites, scrollX, scrollY)
    scrollSprites(character, bridgeSprites, scrollX, scrollY)
    scrollSprites(character, enemySprites, scrollX, scrollY)
    
    scrollIslands(blockArray1, scrollX, scrollY, character)
    # print("board bounds", getCartesianBoardBounds(cartesianBlockArray1))
    scrollIslands(cartesianBlockArray1, cartScrollX, cartScrollY, character)
    # print("board bounds after", getCartesianBoardBounds(cartesianBlockArray1))
    # print("blockArray2")
    scrollIslands(blockArray2, scrollX, scrollY, character)
    scrollIslands(cartesianBlockArray2, cartScrollX, cartScrollY, character)
    character.justMoved = False


def redrawAll(character):
    # global isShopping
    global drawOutline
    global drawUnaffordableMessage
    screen.fill((255, 255, 255))
    
    scrollX = character.scrollX
    scrollY = character.scrollY
    cartScrollX = character.cartScrollX
    cartScrollY = character.cartScrollY
    # print("scrollX scrollY", scrollX, scrollY)

    scrollAll(blockArray1, blockArray2, scrollX, scrollY, cartScrollX, cartScrollY, character)

    waterSprites.update()
    waterSprites.draw(screen)
    inventoryBarSprite.update(screen)
    inventoryBarSprite.draw(screen)
    resourceSprites.update(screen)
    resourceSprites.draw(screen)
    pygame.draw.rect(screen, (0, 255, 0),(200, 200, 50, 30))
    if (variables.isSplashScreen):
        drawStartScreen()
    elif (variables.isInstructionsScreen):
        drawInstructionsScreen()
    elif (variables.isGameOver):
        drawGameOver()
    # gameplay mode
    elif (not variables.isShopping):
        drawIslandBase(blockArray2)
        bridgeSprites.update()
        bridgeSprites.draw(screen)
        blockSprites2.update()
        blockSprites2.draw(screen)
        drawBlockBorders(blockArray2)
        drawIslandBase(blockArray1)
        blockSprites1.update()
        blockSprites1.draw(screen)
        drawBlockBorders(blockArray1)
        treeSprites.update()
        treeSprites.draw(screen)
        charSprites.update()
        charSprites.draw(screen)
        enemySprites.update()
        enemySprites.draw(screen)
        ironSprites.update()
        ironSprites.draw(screen)
        drawShopButton()
        drawInstructionsButton()
        # bridgeSprites.update()
        # bridgeSprites.draw(screen)
        for sprite in bridgeSprites:
            pygame.draw.polygon(screen, (255, 0, 255), (sprite.rect.topright, 
                sprite.rect.topleft, sprite.rect.bottomleft, sprite.rect.bottomright), 4)
        drawOutline = False
        drawUnaffordableMessage = False
        for sprite in charSprites:
            pygame.draw.polygon(screen, (155, 0, 255), (sprite.rect.topright, 
                sprite.rect.topleft, sprite.rect.bottomleft, sprite.rect.bottomright), 4)
        for sprite in enemySprites:
            pygame.draw.polygon(screen, (155, 0, 255), (sprite.rect.topright, 
                sprite.rect.topleft, sprite.rect.bottomleft, sprite.rect.bottomright), 4)
    # shop mode
    else:
        createShop()
        drawBuyButton()
        drawExitButton()
        # draws outline around selected item in shop
        if (drawOutline and keyword != None):
            minX, minY, maxX, maxY = purchasableItems[keyword]
            pygame.draw.rect(screen, (0, 52, 114), (minX, 
                minY, maxX - minX, maxY - minY), 4)
        if (drawUnaffordableMessage):
            minX, minY, maxX, maxY = purchasableItems[keyword]
            font = pygame.font.Font('freesansbold.ttf', 14)
            caption = "You can't afford this item"
            text = font.render(caption, True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.centerx = (minX + maxX) / 2
            textRect.centery = maxY + 30
            screen.blit(text, textRect)

    # adds resource caption only if there are resource sprites in the sprite group
    createInventoryCaptions(Wood)
    createInventoryCaptions(Iron)
    createInventoryCaptions(Hammer)

    # coordinates for first inventory box
    pygame.draw.rect(screen, (0, 255, 255),(265, 10, 90, 70), 3)
    pygame.display.flip()
    resetScroll(character)

def createInventoryCaptions(classType):
    text = None
    textRect = None
    for sprite in resourceSprites:
        currCount = 0
        # print("sprite amount", sprite.amount)
        if (isinstance(sprite, classType)):
            if (sprite.amount > currCount):
                currCount = sprite.amount
                text, textRect = sprite.addCaption()
    if (textRect != None and text != None):
        screen.blit(text, textRect)

def mousePressed(event, character, inventoryBar):
    # global isShopping
    global keyword
    global drawOutline
    global drawUnaffordableMessage
    print("clicked mouse pressed", event.pos)
    if (variables.isShopping):
        drawOutline, keyword, drawUnaffordableMessage = selectedItem(event, keyword)
        variables.isShopping = endShopping(event, keyword, inventoryBar)
        if (not variables.isShopping):
            keyword = None
            drawOutline = False
    elif (variables.isSplashScreen):
        endStartScreen(event)
    elif (variables.isInstructionsScreen):
        endInstructionsScreen(event)
    else:
        count = 1
        for sprite in treeSprites:
            # print("SPRITE #", count)
            if (sprite.removeTrees(event)):
                break
            count += 1
        character.killEnemy(event)
        variables.isShopping = beginShopping(event)
        beginInstructionsScreen(event)
    # return variables.isShopping

def playGame():
    # global isGameOver
    # global isShopping
    pygame.init()
    createIslands()

    # character picture from: https://ya-webdesign.com/imgdownload.html
    character = createCharacter("character.png", charSprites, cellWidth, 
        cellHeight, blockArray1, cartesianBlockArray1, offsetX1, offsetY1)
    enemyThread = createEnemies(character, charSprites, cellWidth, 
        cellHeight, blockArray1, cartesianBlockArray1, offsetX1, offsetY1)

    # water picture from: http://igm-tuto.blogspot.com/2014/06/pixel-art-draw-water-background.html
    waterImage = pygame.image.load("water.png").convert_alpha()
    rect = waterImage.get_rect()
    createWater(waterSprites, waterImage, rect)
    inventoryBar = Inventory()
    inventoryBarSprite.add(inventoryBar)
    makeTrees(character, blockArray1, cartesianBlockArray1, inventoryBar,
        offsetX1, offsetY1, cellWidth, cellHeight, 6)
    makeTrees(character, blockArray2, cartesianBlockArray2, inventoryBar,
      offsetX1, offsetY1, cellWidth, cellHeight, 5)
    createIronEvent = pygame.USEREVENT + 1
    createTreeEvent = pygame.USEREVENT + 2
    createEnemyEvent = pygame.USEREVENT + 3
    pygame.time.set_timer(createIronEvent, 2000)
    pygame.time.set_timer(createTreeEvent, 1000)
    pygame.time.set_timer(createEnemyEvent, 2000)

    clock = pygame.time.Clock()
    playing = True
    while playing:
        checkEnemyCollision(character, enemySprites)
        time = clock.tick(fps) # waits for next frame
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                playing = False
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                # character.jump(event)
                mousePressed(event, character, inventoryBar)
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
            if (event.type == createIronEvent):
                if (len(ironSprites) < 5):
                    placeIron(character, blockArray1, cartesianBlockArray1, 
                        inventoryBar, offsetX1, offsetY1, cellWidth, cellHeight)
            elif (event.type == createTreeEvent):
                # fix to spawn on specific island
                if (len(treeSprites) < 7):
                    count = 0
                    print("tree #", count)
                    makeTrees(character, blockArray1, cartesianBlockArray1, 
                        inventoryBar, offsetX1, offsetY1, cellWidth, cellHeight, 1)
                    count += 1
            elif (event.type == createEnemyEvent):
                if (len(enemySprites) == 0):
                    createEnemies(character, charSprites, cellWidth, cellHeight, 
                        blockArray1, cartesianBlockArray1, offsetX1, offsetY1)
            # elif (event.type == pygame.K_SPACE and isGameOver):
            #     print("HERE")
            #     isGameOver = False
            #     playing = False
            #     # playGame()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_DOWN]):
            character.moveDown()
            character.collectIron()
        elif (keys[pygame.K_UP]):
            character.moveUp()
            character.collectIron()
        elif (keys[pygame.K_RIGHT]):
            character.moveRight()
            character.collectIron()
        elif (keys[pygame.K_LEFT]):
            character.moveLeft()
            character.collectIron()
        # elif (keys[pygame.K_r] and isGameOver):
        #     print("HERE")
        #     isGameOver = False
        #     playing = False
    
        redrawAll(character)
    # print("???", isGameOver)
    # if (not isGameOver):
    #     print("here??")
    #     playGame()
    pygame.quit()
    os._exit(0)

# if (not isGameOver):
playGame()
