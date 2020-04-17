import pygame
import numpy as np
from variables import *

# creates Water objects from the water image to act as the background of the
# game

class Water(pygame.sprite.Sprite):
    def __init__(self, image, location):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        # self.rect.x, self.rect.y = location

# repeatedly generates water picture sprites to fill the width and height of
# the screen
def createWater(waterSprites, image, rect):
    rect.width, rect.height = rect[2], rect[3]
    for xPixel in range(0, width, rect.width):
        for yPixel in range(0, height, rect.height):
            water = Water(image, (xPixel, yPixel))
            waterSprites.add(water)