import pygame
import numpy as np
from variables import *
from bridge import *
from resources import *

def createShop():
    # # cobblestone image from: https://tinyurl.com/y9poq2sb
    # background = pygame.image.load("cobblestone.jpg")
    # backgroundRect = background.get_rect()
    # backgroundRect.x = 20
    # backgroundRect.y = 20
    # screen.blit(background, (backgroundRect.x, backgroundRect.y))
    pygame.draw.rect(screen, (163, 196, 220), (baseX, baseY, width - baseX * 2, 
        height - baseY * 2))
    pygame.draw.rect(screen, (0, 52, 114), (baseX, baseY, width - baseX * 2, 
        height - baseY * 2), 4)
    addBridgeToShop(bridgeCost, bridgeResource)

def selectedItem(event):
    global drawOutline
    # global currSelectedItem
    global drawUnaffordableMessage
    keyword = None
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, 60, 60))
    posX, posY = event.pos
    image = None
    imageRect = None
    for key in purchasableItems:
        if (key.lower() == "bridge"):
            imageDim = purchasableItems[key]
            keyword = key
        minX, minY, maxX, maxY = imageDim
        # print("min max", minX, minY, maxX, maxY)
        # print(posX >= minX, posX <= maxX, posY >= minY, posY <= maxY)
        isAffordable = affordable(keyword)
        print("isAffordable", isAffordable)
        if (posX >= minX and posX <= maxX and posY >= minY and posY <= maxY):
            drawOutline = not drawOutline
            print("drawOutline", drawOutline)
            if (not isAffordable and drawOutline):
                drawUnaffordableMessage = True
            else:
                drawUnaffordableMessage = False
            print("drawUnaffordableMessage", drawUnaffordableMessage)
    return drawOutline, keyword, drawUnaffordableMessage
        
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
    # buy button image from: http://pixelartmaker.com/art/cc53de89e33b6fa
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
    # print("posx y", posX, posY)
    shopMinX, shopMinY = shopButtonRect.x, shopButtonRect.y
    shopMaxX, shopMaxY = shopButtonRect.bottomright[0], shopButtonRect.bottomright[1]
    # print("shop min max", shopMinX, shopMinY, shopMaxX, shopMaxY)
    # print("x", posX >= shopMinX, posX <= shopMaxX,"y", posY >= shopMinY, posY <= shopMaxY)
    if (posX >= shopMinX and posX <= shopMaxX and posY >= shopMinY and posY <= shopMaxY):
        isShopping = True
    # print("isshopping", isShopping)
    return isShopping

def createBoughtItem():
    global keyword
    if (keyword == "bridge"):
        bridge = Bridge(bridgeCost, bridgeResource)
        bridgeSprites.add(bridge)

# takes out Wood sprites to pay for bridge
def subtractResources():
    global keyword
    count = 0
    if (keyword == "bridge"):
        for sprite in resourceSprites:
            if (isinstance(sprite, Wood)):
                sprite.kill()
                count += 1
                if (count == bridgeCost):
                    break

def affordable(keyword):
    print("affordable keyword", keyword)
    resourceType = None
    itemCost = None
    amountInInventory = None
    if (keyword == "bridge"):
        resourceType = bridgeResource
        itemCost = bridgeCost
        amountInInventory = numWoodSprites(keyword)
        print("amountInInventory", amountInInventory)
    return amountInInventory >= itemCost

def endShopping(event, keyword):
    global isShopping
    global drawOutline
    # global keyword
    buyImage, buyButtonRect = buyButtonInfo()
    exitImage, exitButtonRect = exitButtonInfo()
    posX, posY = event.pos
    buyMinX, buyMinY = buyButtonRect.x, buyButtonRect.y
    buyMaxX, buyMaxY = buyButtonRect.bottomright[0], buyButtonRect.bottomright[1]
    exitMinX, exitMinY = exitButtonRect.x, exitButtonRect.y
    exitMaxX, exitMaxY = exitButtonRect.bottomright[0], exitButtonRect.bottomright[1]
    isInBuyBounds = posX >= buyMinX and posX <= buyMaxX and posY >= buyMinY and posY <= buyMaxY
    isInExitBounds = posX >= exitMinX and posX <= exitMaxX and posY >= exitMinY and posY <= exitMaxY
    print("endshopping keyword", keyword)
    isAffordable = affordable(keyword)
    if (isInExitBounds):
        isShopping = False
    if (isInBuyBounds and drawOutline and isAffordable):
        isShopping = False
        # subtractResources()
        # createBoughtItem()
        # add subtracting resources
    return isShopping
