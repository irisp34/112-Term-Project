import pygame
import numpy as np
from variables import *

class Inventory(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image from: http://pixelartmaker.com/art/cf310145e43029a
        self.image = pygame.image.load("inventoryBar.png").convert_alpha()
        self.image.set_alpha(5)
        self.findImageDimensions()
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.y = -self.barHeight / 2

    def findImageDimensions(self):
        self.barWidth, self.barHeight = self.image.get_size()

    def getInventorySpaceDimensions(self):
        self.spaceWidth = 90
        self.spaceHeight = 70
        return self.spaceWidth, self.spaceHeight