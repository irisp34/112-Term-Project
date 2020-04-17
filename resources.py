import pygame
import numpy as np
from variables import *
from trees import *
from inventory import *
from character import *

class Resource(pygame.sprite.Sprite):
    def __init__(self, image, resourceType, resourceValue, resourceAmount, inventoryBar):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.resourceType = resourceType
        self.resourceValue = resourceValue
        self.amount = resourceAmount
        self.inventoryBar = inventoryBar
        self.image, self.rect = self.scaleImage(self.image, self.rect)
    
    def scaleImage(self, image, rect):
        self.barSpaceWidth, self.barSpaceHeight = self.inventoryBar.getInventorySpaceDimensions()
        location = (int(self.barSpaceWidth * .75), int(self.barSpaceHeight * .75))
        image = pygame.transform.scale(image, location)
        rect = image.get_rect()
        return image, rect
    
    def placeInInventory(self):
        # barSpaceWidth, barSpaceHeight = self.inventoryBar.getInventorySpaceDimensions()
        inventorySpaces = self.getInventorySpaces()
        self.rect.x, self.rect.y = inventorySpaces[0]
        self.rect.centerx = self.rect.x + self.barSpaceWidth / 2
        self.rect.centery = self.rect.y + self.barSpaceHeight / 2
        print("log location", self.rect.x, self.rect.y)

    def getInventorySpaces(self):
        space1 = (self.inventoryBar.rect.x + 80, 10)
        return [space1]