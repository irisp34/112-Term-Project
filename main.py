#########################################################################
# 15112 Term Project Spring 2020
# By: Iris Pan
# This file runs the game and contains the main Pygame while loop to set
# up all graphics
#########################################################################
import pygame
import os
import numpy as np
import pickle
from island import *
from character import *
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
import score

# resets all the character scrolls back to zero after moving and scrolling all
# elements that need to be scrolled
def resetScroll(character):
    character.scrollX = 0
    character.scrollY = 0
    character.cartScrollX = 0
    character.cartScrollY = 0

# adds the current scroll values to each block of the blockArray to make it move
# with the character
def scrollIslands(blockArray, scrollX, scrollY):
    for row in range(blockArray.shape[0]):
        for col in range(blockArray.shape[1]):
            currBlock = blockArray[row, col]
            currBlock.rect.x -= scrollX
            currBlock.rect.y -= scrollY

# scrolls all sprites within a sprite Group
def scrollSprites(spriteGroup, scrollX, scrollY):
    for sprite in spriteGroup:
        sprite.rect.centerx -= scrollX
        sprite.rect.centery -= scrollY

# this function scrolls all elements in the game and then resets scrolls
def scrollAll(blockArray1, blockArray2, scrollX, scrollY, cartScrollX, cartScrollY, character):
    if (character.justMoved):
        scrollSprites(charSprites, scrollX, scrollY)
        scrollSprites(treeSprites, scrollX, scrollY)
        scrollSprites(ironSprites, scrollX, scrollY)
        scrollSprites(bridgeSprites, scrollX, scrollY)
        scrollSprites(enemySprites, scrollX, scrollY)
        scrollSprites(buildingSprites, scrollX, scrollY)
    
        scrollIslands(blockArray1, scrollX, scrollY)
        scrollIslands(cartesianBlockArray1, cartScrollX, cartScrollY)
        scrollIslands(blockArray2, scrollX, scrollY)
        scrollIslands(cartesianBlockArray2, cartScrollX, cartScrollY)
    character.justMoved = False

# main draw function which updates and drawns all sprites on the screen
def redrawAll(character):
    global drawOutline
    global drawUnaffordableMessage
    screen.fill((255, 255, 255))
    
    scrollX = character.scrollX
    scrollY = character.scrollY
    cartScrollX = character.cartScrollX
    cartScrollY = character.cartScrollY

    scrollAll(blockArray1, blockArray2, scrollX, scrollY, cartScrollX, cartScrollY, character)

    # constructs the background and the inventory bar
    waterSprites.update()
    waterSprites.draw(screen)
    inventoryBarSprite.update(screen)
    inventoryBarSprite.draw(screen)
    variables.resourceSprites.update(screen)
    variables.resourceSprites.draw(screen)
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
        enemySprites.update()
        enemySprites.draw(screen)
        ironSprites.update()
        ironSprites.draw(screen)
        drawShopButton()
        buildingSprites.update()
        buildingSprites.draw(screen)
        charSprites.update()
        charSprites.draw(screen)
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
            minX, minY, maxX, maxY = purchasableItems[keyword]
            pygame.draw.rect(screen, (0, 52, 114), (minX, 
                minY, maxX - minX, maxY - minY), 4)
        # tells the user if they have picked an item in the shop they cannot afford
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

    pygame.display.flip()
    resetScroll(character)

# loops through all the inventory sprites present and creates a caption which tells
# the user how many of that resource they have
def createInventoryCaptions(classType):
    text = None
    textRect = None
    for sprite in resourceSprites:
        currCount = 0
        if (isinstance(sprite, classType)):
            if (sprite.amount > currCount):
                currCount = sprite.amount
                text, textRect = sprite.addCaption()
    if (textRect != None and text != None):
        screen.blit(text, textRect)

# calls the appropriate function that executes the correct action when the mouse
# is pressed
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
        beginInstructionsScreen(event)
        count = 1
        for sprite in treeSprites:
            if (sprite.removeTrees(event)):
                break
            count += 1
        character.killEnemy(event)
        variables.isShopping = beginShopping(event)
        beginInstructionsScreen(event)

def bridgeCount():
    count = 0
    for sprite in variables.bridgeSprites:
        count += 1
    return count

# main function which starts the game
def playGame():
    pygame.init()

    # water picture from: http://igm-tuto.blogspot.com/2014/06/pixel-art-draw-water-background.html
    waterImage = pygame.image.load("water.png").convert_alpha()
    rect = waterImage.get_rect()
    createWater(waterSprites, waterImage, rect)
    inventoryBar = Inventory()
    inventoryBarSprite.add(inventoryBar)
    characterPosition = None
    enemyPosition = None
    treeList1 = None
    treeList2 = None
    ironList1 = None
    ironList2 = None
    farmList = None
    factoryList = None
    scrollValues = None

    # this section reads in a file that is saved from the last time the game is
    # played and reassigns variables appropriately. If no file was saved at the
    # last iteration of the game, this is skipped
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
                factoryList = resources["factory"]
                scrollValues = resources["totalScrolls"]

        except EOFError as error:
            print('ooops')

    # adjusts scrolling on the islands after the game is reloaded
    createIslands()
    if (scrollValues != None):
        totalIsoScrollX = scrollValues[0]
        totalIsoScrollY = scrollValues[1]
        totalCartScrollX = scrollValues[2]
        totalCartScrollY = scrollValues[3]
        if (totalIsoScrollX != 0 or totalIsoScrollY != 0):
            scrollIslands(blockArray1, totalIsoScrollX, totalIsoScrollY)
            scrollIslands(cartesianBlockArray1, totalCartScrollX, totalCartScrollY)
            scrollIslands(blockArray2, totalIsoScrollX, totalIsoScrollY)
            scrollIslands(cartesianBlockArray2, totalCartScrollX, totalCartScrollY)

    # world building for character, enemy, and trees
    # character picture from: https://ya-webdesign.com/imgdownload.html
    character = createCharacter("character.png", charSprites, cellWidth, 
        cellHeight, blockArray1, cartesianBlockArray1, offsetX1, offsetY1, characterPosition)
    enemy = createEnemies(character, charSprites, cellWidth, 
        cellHeight, blockArray1, cartesianBlockArray1, offsetX1, offsetY1, enemyPosition)
    makeTrees(character, blockArray1, cartesianBlockArray1, inventoryBar,
        offsetX1, offsetY1, cellWidth, cellHeight, 6, 1, treeList1)
    makeTrees(character, blockArray2, cartesianBlockArray2, inventoryBar,
      offsetX1, offsetY1, cellWidth, cellHeight, 5, 2, treeList2)
    
    # places any buildings or resources from the saved version of the game
    if (ironList1 is not None):
        for iron in ironList1:
            placeIron(character, blockArray1, cartesianBlockArray1, 
                inventoryBar, offsetX1, offsetY1, cellWidth, cellHeight, 1, iron)
    if (ironList2 is not None):
        for iron in ironList2:
            placeIron(character, blockArray2, cartesianBlockArray2, 
                inventoryBar, offsetX1, offsetY1, cellWidth, cellHeight, 2, iron)
    if (farmList is not None):
        # picture cited in shopping.py
        image = "farm.png"
        location = (int(cellWidth * 1.5), int(cellHeight * 1.25))
        for farmPos in farmList:
            farm = Farm(image, farmDict, blockArray1, cartesianBlockArray1,
                offsetX1, offsetY1, cellWidth, cellHeight, location, 1, farmPos)
            buildingSprites.add(farm)
    if (factoryList is not None):
        # picture cited in shopping.py
        image = "factory1.png"
        location = (int(cellWidth * 1.25), int(cellHeight * 1.75))
        for factoryPos in factoryList:
            factory = Factory(image, factoryDict, blockArray1, cartesianBlockArray1,
                offsetX1, offsetY1, cellWidth, cellHeight, location, 1, factoryPos)
            buildingSprites.add(factory)

    # generates events that will be executed automatically after a certain time
    createIronEvent = pygame.USEREVENT + 1
    createTreeEvent = pygame.USEREVENT + 2
    createEnemyEvent = pygame.USEREVENT + 3
    farmWoodEvent = pygame.USEREVENT + 4
    factoryIronEvent = pygame.USEREVENT + 5
    pygame.time.set_timer(createIronEvent, 3000)
    pygame.time.set_timer(createTreeEvent, 2000)
    pygame.time.set_timer(createEnemyEvent, 3000)
    pygame.time.set_timer(farmWoodEvent, 3000)
    pygame.time.set_timer(factoryIronEvent, 3000)

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
            # replenishes iron within the game (iron only exists on the main island)
            if (event.type == createIronEvent and not variables.isSplashScreen
                and not variables.isInstructionsScreen and not variables.isGameOver
                and not variables.isShopping):
                if (len(ironSprites) < 4):
                    placeIron(character, blockArray1, cartesianBlockArray1, 
                        inventoryBar, offsetX1, offsetY1, cellWidth, cellHeight, 1)
                    character.collectIron()
            # replenishes trees on each island
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
            # for each Farm that is built, wood will automatically be produced
            # from that farm. This section adds the newly produced wood to inventory
            elif (event.type == farmWoodEvent and not variables.isGameOver):
                for building in buildingSprites:
                    if (isinstance(building, Farm)):
                        image = "tree.png"
                        location = (int(cellWidth * 1.5), int(cellHeight * 1.5))
                        variables.isBuildingProduction = True
                        tree = Trees(image, character, blockArray1, cartesianBlockArray1,
                            inventoryBar, offsetX1, offsetY1, location, 1)
                        tree.addWoodToInventory()
                        variables.isBuildingProduction = False
            # factories generate iron like farms with wood. These iron resources
            # are automatically added to inventory
            elif (event.type == factoryIronEvent and not variables.isGameOver):
                for building in buildingSprites:
                    if (isinstance(building, Factory)):
                        image = "metalBar.png"
                        location = (int(cellWidth * .6), int(cellHeight * .6))
                        variables.isBuildingProduction = True
                        iron = RawIron(image, character, blockArray1, 
                            cartesianBlockArray1, inventoryBar,
                            offsetX1, offsetY1, location, 1)
                        iron.addIronToInventory()
                        variables.isBuildingProduction = False
            # when the current enemy is killed, a new one is spawned.
            elif (event.type == createEnemyEvent and not variables.isGameOver):
                if (len(enemySprites) == 0):
                    enemy = createEnemies(character, charSprites, cellWidth, cellHeight, 
                        blockArray1, cartesianBlockArray1, offsetX1, offsetY1)

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
    
        redrawAll(character)

    # removes the current saved resources file if the game is over
    if (variables.isGameOver):
        if os.path.exists('resources.bin'):
            os.remove('resources.bin')
    # if the game is not over, all relevant resource characteristics are stored
    # into the file
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
        scrollList = [character.totalIsoScrollX, character.totalIsoScrollY, 
            character.totalCartScrollX, character.totalCartScrollY]
        resources["totalScrolls"] = scrollList

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
        factoryList = []
        resources['farm'] = farmList
        resources["factory"] = factoryList
        for sprite in buildingSprites:
            if (isinstance(sprite, Farm)):
                farmDic = dict()
                if (sprite.island == 1):
                    farmList.append(farmDic)
                farmDic['x'] = sprite.rect.centerx
                farmDic['y'] = sprite.rect.centery
                farmDic['row'] = sprite.row
                farmDic['col'] = sprite.col
            elif (isinstance(sprite, Factory)):
                factoryDic = dict()
                if (sprite.island == 1):
                    factoryList.append(factoryDic)
                factoryDic['x'] = sprite.rect.centerx
                factoryDic['y'] = sprite.rect.centery
                factoryDic['row'] = sprite.row
                factoryDic['col'] = sprite.col

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

playGame()
