import pygame
import numpy as np
from variables import *
from rawResources import *
from inventory import *
from character import *

class Resource(pygame.sprite.Sprite):
    def __init__(self, image, resourceType, resourceValue, inventoryBar):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.resourceType = resourceType
        self.resourceValue = resourceValue
        # self.amount = len(resourceSprites) + 1
        self.inventoryBar = inventoryBar
        self.image, self.rect = self.scaleImage(self.image, self.rect)
    
    def scaleImage(self, image, rect):
        self.barSpaceWidth, self.barSpaceHeight = self.inventoryBar.getInventorySpaceDimensions()
        location = (int(self.barSpaceWidth * .75), int(self.barSpaceHeight * .75))
        image = pygame.transform.scale(image, location)
        rect = image.get_rect()
        return image, rect
    
    # generalize to put resources in spaces not filled
    def placeInInventory(self, space):
        inventorySpaces = self.getInventorySpaces()
        self.rect.x, self.rect.y = inventorySpaces[space]
        self.rect.centerx = self.rect.x + self.barSpaceWidth / 2
        self.rect.centery = self.rect.y + self.barSpaceHeight / 2
        print("log location", self.rect.x, self.rect.y)

    def getInventorySpaces(self):
        spaceTopCorners = []
        topEdgeOfInventorySpace = 10
        leftEdgeOfRect = 80
        betweenInventorySpaces = 20
        leftEdgeOfFirstSpace = self.inventoryBar.rect.x + leftEdgeOfRect
        # nextEdgeOfSpace = leftEdgeOfFirstSpace + 
        for i in range(6):
            spaceX = leftEdgeOfFirstSpace + (self.barSpaceWidth + 
                betweenInventorySpaces) * i
            spaceY = topEdgeOfInventorySpace
            spaceTopCorners.append((spaceX, spaceY))
        # space1 = (leftEdgeOfFirstSpace, topEdgeOfInventorySpace)
        # space2 = (self.inventoryBar.rect.x + )
        return spaceTopCorners
    
    def addCaption(self):
        font = pygame.font.Font('freesansbold.ttf', 12)
        caption = f"{self.amount} {self.resourceType.lower()}"
        text = font.render(caption, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = self.rect.centerx
        textRect.centery = self.rect.y + self.barSpaceHeight - 15
        return text, textRect

    # fix to account for different resources
    def updateAmount(self, classType):
        currCount = 0
        # for sprite in resourceSprites:
        #     # sprite.getAmount(classType)
        #     # self.amount = len(resourceSprites)
        #     # print("sprite amount", sprite.amount)
        #     if (isinstance(sprite, classType)):
        #         if (sprite.amount >= currCount):
        #             currCount = sprite.amount
        # for sprite in resourceSprites:
        #     if (isinstance(sprite, classType)):
        #         sprite.amount = currCount
        print("update", resourceSprites)
        currAmount = self.getAmount(classType)
        # currAmount = numResourceSprites(resource)
        print("class", classType, "curramount", currAmount)
        for sprite in resourceSprites:
            if (isinstance(sprite, classType)):
                sprite.amount = currAmount
    
    def getAmount(self, classType):
        print("inget amount", resourceSprites)
        count = 0
        for sprite in resourceSprites:
            if (isinstance(sprite, classType)):
                count += 1
        return count

class Wood(Resource):
    def __init__(self, image, resourceType, resourceValue, inventoryBar):
        super().__init__(image, resourceType, resourceValue, inventoryBar)
        self.amount = 0
        # self.getAmount()
    
    # def getAmount(self):
    #     for sprite in resourceSprites:
    #         if (isinstance(sprite, Wood)):
    #             self.amount += 1

class Iron(Resource):
    def __init__(self, image, resourceType, resourceValue, inventoryBar):
        super().__init__(image, resourceType, resourceValue, inventoryBar)
        self.amount = 0
        # self.getAmount()

class Hammer(Resource):
    def __init__(self, image, resourceType, resourceValue, inventoryBar):
        super().__init__(image, resourceType, resourceValue, inventoryBar)
        self.amount = 0

    
                
def numResourceSprites(resource):
    # resourceType = resourceType[0].upper() + resourceType[1:]
    # print("resource", resourceType)
    if (resource == "wood"):
        classType = Wood
    elif (resource == "iron"):
        classType = Iron
    elif (resource == "hammer"):
        classType = Hammer
    count = 0
    for sprite in resourceSprites:
        # print("isinstance", isinstance(sprite, classType))
        if (isinstance(sprite, classType)):
            count += 1
    return count