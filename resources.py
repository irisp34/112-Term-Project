import pygame
import numpy as np
from variables import *
from trees import *
from inventory import *
from character import *

class Resource(pygame.sprite.Sprite):
    def __init__(self, image, resourceType, resourceValue, inventoryBar):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.resourceType = resourceType
        self.resourceValue = resourceValue
        self.amount = len(resourceSprites) + 1
        self.inventoryBar = inventoryBar
        self.image, self.rect = self.scaleImage(self.image, self.rect)
    
    def scaleImage(self, image, rect):
        self.barSpaceWidth, self.barSpaceHeight = self.inventoryBar.getInventorySpaceDimensions()
        location = (int(self.barSpaceWidth * .75), int(self.barSpaceHeight * .75))
        image = pygame.transform.scale(image, location)
        rect = image.get_rect()
        return image, rect
    
    def placeInInventory(self):
        inventorySpaces = self.getInventorySpaces()
        self.rect.x, self.rect.y = inventorySpaces[0]
        self.rect.centerx = self.rect.x + self.barSpaceWidth / 2
        self.rect.centery = self.rect.y + self.barSpaceHeight / 2
        print("log location", self.rect.x, self.rect.y)

    def getInventorySpaces(self):
        topEdgeOfInventorySpace = 10
        space1 = (self.inventoryBar.rect.x + 80, topEdgeOfInventorySpace)
        return [space1]
    
    def addCaption(self):
        font = pygame.font.Font('freesansbold.ttf', 12)
        caption = f"{self.amount} {self.resourceType.lower()}"
        text = font.render(caption, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = self.rect.centerx
        textRect.centery = self.rect.y + self.barSpaceHeight - 15
        return text, textRect

    # fix to account for different resources
    def updateAmount(self):
        currCount = 0
        for sprite in resourceSprites:
            self.amount = len(resourceSprites)
            # print("sprite amount", sprite.amount)
            if (sprite.amount >= currCount):
                currCount = sprite.amount
        for sprite in resourceSprites:
            sprite.amount = currCount

class Wood(Resource):
    def __init__(self, image, resourceType, resourceValue, inventoryBar):
        super().__init__(image, resourceType, resourceValue, inventoryBar)


def numWoodSprites(keyword):
    # resourceType = resourceType[0].upper() + resourceType[1:]
    # print("resource", resourceType)
    if (keyword == "bridge"):
        classType = Wood
    count = 0
    for sprite in resourceSprites:
        print("isinstance", isinstance(sprite, classType))
        if (isinstance(sprite, classType)):
            count += 1
    return count