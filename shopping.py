import pygame
import numpy as np
from variables import *

def createShop():
    # cobblestone image from: https://tinyurl.com/y9poq2sb
    background = pygame.image.load("cobblestone.jpg")
    backgroundRect = background.get_rect()

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
    buyButtonRect.y = height - 150
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
