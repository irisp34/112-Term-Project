import pygame
import numpy as np
import random
from variables import *
from character import *
from island import *

class Trees(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # tree image: https://www.reddit.com/r/PixelArt/comments/6ktv32/newbiecc_looking_for_tips_how_to_improve_this_tree/
        self.image = pygame.image.load("tree.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.getRandomBoardCenter()
        self.carbonDioxide = 10
        self.cutDown = False

    # retrieves a random isometric board center
    # fix to account for where character is
    def getRandomBoardCenter(self):
        randRow = random.randint(0, blockRows - 1)
        randCol = random.randint(0, blockCols - 1)
        block = blockArray[randRow, randCol]
        centerX = block.rect.centerx
        centerY = block.rect.centery
        return centerX, centerY
    
def sumCarbon(treeSprites):
    totCarbon = 0
    for sprite in treeSprites:
        totCarbon += sprite.carbonDioxide
    return totCarbon