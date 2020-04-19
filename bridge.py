import pygame
import numpy as np
from variables import *

class Bridge(pygame.sprite.Sprite):
    def __init__(self, cost, resourceType, cellWidth, cellHeight, blockArray1, 
        cartesianBlockArray1, blockArray2, cartesianBlockArray2):
        super().__init__()
        self.cost = cost
        self.resourceType = resourceType
        self.image = pygame.image.load("bridge.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        self.blockArray1 = blockArray1
        self.cartBlockArray1 = cartesianBlockArray1
        self.blockArray2 = blockArray2
        self.cartBlockArray2 = cartesianBlockArray2

    def scaleImage(self):
        location = (self.boardCellWidth, self.boardCellHeight)
        self.image = pygame.transform.scale(self.image, location)
        self.rect = self.image.get_rect()

def addBridgeToShop(bridgeCost, bridgeResource):
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
    # add bridge cost text
    font = pygame.font.Font('freesansbold.ttf', 16)
    caption = f"Cost: {bridgeCost} {bridgeResource}"
    text = font.render(caption, True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = bridgeRect.centerx
    textRect.centery = bridgeRect.bottomright[1] + 15
    screen.blit(text, textRect)
    return bridge, bridgeRect
