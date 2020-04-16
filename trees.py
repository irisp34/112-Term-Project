import pygame
import numpy as np
import random
from variables import *
from character import *
from island import *

class Trees(pygame.sprite.Sprite):
    def __init__(self, character):
        super().__init__()
        self.character = character
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        # tree image: https://www.reddit.com/r/PixelArt/comments/6ktv32/newbiecc_looking_for_tips_how_to_improve_this_tree/
        self.image = pygame.image.load("tree.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.scaleImage()
        self.rect.centerx, self.rect.centery = self.getRandomBoardCenter(blockArray1)
        self.carbonDioxide = 10
        self.cutDown = False
    
    def scaleImage(self):
        location = (int(self.boardCellWidth * 1.5), int(self.boardCellHeight * 1.5))
        self.image = pygame.transform.scale(self.image, location)
        self.rect = self.image.get_rect()

    def findBlockCenter(self, block):
        centerX = (block.rect.centerx + block.rect.midtop[0]) // 2
        centerY = (block.rect.centery + block.rect.midtop[1]) // 2
        return centerX, centerY

    def pickRandomRowAndCol(self, boardRows, boardCols):
        randRow = random.randint(0, boardRows - 1)
        randCol = random.randint(0, boardCols - 1)
        return randRow, randCol

    # retrieves a random isometric board center that doesn't already have
    # something on it to place a tree on
    def getRandomBoardCenter(self, blockArray):
        seenCenters = []
        for sprite in treeSprites:
            seenCenters.append(sprite.rect.centerx, sprite.rect.centery)
        boardRows = blockArray.shape[0]
        boardCols = blockArray.shape[1]
        randRow, randCol = self.pickRandomRowAndCol(boardRows, boardCols)
        charCenterX = self.character.rect.centerx
        charCenterY = self.character.rect.centery
        block = blockArray[randRow, randCol]
        centerX, centerY = self.findBlockCenter(block)
        seenCenters.append((charCenterX, charCenterY))
        while ((centerX, centerY) in seenCenters):
            randRow, randCol = self.pickRandomRowAndCol(boardRows, boardCols)
            block = blockArray[randRow, randCol]
            centerX, centerY = self.findBlockCenter(self, block)
        return centerX, centerY
    
def sumCarbon(self):
    totCarbon = 0
    for sprite in treeSprites:
        totCarbon += sprite.carbonDioxide
    return totCarbon