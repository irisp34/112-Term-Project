# generates Block objects to encompass a map and makes that map 2.5D

import pygame
import numpy as np
import os
from variables import *


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
        self.rect.centerx = (self.rect[0] + self.rect[2]) // 2
        self.rect.centery = (self.rect[1] + self.rect[3]) // 2
        self.margin = 5
        self.image = self.scaleImage()
        
        # position of top left corner
        self.rect.x = posX
        self.rect.y = posY
        # halfWidth = self.cellWidth // 2
        # halfHeight = self.cellHeight // 2
        # self.rect.centerx = self.rect.x + halfWidth
        # self.rect.centery = self.rect.y + halfHeight
    
    def makeBlockIsometric(self, row, col):
        # self.rotatedImage = self.image
        # row = row + 1
        # col = col + 1
        self.angle = 45
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.cellWidth = self.cellWidth * 2
        self.image = self.scaleImage()
        self.convertCartesianToIsometric(row, col)
    
    def convertCartesianToIsometric(self, row, col):
        halfWidth = self.cellWidth / 2
        halfHeight = self.cellHeight / 2
        # offsetX = (width // 2) - self.startX
        # offsetY = (height // 2) - self.startY
        self.rect.x = ((col - row) * halfWidth) + offsetX
        self.rect.y = ((row + col) * halfHeight) + offsetY
        # self.rect.centerx = self.rect.x + halfWidth
        # self.rect.centery = self.rect.y + halfHeight
    
    def scaleImage(self):
        self.image = pygame.transform.scale(self.image, (self.cellWidth, self.cellHeight))
        self.cellWidth, self.cellHeight = self.image.get_size()
        self.rect = self.image.get_rect()
        return self.image

def findIslandBasePoints(blockArray):
    boardCorners = getBoardCorners(blockArray)
    topLeft, topRight, bottomLeft, bottomRight = boardCorners
    leftTopVertexX = bottomLeft.rect.left
    leftTopVertexY = (bottomLeft.rect.top + bottomLeft.rect.bottom) // 2
    midTopVertexX = (bottomRight.rect.left + bottomRight.rect.right) // 2
    midTopVertexY = bottomRight.rect.bottom
    rightTopVertexX = topRight.rect.right
    rightTopVertexY = (topRight.rect.top + topRight.rect.bottom) // 2
    leftBottomVertexX = leftTopVertexX
    leftBottomVertexY = leftTopVertexY + height//4
    midBottomVertexY = midTopVertexY + height//4
    midBottomVertexX = midTopVertexX
    rightBottomVertexY = rightTopVertexY + height//4
    rightBottomVertexX = rightTopVertexX
    pointsLeft = ((leftTopVertexX, leftTopVertexY), (midTopVertexX, midTopVertexY), 
        (midBottomVertexX, midBottomVertexY), (leftBottomVertexX, leftBottomVertexY))
    pointsRight = ((midTopVertexX, midTopVertexY), (midBottomVertexX, midBottomVertexY),
        (rightBottomVertexX, rightBottomVertexY), (rightTopVertexX, rightTopVertexY))
    return pointsLeft, pointsRight 


# adds Block instances to the array
def addBlockToArray(blockArray, block, row, col):
    blockArray[row, col] = block 

# generates a new Block with the correct properties
def createBlock(blockSprites, blockArray, cartesianBlockArray, cellWidth, cellHeight, color, posX,
                posY, startX, startY, row, col):
    block1 = Block(cellWidth, cellHeight, color, posX, posY, startX, startY)
    block2 = Block(cellWidth, cellHeight, color, posX, posY, startX, startY)
    addBlockToArray(blockArray, block1, row, col)
    addBlockToArray(cartesianBlockArray, block2, row, col)
    blockSprites.add(block1)

# loops through the desired rows and columns for the board to make the entire
# board
def make2DBoard(blockSprites, blockArray, cartesianBlockArray, blockRows, 
                blockCols, cellWidth, cellHeight, startX, startY):
    newStartX, newStartY = startX - cellWidth, startY - cellHeight
    color = (255, 0, 255)
    for row in range(blockRows):
        newStartX += cellWidth
        for col in range(blockCols):
            newStartY += cellHeight
            createBlock(blockSprites, blockArray, cartesianBlockArray, cellWidth, cellHeight, color,
                        newStartX, newStartY, startX, startY, row, col)
        newStartY = startY - cellHeight

def makeBoardIsometric(blockArray):
    for row in range(blockArray.shape[0]):
        for col in range(blockArray.shape[1]):
            print("before x",blockArray[row, col].rect.x, "y", blockArray[row, col].rect.y)
            blockArray[row, col].makeBlockIsometric(row, col)
            print("after x", blockArray[row, col].rect.x, "y", blockArray[row, col].rect.y)

def getBoardCorners(blockArray):
    topLeftCorner = blockArray[0, 0]
    topRightCorner = blockArray[0, blockCols - 1]
    bottomLeftCorner = blockArray[blockRows - 1, 0]
    bottomRightCorner = blockArray[blockRows - 1, blockCols - 1]
    return (topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner)

def getIsometricBoardBounds(blockArray):
    # boardCoordinates = getCartesianBoardBounds()
    topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner = getBoardCorners(blockArray)
    topLeft = (topLeftCorner.rect.x, topLeftCorner.rect.y)
    topRight = (topRightCorner.rect.x, topRightCorner.rect.y)
    bottomLeft = (bottomLeftCorner.rect.x, bottomLeftCorner.rect.y)
    bottomRight = (bottomRightCorner.rect.x, bottomRightCorner.rect.y)
    return [topLeft, topRight, bottomLeft, bottomRight]

def getIsometricBoardCenters(blockArray):
    topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner = getBoardCorners(blockArray)
    topLeft = (topLeftCorner.rect.centerx, topLeftCorner.rect.centery)
    topRight = (topRightCorner.rect.centerx, topRightCorner.rect.centery)
    bottomLeft = (bottomLeftCorner.rect.centerx, bottomLeftCorner.rect.centery)
    bottomRight = (bottomRightCorner.rect.centerx, bottomRightCorner.rect.centery)
    return [topLeft, topRight, bottomLeft, bottomRight]

# returns list with top left, top right, bottom left, bottom right coordinates
# each in a tuple
# take out width height when this works
def getCartesianBoardBounds(cartesianBlockArray):
    # boardCoordinates = []
    # maxX = startX + (blockCols * cellWidth) + offsetX
    # maxY = startY + (blockRows * cellHeight) + offsetY
    # # top left
    # boardCoordinates.append((startX + offsetX, startY + offsetY))
    # # top right
    # boardCoordinates.append((maxX, startY + offsetY))
    # # bottom left
    # boardCoordinates.append((startX + offsetX, maxY))
    # # bottom right
    # boardCoordinates.append((maxX, maxY))
    # return boardCoordinates
    # print("cartesianBlockArray", cartesianBlockArray)
    boardCorners = getBoardCorners(cartesianBlockArray)
    topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner = boardCorners
    topLeft = (topLeftCorner.rect.x, topLeftCorner.rect.y)
    topRight = (topRightCorner.rect.x, topRightCorner.rect.y)
    bottomLeft = (bottomLeftCorner.rect.x, bottomLeftCorner.rect.y)
    bottomRight = (bottomRightCorner.rect.x, bottomRightCorner.rect.y)
    return [topLeft, topRight, bottomLeft, bottomRight]



