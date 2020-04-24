import pygame
import numpy as np
import variables

class Building(pygame.sprite.Sprite):
    def __init__(self, blockArray, cartesianBlockArray, offsetX, offsetY):
        self.blockArray = blockArray
        
        self.cartBlockArray = cartesianBlockArray
        self.offsetX = offsetX
        self.offsetY = offsetY

class Farm(Building):
    def __init__(self, resourceDict, blockArray, cartesianBlockArray, offsetX, offsetY):
        super().__init__(blockArray, cartesianBlockArray, offsetX, offsetY)
        self.resoureDict = resourceDict