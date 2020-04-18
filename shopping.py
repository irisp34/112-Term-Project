import pygame
import numpy as np
from variables import *
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
    addBridgeToShop()

def addBridgeToShop():
    # purchasableItems.add("bridge")
    bridge = pygame.image.load("woodBridge.png").convert_alpha()
    bridgeRect = bridge.get_rect()
    location = (int(bridgeRect.width * .5), int(bridgeRect.height * .5))
    bridge = pygame.transform.scale(bridge, location)
    bridgeRect = bridge.get_rect()
    bridgeRect.x = baseX + betweenItemsOffset
    bridgeRect.y = baseY + betweenItemsOffset
    minX, minY = bridgeRect.x, bridgeRect.y
    maxX, maxY = bridgeRect.bottomright[0], bridgeRect.bottomright[1]
    purchasableItems["bridge"] = (minX, minY, maxX, maxY)
    screen.blit(bridge, (bridgeRect.x, bridgeRect.y))
    return bridge, bridgeRect

def selectedItem(event):
    drawOutline = False
    keyword = None
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, 60, 60))
    posX, posY = event.pos
    print("clicked bridge", posX, posY)
    image = None
    imageRect = None
    print("items", purchasableItems)
    for key in purchasableItems:
        if (key.lower() == "bridge"):
            # image, imageRect = addBridgeToShop()
            imageDim = purchasableItems[key]
            keyword = key
            print("in if")
        # minX, minY = imageRect.x, imageRect.y
        # maxX, maxY = imageRect.bottomright[0], imageRect.bottomright[1]
        minX, minY, maxX, maxY = imageDim
        print("min max", minX, minY, maxX, maxY)
        print(posX >= minX, posX <= maxX, posY >= minY, posY <= maxY)
        if (posX >= minX and posX <= maxX and posY >= minY and posY <= maxY):
            # print("here")
            drawOutline = True
        return drawOutline, keyword
        

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
    buyButtonRect.y = height - 200
    return buyImage, buyButtonRect

def drawBuyButton():
    buyImage, buyButtonRect = buyButtonInfo()
    screen.blit(buyImage, (buyButtonRect.x, buyButtonRect.y))

def beginShopping(event):
    global isShopping
    print("before", isShopping)
    shopImage, shopButtonRect = shopButtonInfo()
    posX, posY = event.pos
    print("posx y", posX, posY)
    shopMinX, shopMinY = shopButtonRect.x, shopButtonRect.y
    shopMaxX, shopMaxY = shopButtonRect.bottomright[0], shopButtonRect.bottomright[1]
    print("shop min max", shopMinX, shopMinY, shopMaxX, shopMaxY)
    print("x", posX >= shopMinX, posX <= shopMaxX,"y", posY >= shopMinY, posY <= shopMaxY)
    if (posX >= shopMinX and posX <= shopMaxX and posY >= shopMinY and posY <= shopMaxY):
        isShopping = True
    print("isshopping", isShopping)
    return isShopping

# adjust to buy if an item is selected
def endShopping(event):
    global isShopping
    buyImage, buyButtonRect = buyButtonInfo()
    posX, posY = event.pos
    buyMinX, buyMinY = buyButtonRect.x, buyButtonRect.y
    buyMaxX, buyMaxY = buyButtonRect.bottomright[0], buyButtonRect.bottomright[1]
    if (posX >= buyMinX and posX <= buyMaxX and posY >= buyMinY and posY <= buyMaxY):
        isShopping = False
        # add subtracting resources
    return isShopping
