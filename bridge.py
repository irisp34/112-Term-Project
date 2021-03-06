# Bridge class creates the bridges and places them appropriately between the
# two islands

import pygame
import numpy as np
from variables import *

class Bridge(pygame.sprite.Sprite):
    def __init__(self, bridgeDict, cellWidth, cellHeight, blockArray1, 
        cartesianBlockArray1, blockArray2, cartesianBlockArray2):
        super().__init__()
        self.bridgeDict = bridgeDict
        #bridge picture: http://pixelartmaker.com/art/4bc6db1c50b02fc
        self.image = pygame.image.load("bridge.png").convert_alpha()
        self.rect = self.image.get_rect()
        #angle for 10 x 10
        self.angle = 30
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        self.blockArray1 = blockArray1
        self.cartBlockArray1 = cartesianBlockArray1
        self.blockArray2 = blockArray2
        self.cartBlockArray2 = cartesianBlockArray2
        self.setBridgeCoordinates()

    def scaleImage(self, locationX):
        location = (locationX + 30, self.boardCellHeight)
        self.image = pygame.transform.scale(self.image, location)
        self.rect = self.image.get_rect()
    
    # rotates the given image by a certain angle
    def rotateImage(self):
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()

    # Finds the correct location of where the bridge is supposed to be based
    # on the offsets provided
    # Note: optimized for more islands, but did not get a chance to add more due
    # to time constraint
    def findIslandRowAndCol(self):
        originRow = 0
        originCol = 0
        destinationRow = 0
        destinationCol = 0
        locationX = 25
        blockRows1 = self.cartBlockArray1.shape[0] - 1
        blockCols1 = self.cartBlockArray1.shape[1] - 1
        blockRows2 = self.cartBlockArray2.shape[0] - 1
        blockCols2 = self.cartBlockArray2.shape[1] - 1
        offsetX1 = self.blockArray1[0,0].offsetX
        offsetY1 = self.blockArray1[0,0].offsetY
        offsetX2 = self.blockArray2[0,0].offsetX
        offsetY2 = self.blockArray2[0,0].offsetY
        isUpLeft = ((offsetX1 > offsetX2 and offsetY1 > offsetY2) or 
            (offsetX1 > offsetX2 and offsetY1 == offsetY2) or
            (offsetX1 == offsetX2 and offsetY1 > offsetY2))
        isUpRight = ((offsetX1 < offsetX2 and offsetY1 > offsetY2) or 
            (offsetX1 < offsetX2 and offsetY1 == offsetY2))
        isDownLeft = ((offsetX1 > offsetX2 and offsetY1 < offsetY2) or
            (offsetX1 == offsetX2 and offsetY1 < offsetY2))
        isDownRight = (offsetX1 < offsetX2 and offsetY1 < offsetY2)
        if (isUpLeft):
            originRow = blockRows1 // 2
            originCol = 0
            destinationRow = blockRows2 // 2
            destinationCol = blockCols2
            locationX = abs(self.blockArray1[blockRows1, 0].rect.topright[0] - 
                self.blockArray2[blockRows2, blockCols2].rect.topright[0])
            self.bridgeName = "1to5"
        elif (isUpRight):
            originRow = 0
            originCol = blockCols1 // 2
            destinationRow = blockRows2
            destinationCol = blockCols2 // 2
            locationX = abs(self.blockArray1[0, blockCols1].rect.topright[0] - 
                self.blockArray2[blockRows2, blockCols2].rect.topright[0])
            self.bridgeName = "1to2"
        elif (isDownLeft):
            originRow = blockRows1
            originCol = blockCols1 // 2
            destinationRow = 0
            destinationCol = blockCols2 // 2
            locationX = abs(self.blockArray1[0, blockCols1].rect.topright[0] - 
                self.blockArray2[0, 0].rect.topright[0])
            self.bridgeName = "1to4"
        elif (isDownRight):
            originRow = blockRows1 // 2
            originCol = blockCols1
            destinationRow = blockRows2 // 2
            destinationCol = 0
            locationX = abs(self.blockArray1[0, blockCols1].rect.topright[0] - 
                self.blockArray2[0, 0].rect.topright[0])
            self.bridgeName = "1to3"
        self.scaleImage(locationX)
        return originRow, originCol, destinationRow, destinationCol

    # adjusts the coordinates of the bridge to where it should be relative to 
    # islands
    def setBridgeCoordinates(self):
        originRow, originCol, destinationRow, destinationCol = self.findIslandRowAndCol()
        originBlock = self.blockArray1[originRow, originCol]
        destinationBlock = self.blockArray2[destinationRow, destinationCol]
        self.rotateImage()
        assignX = (originBlock.rect.bottomright[0] + originBlock.rect.bottomleft[0]) / 2
        assignY = originBlock.rect.bottomright[1]
        self.rect.bottomleft = assignX, assignY
