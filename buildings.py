# Building class controls the Farms and Factories that the user can buy

import pygame
import numpy as np
import variables
from island import *
import random

class Building(pygame.sprite.Sprite):
    def __init__(self, image, blockArray, cartesianBlockArray, offsetX, offsetY,
        cellWidth, cellHeight, location, island, position = None):
        super().__init__()
        self.blockArray = blockArray
        self.cartBlockArray = cartesianBlockArray
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        self.island = island
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.scaleLocation = location
        self.image, self.rect = self.scaleImage(self.image, self.rect, self.scaleLocation)
        self.findCartesianBounds(self.cartBlockArray)
        # sets positions of the objects if the game was saved
        if (position is not None):
            self.rect.centerx = position['x']
            self.rect.centery = position['y']
            self.row = position['row']
            self.col = position['col']
            self.block = blockArray[self.row, self.col]
            self.block.isEmpty = False
        else:
            self.rect.centerx, self.rect.centery, self.row, self.col, self.block = self.getRandomBoardCenter(self.blockArray)
    
    # scales image to right size
    def scaleImage(self, image, rect, location):
        image = pygame.transform.scale(image, location)
        rect = image.get_rect()
        return image, rect

    # finds the bounds for a cartesian block array
    def findCartesianBounds(self, cartBlockArray):
        cartBoard = getBoardBounds(cartBlockArray)
        self.cartMinX = cartBoard[0][0]
        self.cartMinY = cartBoard[0][1]
        self.cartMaxX = cartBoard[3][0]
        self.cartMaxY = cartBoard[3][1]
    
    # randomly generates a row and col based on the board size
    def pickRandomRowAndCol(self, boardRows, boardCols):
        randRow = random.randint(0, boardRows - 2)
        randCol = random.randint(0, boardCols - 2)
        return randRow, randCol
    
    # finds the center of where the block is (with an adjustment for taller
    # images)
    def findBlockCenter(self, block):
        centerX = (block.rect.centerx + block.rect.midtop[0]) / 2
        centerY = (block.rect.centery + block.rect.midtop[1]) / 2
        return centerX, centerY

    def convertIsometricToCartesian(self, isoX, isoY):
        cartesianX = (isoX + isoY * 2) / 2
        cartesianY = (2*isoY - isoX) / 2
        return (cartesianX, cartesianY)

    def convertCartesianToIsometric(self, cartX, cartY):
        isoX = (cartX - cartY)
        isoY = ((cartX + cartY) / 2)
        return (isoX, isoY)

    # retrieves a random isometric board center that doesn't already have
    # something on it to place the building on
    def getRandomBoardCenter(self, blockArray):
        boardRows = blockArray.shape[0]
        boardCols = blockArray.shape[1]
        maxVal = boardRows * boardCols
        count = 0
        while (True):
            randRow, randCol = self.pickRandomRowAndCol(boardRows, boardCols)
            block = blockArray[randRow, randCol]
            if (block.isEmpty):
                block.isEmpty = False
                centerX, centerY = self.findBlockCenter(block)
                return centerX, centerY, randRow, randCol, block
            count += 1
            if (count > maxVal):
                print("Try times exceeds max value")

# child classes of Building 
class Farm(Building):
    def __init__(self, image, resourceDict, blockArray, cartesianBlockArray, 
        offsetX, offsetY, cellWidth, cellHeight, location, island, position = None):
        super().__init__(image, blockArray, cartesianBlockArray, offsetX, offsetY, 
            cellWidth, cellHeight, location, island, position)
        self.resoureDict = resourceDict

class Factory(Building):
    def __init__(self, image, resourceDict, blockArray, cartesianBlockArray, 
        offsetX, offsetY, cellWidth, cellHeight, location, island, position = None):
        super().__init__(image, blockArray, cartesianBlockArray, offsetX, offsetY, 
            cellWidth, cellHeight, location, island, position)
        self.resoureDict = resourceDict
