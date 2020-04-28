# main while loop which starts the game 
import pygame
import os
import numpy as np
import pickle
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
from buildings import *
#from score import *
import score

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
    scrollSprites(character, buildingSprites, scrollX, scrollY)
    
    scrollIslands(blockArray1, scrollX, scrollY, character)
    # print("board bounds", getCartesianBoardBounds(cartesianBlockArray1))
    scrollIslands(cartesianBlockArray1, cartScrollX, cartScrollY, character)
    # print("board bounds after", getCartesianBoardBounds(cartesianBlockArray1))
    # print("blockArray2")
    scrollIslands(blockArray2, scrollX, scrollY, character)
    scrollIslands(cartesianBlockArray2, cartScrollX, cartScrollY, character)
    character.justMoved = False


def redrawAll(character):
    # print("redrawAll", variables.isSplashScreen, variables.isInstructionsScreen)
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
    variables.resourceSprites.update(screen)
    variables.resourceSprites.draw(screen)
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
        buildingSprites.update()
        buildingSprites.draw(screen)
        drawInstructionsButton()
        score.displayScore()

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
            print("main keyword", keyword)
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
        # print("in main", drawOutline, keyword, drawUnaffordableMessage)
        variables.isShopping = endShopping(event, keyword, inventoryBar)
        # print("right after end shopping", variables.isShopping)
        if (not variables.isShopping):
            keyword = None
            drawOutline = False
    elif (variables.isSplashScreen):
        endStartScreen(event)
    elif (variables.isInstructionsScreen):
        endInstructionsScreen(event)
    # elif(not variables.isInstructionsScreen and not variables.isSplashScreen
    #     and not variables.isShopping):
    #     beginInstructionsScreen(event)
    else:
        beginInstructionsScreen(event)
        count = 1
        for sprite in treeSprites:
            # print("SPRITE #", count)
            if (sprite.removeTrees(event)):
                break
            count += 1
        character.killEnemy(event)
        # print("testing begin shopping")
        variables.isShopping = beginShopping(event)
        beginInstructionsScreen(event)
    # return variables.isShopping

def bridgeCount():
    count = 0
    for sprite in variables.bridgeSprites:
        count += 1
    return count

def playGame():
    # global isGameOver
    # global isShopping
    pygame.init()
    createIslands()

    # water picture from: http://igm-tuto.blogspot.com/2014/06/pixel-art-draw-water-background.html
    waterImage = pygame.image.load("water.png").convert_alpha()
    rect = waterImage.get_rect()
    createWater(waterSprites, waterImage, rect)
    inventoryBar = Inventory()
    inventoryBarSprite.add(inventoryBar)
    # characterX = None
    # characterY = None
    characterPosition = None
    enemyPosition = None
    treeList1 = None
    treeList2 = None
    ironList1 = None
    ironList2 = None
    farmList = None

    # https://www.techcoil.com/blog/how-to-save-and-load-objects-to-and-from-file-in-python-via-facilities-from-the-pickle-module/
    if os.path.exists('resources.bin'):
        try:
            with open('resources.bin', 'rb') as resourcefile:
                resources = pickle.load(resourcefile)
                count = resources['wood']
                for i in range(count):
                    logImage = "log.png"
                    logResource = Wood(logImage, "Wood", 1, inventoryBar)
                    logResource.placeInInventory(0)
                    resourceSprites.add(logResource)
                    logResource.updateAmount(Wood)
                    variables.resourceSprites.add(logResource)

                count = resources['iron']
                for i in range(count):
                    ironImage = "metalBar.png"
                    ironResource = Iron(ironImage, "Iron", 2, inventoryBar)
                    ironResource.placeInInventory(1)
                    resourceSprites.add(ironResource)
                    ironResource.updateAmount(Iron)

                count = resources['hammer']
                for i in range(count):
                    hammer = Hammer("hammer.png", "hammer", 1, inventoryBar)
                    resourceSprites.add(hammer)
                    hammer.placeInInventory(2)
                    hammer.updateAmount(Hammer)

                count = resources['bridge']
                for i in range(count):
                    bridge = Bridge(bridgeDict, cellWidth, cellHeight, blockArray1,
                        cartesianBlockArray1, blockArray2, cartesianBlockArray2)
                    bridgeSprites.add(bridge)
                score.pointsDict = resources['score']
                characterPosition = resources['character']
                enemyPosition = resources['enemy']
                treeList1 = resources['trees1']
                treeList2 = resources['trees2']
                ironList1 = resources['iron1']
                ironList2 = resources['iron2']
                farmList = resources["farm"]
        except EOFError as error:
            print('ooops')

# character picture from: https://ya-webdesign.com/imgdownload.html
    character = createCharacter("character.png", charSprites, cellWidth, 
        cellHeight, blockArray1, cartesianBlockArray1, offsetX1, offsetY1, characterPosition)
    enemy = createEnemies(character, charSprites, cellWidth, 
        cellHeight, blockArray1, cartesianBlockArray1, offsetX1, offsetY1, enemyPosition)
    makeTrees(character, blockArray1, cartesianBlockArray1, inventoryBar,
        offsetX1, offsetY1, cellWidth, cellHeight, 6, 1, treeList1)
    makeTrees(character, blockArray2, cartesianBlockArray2, inventoryBar,
      offsetX1, offsetY1, cellWidth, cellHeight, 5, 2, treeList2)
      
    if (ironList1 is not None):
        for iron in ironList1:
            placeIron(character, blockArray1, cartesianBlockArray1, 
                inventoryBar, offsetX1, offsetY1, cellWidth, cellHeight, 1, iron)
    if (ironList2 is not None):
        for iron in ironList2:
            placeIron(character, blockArray2, cartesianBlockArray2, 
                inventoryBar, offsetX1, offsetY1, cellWidth, cellHeight, 2, iron)
    if (farmList is not None):
        image = "farm.png"
        for farmPos in farmList:
            farm = Farm(image, farmDict, blockArray1, cartesianBlockArray1,
                offsetX1, offsetY1, cellWidth, cellHeight, 1, farmPos)
            buildingSprites.add(farm)

    createIronEvent = pygame.USEREVENT + 1
    createTreeEvent = pygame.USEREVENT + 2
    createEnemyEvent = pygame.USEREVENT + 3
    farmWoodEvent = pygame.USEREVENT + 4
    pygame.time.set_timer(createIronEvent, 2000)
    pygame.time.set_timer(createTreeEvent, 1000)
    pygame.time.set_timer(createEnemyEvent, 3000)
    pygame.time.set_timer(farmWoodEvent, 3000)

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
            if (event.type == createIronEvent and not variables.isSplashScreen
                and not variables.isInstructionsScreen and not variables.isGameOver
                and not variables.isShopping):
                if (len(ironSprites) < 4):
                    placeIron(character, blockArray1, cartesianBlockArray1, 
                        inventoryBar, offsetX1, offsetY1, cellWidth, cellHeight, 1)
                    character.collectIron()
            elif (event.type == createTreeEvent):
                treeCount1 = sumTreesOnIsland(1)
                treeCount2 = sumTreesOnIsland(2)
                island = None
                if (treeCount1 < 3):
                    makeTrees(character, blockArray1, cartesianBlockArray1, 
                        inventoryBar, offsetX1, offsetY1, cellWidth, cellHeight, 1, 1)
                elif (treeCount2 < 3):
                    makeTrees(character, blockArray1, cartesianBlockArray1, 
                        inventoryBar, offsetX1, offsetY1, cellWidth, cellHeight, 1, 2)
                
            elif (event.type == farmWoodEvent and not variables.isGameOver):
                for building in buildingSprites:
                    if (isinstance(building, Farm)):
                        image = "tree.png"
                        location = (int(cellWidth * 1.5), int(cellHeight * 1.5))
                        variables.isFarmProduction = True
                        tree = Trees(image, character, blockArray1, cartesianBlockArray1,
                            inventoryBar, offsetX1, offsetY1, location, 1)
                        tree.addWoodToInventory()
                        variables.isFarmProduction = False
            elif (event.type == createEnemyEvent and not variables.isGameOver):
                if (len(enemySprites) == 0):
                    enemy = createEnemies(character, charSprites, cellWidth, cellHeight, 
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

    if (variables.isGameOver):
        if os.path.exists('resources.bin'):
            os.remove('resources.bin')
    else:
        # https://www.techcoil.com/blog/how-to-save-and-load-objects-to-and-from-file-in-python-via-facilities-from-the-pickle-module/
        resources = dict()
        count = numResourceSprites('wood')
        resources['wood'] = count
        count = numResourceSprites('iron')
        resources['iron'] = count
        count = numResourceSprites('hammer')
        resources['hammer'] = count
        count = bridgeCount()
        resources['bridge'] = count
        resources['score'] = score.pointsDict
        characterDic = dict()
        characterDic['x'] = character.rect.centerx
        characterDic['y'] = character.rect.centery
        characterDic['scrollX'] = character.scrollX
        characterDic['scrollY'] = character.scrollY
        characterDic['cartScrollX'] = character.cartScrollX
        characterDic['cartScrollY'] = character.cartScrollY
        resources['character'] = characterDic
        enemyDic = dict()
        enemyDic['x'] = enemy.rect.centerx
        enemyDic['y'] = enemy.rect.centery
        enemyDic['scrollX'] = enemy.scrollX
        enemyDic['scrollY'] = enemy.scrollY
        enemyDic['cartScrollX'] = enemy.cartScrollX
        enemyDic['cartScrollY'] = enemy.cartScrollY
        resources['enemy'] = enemyDic

        treeList1 = []
        resources['trees1'] = treeList1
        treeList2 = []
        resources['trees2'] = treeList2
        for tree in treeSprites:
            treeDic = dict()
            if (tree.island == 1):
                treeList1.append(treeDic)
            else:
                treeList2.append(treeDic)
            treeDic['x'] = tree.rect.centerx
            treeDic['y'] = tree.rect.centery
            treeDic['row'] = tree.row
            treeDic['col'] = tree.col

        farmList = []
        resources['farm'] = farmList
        # treeList2 = []
        # resources['trees2'] = treeList2
        for farm in buildingSprites:
            if (isinstance(farm, Farm)):
                farmDic = dict()
                if (farm.island == 1):
                    farmList.append(farmDic)
                farmDic['x'] = farm.rect.centerx
                farmDic['y'] = farm.rect.centery
                farmDic['row'] = farm.row
                farmDic['col'] = farm.col

        ironList1 = []
        resources['iron1'] = ironList1
        ironList2 = []
        resources['iron2'] = ironList2
        for iron in ironSprites:
            ironDic = dict()
            if (iron.island == 1):
                ironList1.append(ironDic)
            else:
                ironList2.append(ironDic)
            ironDic['x'] = iron.rect.centerx
            ironDic['y'] = iron.rect.centery
            ironDic['row'] = iron.row
            ironDic['col'] = iron.col
        with open('resources.bin', 'wb') as resourcefile:
            pickle.dump(resources, resourcefile)

    pygame.quit()
    os._exit(0)

# if (not isGameOver):
playGame()
