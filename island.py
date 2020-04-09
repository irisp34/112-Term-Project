# generates Block objects to encompass a map and makes that map 2.5D

import pygame
import numpy as np
import os
from variables import *

blockArray = np.empty(shape=(blockRows, blockCols), dtype = object)
blockSprites = pygame.sprite.Group()

# Block class creates each of the blocks for the ground
class Block(pygame.sprite.Sprite):
    def __init__(self, cellWidth, cellHeight, color, posX, posY, startX, startY):
        super().__init__()
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.color = color
        self.startX = startX
        self.startY = startY
        # self.image = pygame.Surface([self.cellWidth, self.cellHeight])

        # grass image from https://clipart.info/natural-grass-png-top-view-12874
        self.originalImage = pygame.image.load("grass.png").convert_alpha()
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.margin = 5
        self.image = self.scaleImage()
        
        
        # position of top left corner
        self.rect.x = posX
        self.rect.y = posY
    
    def makeBlockIsometric(self, row, col):
        # self.rotatedImage = self.image
        self.angle = 45
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.cellWidth = self.cellWidth * 2
        self.image = self.scaleImage()
        self.convertCartesianToIsometric(row, col)
    
    def convertCartesianToIsometric(self, row, col):
        halfWidth = self.cellWidth / 2
        halfHeight = self.cellHeight / 2
        offsetX = (width // 2) - self.startX
        offsetY = (height // 2) - self.startY
        self.rect.x = ((col - row) * halfWidth) + offsetX
        self.rect.y = ((row + col) * halfHeight) + offsetY
    
    def scaleImage(self):
        self.image = pygame.transform.scale(self.image, (self.cellWidth, self.cellHeight))
        self.cellWidth, self.cellHeight = self.image.get_size()
        return self.image

# adds Block instances to the array
def addBlockToArray(blockArray, block, row, col):
    blockArray[row, col] = block 

# generates a new Block with the correct properties
def createBlock(blockSprites, blockArray, cellWidth, cellHeight, color, posX,
                posY, startX, startY, row, col):
    block = Block(cellWidth, cellHeight, color, posX, posY, startX, startY)
    addBlockToArray(blockArray, block, row, col)
    blockSprites.add(block)

# loops through the desired rows and columns for the board to make the entire
# board
def make2DBoard(blockSprites, blockArray, blockRows, blockCols, cellWidth, cellHeight, startX, startY):
    newStartX, newStartY = startX - cellWidth, startY - cellHeight
    color = (255, 0, 255)
    for row in range(blockRows):
        newStartX += cellWidth
        for col in range(blockCols):
            newStartY += cellHeight
            createBlock(blockSprites, blockArray, cellWidth, cellHeight, color,
                        newStartX, newStartY, startX, startY, row, col)
        newStartY = startY - cellHeight

def makeBoardIsometric(blockArray):
    for row in range(blockArray.shape[0]):
        for col in range(blockArray.shape[1]):
            print("before x",blockArray[row, col].rect.x, "y", blockArray[row, col].rect.y)
            blockArray[row, col].makeBlockIsometric(row, col)
            print("after x", blockArray[row, col].rect.x, "y", blockArray[row, col].rect.y)

def getIsometricBoardBounds(blockArray):
    # boardCoordinates = getCartesianBoardBounds()
    firstElem = blockArray[0, 0]
    lastElem = blockArray[blockRows - 1, blockCols - 1]
    topLeft = (firstElem.rect.x, firstElem.rect.y)
    # check this
    bottomRight = (lastElem.rect.x, lastElem.rect.y)
    return [topLeft, bottomRight]


## returns list with top left, top right, bottom left, bottom right coordinates
## each in a tuple
# def getCartesianBoardBounds(startX, startY, width, height):
#     boardCoordinates = []
#     boardCoordinates.append((startX, startY))
#     # boardCoordinates.append((startX + width, startY))
#     # boardCoordinates.append((startX, startY + height))
#     boardCoordinates.append((startX + width, startY + height))


