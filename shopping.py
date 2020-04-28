import pygame
import numpy as np
from variables import *
from bridge import *
from resources import *
from buildings import *
import score

def createShop():
    pygame.draw.rect(screen, (163, 196, 220), (baseX, baseY, width - baseX * 2, 
        height - baseY * 2))
    pygame.draw.rect(screen, (0, 52, 114), (baseX, baseY, width - baseX * 2, 
        height - baseY * 2), 4)
    addBridgeToShop(bridgeDict)
    addHammerToShop(hammerDict)
    addFarmToShop(farmDict)
    addFactoryToShop(factoryDict)

def scaleImage(image, location):
    image = pygame.transform.scale(image, location)
    rect = image.get_rect()
    return image, rect

# takes in the resources needed to buy the item and the image rect to display
# the cost in the shop
def createCostCaption(resourceDict, resourceRect):
    font = pygame.font.Font('freesansbold.ttf', 16)
    caption = "Cost: "
    for key in resourceDict:
        caption += f"{resourceDict[key]} {key}, "
    caption = caption[:-2]
    text = font.render(caption, True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = resourceRect.centerx
    textRect.centery = resourceRect.bottomright[1] + 15
    screen.blit(text, textRect)

def addBridgeToShop(bridgeDict):
    bridge = pygame.image.load("woodBridge.png").convert_alpha()
    bridgeRect = bridge.get_rect()
    location = (int(bridgeRect.width * .5), int(bridgeRect.height * .5))
    bridge, bridgeRect = scaleImage(bridge, location)
    bridgeRect.x = baseX + betweenItemsOffset
    bridgeRect.y = baseY + betweenItemsOffset
    minX, minY = bridgeRect.x, bridgeRect.y
    maxX, maxY = bridgeRect.bottomright[0], bridgeRect.bottomright[1]
    # adds this items to dictionary of items that can be purchased
    purchasableItems["bridge"] = (minX, minY, maxX, maxY)
    screen.blit(bridge, (bridgeRect.x, bridgeRect.y))
    createCostCaption(bridgeDict, bridgeRect)
    return bridge, bridgeRect

def addHammerToShop(hammerDict):
    # hammer picture from: https://minecraft.novaskin.me/search?q=axe%20iron
    hammer = pygame.image.load("hammer.png").convert_alpha()
    hammerRect = hammer.get_rect()
    location = (int(hammerRect.width * .2), int(hammerRect.height * .2))
    hammer, hammerRect = scaleImage(hammer, location)
    hammerRect.x = baseX + betweenItemsOffset + 200
    hammerRect.y = baseY + betweenItemsOffset
    minX, minY = hammerRect.x, hammerRect.y
    maxX, maxY = hammerRect.bottomright[0], hammerRect.bottomright[1]
    purchasableItems["hammer"] = (minX, minY, maxX, maxY)
    screen.blit(hammer, (hammerRect.x, hammerRect.y))
    createCostCaption(hammerDict, hammerRect)
    return hammer, hammerRect

# creates the farm that can be bought from the shop and also lists the cost
def addFarmToShop(farmDict):
    # farm picture from: https://www.deviantart.com/thkaspar/art/Unfinished-Isometric-Farm-297762732
    farm = pygame.image.load("farm.png").convert_alpha()
    farmRect = farm.get_rect()
    location = (int(farmRect.width * .5), int(farmRect.height * .5))
    farm, farmRect = scaleImage(farm, location)
    farmRect.x = baseX + betweenItemsOffset + 350
    farmRect.y = baseY + betweenItemsOffset - 20
    minX, minY = farmRect.x, farmRect.y
    maxX, maxY = farmRect.bottomright[0], farmRect.bottomright[1]
    purchasableItems["farm"] = (minX, minY, maxX, maxY)
    screen.blit(farm, (farmRect.x, farmRect.y))
    createCostCaption(farmDict, farmRect)
    return farm, farmRect

def addFactoryToShop(factoryDict):
    # factory picture from: https://design.tutsplus.com/tutorials/how-to-create-an-isometric-pixel-art-factory-in-adobe-photoshop--cms-25351
    factory = pygame.image.load("factory1.png").convert_alpha()
    factoryRect = factory.get_rect()
    location = (int(factoryRect.width * .2), int(factoryRect.height * .2))
    factory, factoryRect = scaleImage(factory, location)
    factoryRect.x = baseX + betweenItemsOffset + 610
    factoryRect.y = baseY + betweenItemsOffset - 65
    minX, minY = factoryRect.x, factoryRect.y
    maxX, maxY = factoryRect.bottomright[0], factoryRect.bottomright[1]
    purchasableItems["factory"] = (minX, minY, maxX, maxY)
    screen.blit(factory, (factoryRect.x, factoryRect.y))
    createCostCaption(factoryDict, factoryRect)
    return factory, factoryRect

# loops through all the purchasable items to detect which item the user has
# clicked on. 
def selectedItem(event, currentItem):
    global drawOutline
    global drawUnaffordableMessage
    # keyword = None
    # # global keyword
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, 60, 60))
    posX, posY = event.pos
    image = None
    imageRect = None
    currKey = None
    selectedItem = None
    for key in purchasableItems:
        print("key", key)
        imageDim = purchasableItems[key]
        currKey = key
        print("currKey", currKey)
        minX, minY, maxX, maxY = imageDim
        isAffordable = affordable(currKey)
        if (posX >= minX and posX <= maxX and posY >= minY and posY <= maxY):
            if (currKey == currentItem):
                return False, None, False

            drawOutline = True
            selectedItem = currKey
            # drawOutline = not drawOutline
            # print("drawOutline", drawOutline)
            if (not isAffordable and drawOutline):
                drawUnaffordableMessage = True
            else:
                drawUnaffordableMessage = False
        if (selectedItem != None):
            return drawOutline, selectedItem, drawUnaffordableMessage
    print("keyword before return", keyword)
    return drawOutline, currentItem, drawUnaffordableMessage
        
def shopButtonInfo():
    # shop button image from: http://pixelartmaker.com/art/48b2d0645893d05
    shopImage = pygame.image.load("shopButton.png").convert_alpha()
    shopButtonRect = shopImage.get_rect()
    location = (int(shopButtonRect.width * .4), int(shopButtonRect.height * .4))
    shopImage = pygame.transform.scale(shopImage, location)
    shopButtonRect = shopImage.get_rect()
    shopButtonRect.x = width - 25 - shopButtonRect.width
    shopButtonRect.y = height - 85
    return shopImage, shopButtonRect

def drawShopButton():
    shopImage, shopButtonRect = shopButtonInfo()
    # print("shop button", shopButtonRect)
    screen.blit(shopImage, (shopButtonRect.x, shopButtonRect.y))

def buyButtonInfo():
    # buy button image from: http://pixelartmaker.com/art/cc53de89e33b6fa
    buyImage = pygame.image.load("buyButton.png").convert_alpha()
    buyButtonRect = buyImage.get_rect()
    location = (int(buyButtonRect.width * .4), int(buyButtonRect.height * .4))
    buyImage = pygame.transform.scale(buyImage, location)
    buyButtonRect = buyImage.get_rect()
    buyButtonRect.x = width / 2 - buyButtonRect.width / 2
    buyButtonRect.y = height - 260
    return buyImage, buyButtonRect

def drawBuyButton():
    buyImage, buyButtonRect = buyButtonInfo()
    screen.blit(buyImage, (buyButtonRect.x, buyButtonRect.y))

def exitButtonInfo():
    # exit button image from: http://pixelartmaker.com/art/23f04c51990a6b8
    exitImage = pygame.image.load("exitButton.png").convert_alpha()
    exitButtonRect = exitImage.get_rect()
    location = (int(exitButtonRect.width * .45), int(exitButtonRect.height * .45))
    exitImage = pygame.transform.scale(exitImage, location)
    exitButtonRect = exitImage.get_rect()
    exitButtonRect.x = (width / 2) - (exitButtonRect.width / 2) + 5
    exitButtonRect.y = height - 185
    return exitImage, exitButtonRect

def drawExitButton():
    exitImage, exitButtonRect = exitButtonInfo()
    screen.blit(exitImage, (exitButtonRect.x, exitButtonRect.y))

def beginShopping(event):
    global isShopping
    shopImage, shopButtonRect = shopButtonInfo()
    posX, posY = event.pos
    shopMinX, shopMinY = shopButtonRect.x, shopButtonRect.y
    shopMaxX, shopMaxY = shopButtonRect.bottomright[0], shopButtonRect.bottomright[1]
    if (posX >= shopMinX and posX <= shopMaxX and posY >= shopMinY and posY <= shopMaxY):
        isShopping = True
    return isShopping

# generates the bought item by creating an instance of the class it belongs to
def createBoughtItem(keyword, inventoryBar):
    if (keyword == "bridge"):
        bridge = Bridge(bridgeDict, cellWidth, cellHeight, blockArray1,
            cartesianBlockArray1, blockArray2, cartesianBlockArray2)
        bridgeSprites.add(bridge)
        score.pointsDict["bridges built"] += 1
    elif (keyword == "hammer"):
        hammer = Hammer("hammer.png", "hammer", 1, inventoryBar)
        resourceSprites.add(hammer)
        hammer.placeInInventory(2)
        hammer.updateAmount(Hammer)
        score.pointsDict["hammers created"] += 1
    elif (keyword == "farm"):
        image = "farm.png"
        location = (int(cellWidth * 1.5), int(cellHeight * 1.25))
        farm = Farm(image, farmDict, blockArray1, cartesianBlockArray1,
            offsetX1, offsetY1, cellWidth, cellHeight, location, 1)
        buildingSprites.add(farm)
        score.pointsDict["farms built"] += 1
    elif (keyword == "factory"):
        image = "factory1.png"
        location = (int(cellWidth * 1.25), int(cellHeight * 1.75))
        factory = Factory(image, farmDict, blockArray1, cartesianBlockArray1,
            offsetX1, offsetY1, cellWidth, cellHeight, location, 1)
        buildingSprites.add(factory)
        score.pointsDict["factories built"] += 1

# takes out resource sprites out of inventory to pay for items
def subtractResources(keyword):
    count = 0
    if (keyword == "bridge"):
        for sprite in resourceSprites:
            if (isinstance(sprite, Wood)):
                sprite.kill()
                count += 1
                if (count == bridgeDict["wood"]):
                    sprite.updateAmount(Wood)
                    break
    elif (keyword == "hammer"):
        woodCount = 0
        ironCount = 0
        for sprite in resourceSprites:
            if (woodCount == hammerDict["wood"] and ironCount == hammerDict["iron"]):
                sprite.updateAmount(Wood)
                sprite.updateAmount(Iron)
                return
            elif (isinstance(sprite, Wood) and woodCount != hammerDict["wood"]):
                woodCount += 1
                sprite.kill()
            elif (isinstance(sprite, Iron) and ironCount != hammerDict["iron"]):
                ironCount += 1
                sprite.kill()
    elif (keyword == "farm"):
        woodCount = 0
        hammerCount = 0
        for sprite in resourceSprites:
            if (woodCount == farmDict["wood"] and hammerCount == farmDict["hammer"]):
                sprite.updateAmount(Wood)
                sprite.updateAmount(Hammer)
                return
            elif (isinstance(sprite, Wood) and woodCount != farmDict["wood"]):
                woodCount += 1
                sprite.kill()
            elif (isinstance(sprite, Hammer) and hammerCount != farmDict["hammer"]):
                hammerCount += 1
                sprite.kill()
    elif (keyword == "factory"):
        woodCount = 0
        hammerCount = 0
        ironCount = 0 
        for sprite in resourceSprites:
            if (woodCount == factoryDict["wood"] and hammerCount == factoryDict["hammer"]
                and ironCount == factoryDict["iron"]):
                sprite.updateAmount(Wood)
                sprite.updateAmount(Iron)
                sprite.updateAmount(Hammer)
                return
            elif (isinstance(sprite, Wood) and woodCount != factoryDict["wood"]):
                woodCount += 1
                sprite.kill()
            elif (isinstance(sprite, Hammer) and hammerCount != factoryDict["hammer"]):
                hammerCount += 1
                sprite.kill()
            elif (isinstance(sprite, Iron) and ironCount != factoryDict["iron"]):
                ironCount += 1
                sprite.kill()

# checks if you can afford the thing you are trying to buy by checking how many
# types of a resource sprite you have
def affordable(keyword):
    if (keyword == None):
        return True
    currDict = None
    if (keyword == "bridge"):
        currDict = bridgeDict
    elif (keyword == "hammer"):
        currDict = hammerDict
    elif (keyword == "farm"):
        currDict = farmDict
    elif (keyword == "factory"):
        currDict = factoryDict
    for key in currDict:
        if (numResourceSprites(key) < currDict[key]):
            return False
    return True

# detects whether shopping has ended or not by whether the user clicked the 
# buy button or the exit button and purchases the item if buy was clicked
def endShopping(event, keyword, inventoryBar):
    global isShopping
    global drawOutline
    buyImage, buyButtonRect = buyButtonInfo()
    exitImage, exitButtonRect = exitButtonInfo()
    posX, posY = event.pos
    buyMinX, buyMinY = buyButtonRect.x, buyButtonRect.y
    buyMaxX, buyMaxY = buyButtonRect.bottomright[0], buyButtonRect.bottomright[1]
    exitMinX, exitMinY = exitButtonRect.x, exitButtonRect.y
    exitMaxX, exitMaxY = exitButtonRect.bottomright[0], exitButtonRect.bottomright[1]
    isInBuyBounds = posX >= buyMinX and posX <= buyMaxX and posY >= buyMinY and posY <= buyMaxY
    isInExitBounds = posX >= exitMinX and posX <= exitMaxX and posY >= exitMinY and posY <= exitMaxY
    isAffordable = affordable(keyword)
    if (isInExitBounds):
        isShopping = False
        if (drawOutline):
            drawOutline = not drawOutline
    if (isInBuyBounds and drawOutline and isAffordable):
        isShopping = False
        subtractResources(keyword)
        createBoughtItem(keyword, inventoryBar)
    return isShopping
