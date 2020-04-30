# this class is largely connected to RawResources since this is where most
# resources will go once the character has collected them. This places items
# appropriately in the user's inventory

import pygame
import numpy as np
from variables import *
from rawResources import *
from inventory import *
from character import *
import score

class Resource(pygame.sprite.Sprite):
    def __init__(self, image, resourceType, resourceValue, inventoryBar):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.resourceType = resourceType
        self.resourceValue = resourceValue
        self.inventoryBar = inventoryBar
        self.image, self.rect = self.scaleImage(self.image, self.rect)
    
    # scales image based on the size of the inventory bar space
    def scaleImage(self, image, rect):
        self.barSpaceWidth, self.barSpaceHeight = self.inventoryBar.getInventorySpaceDimensions()
        location = (int(self.barSpaceWidth * .75), int(self.barSpaceHeight * .75))
        image = pygame.transform.scale(image, location)
        rect = image.get_rect()
        return image, rect

    # places the item in inventory in a specific space
    def placeInInventory(self, space):
        inventorySpaces = self.getInventorySpaces()
        self.rect.x, self.rect.y = inventorySpaces[space]
        self.rect.centerx = self.rect.x + self.barSpaceWidth / 2
        self.rect.centery = self.rect.y + self.barSpaceHeight / 2

    # retrieves the dimensions of the inventory spaces and returns a list with
    # coordinates for the corners of these spaces
    def getInventorySpaces(self):
        spaceTopCorners = []
        topEdgeOfInventorySpace = 10
        leftEdgeOfRect = 80
        betweenInventorySpaces = 20
        leftEdgeOfFirstSpace = self.inventoryBar.rect.x + leftEdgeOfRect
        for i in range(6):
            spaceX = leftEdgeOfFirstSpace + (self.barSpaceWidth + 
                betweenInventorySpaces) * i
            spaceY = topEdgeOfInventorySpace
            spaceTopCorners.append((spaceX, spaceY))
        return spaceTopCorners
    
    # adds a resource caption to the inventory space
    def addCaption(self):
        font = pygame.font.Font('freesansbold.ttf', 12)
        caption = f"{self.amount} {self.resourceType.lower()}"
        text = font.render(caption, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = self.rect.centerx
        textRect.centery = self.rect.y + self.barSpaceHeight - 15
        return text, textRect

    # updates the amount of a resource the character has
    def updateAmount(self, classType):
        currCount = 0
        currAmount = self.getAmount(classType)
        for sprite in resourceSprites:
            if (isinstance(sprite, classType)):
                sprite.amount = currAmount
    
    # retrieves this amount according to the class it belongs to
    def getAmount(self, classType):
        count = 0
        for sprite in resourceSprites:
            if (isinstance(sprite, classType)):
                count += 1
        return count

class Wood(Resource):
    def __init__(self, image, resourceType, resourceValue, inventoryBar):
        super().__init__(image, resourceType, resourceValue, inventoryBar)
        self.amount = 0

class Iron(Resource):
    def __init__(self, image, resourceType, resourceValue, inventoryBar):
        super().__init__(image, resourceType, resourceValue, inventoryBar)
        self.amount = 0

class Hammer(Resource):
    def __init__(self, image, resourceType, resourceValue, inventoryBar):
        super().__init__(image, resourceType, resourceValue, inventoryBar)
        self.amount = 0

# counts the resource of a certain type within the sprite group resourceSprites 
def numResourceSprites(resource):
    if (resource == "wood"):
        classType = Wood
    elif (resource == "iron"):
        classType = Iron
    elif (resource == "hammer"):
        classType = Hammer
    count = 0
    for sprite in resourceSprites:
        if (isinstance(sprite, classType)):
            count += 1
    return count