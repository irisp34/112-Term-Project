# creates the Character object and allows him to move

import numpy as np
import random
import pygame
from island import *
from variables import *

# character class that controls the main person
class Character(pygame.sprite.Sprite):
    def __init__(self, image, cellWidth, cellHeight, cartesianBlockArray):
        super().__init__()
        self.cartBlockArray = cartesianBlockArray
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        # self.image = pygame.Surface([charWidth, charHeight])
        self.image = pygame.image.load(image).convert_alpha()
        self.scaleImage()
        self.findImageDimensions()
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.findIsometricBounds()
        self.findCartesianBounds()
        # self.rect.centerx = blockArray[blockRows - 1, blockCols - 1].rect.centerx
        # self.rect.centery = blockArray[blockRows - 1, blockCols - 1].rect.centery
        # print("centers", self.rect.centerx, self.rect.centery)
        self.rect.centerx, self.rect.centery = self.getRandomBoardCenter()
        self.cartX, self.cartY = self.convertIsometricToCartesian(self.rect.centerx - offsetX, self.rect.centery - offsetY)
        print("cartX, cartY", self.cartX, self.cartY)
        print("mins and maxs", self.cartMinX, self.cartMinY, self.cartMaxX, self.cartMaxY)
        # self.placeInCenterOfBlock()
        # print("corrected", self.rect.x, self.rect.x)

    # retrieves a random isometric board center
    def getRandomBoardCenter(self):
        randRow = random.randint(0, blockRows - 1)
        randCol = random.randint(0, blockCols - 1)
        block = blockArray[randRow, randCol]
        centerX = block.rect.centerx
        centerY = block.rect.centery
        return centerX, centerY
    
    def placeInCenterOfBlock(self):
        # self.rect.x -= 0.5 * self.boardCellHeight
        # self.rect.y -= 0.25 * self.boardCellWidth
        self.rect.x -= 0.25 * self.boardCellHeight
        self.rect.y += 0.5 * self.boardCellWidth

    
    def findIsometricBounds(self):
        # organized top left, top right, bottom left, bottom right
        boardCoordinates = getIsometricBoardBounds(blockArray)
        # print("board coor", boardCoordinates)
        self.minX = boardCoordinates[2][0] #+ self.boardCellWidth / 4
        self.minY = boardCoordinates[0][1] #+ self.boardCellHeight / 4
        self.maxX = boardCoordinates[1][0] #+ self.boardCellWidth / 4
        self.maxY = boardCoordinates[3][1] #+ self.boardCellHeight / 4
    
    def findCartesianBounds(self):
        # cartesianX, cartesianY = self.convertIsometricToCartesian(self.rect.x, self.rect.y)
        # top left, top right, bottom left, bottom right
        # print("in character", self.cartBlockArray)
        cartBoard = getCartesianBoardBounds(self.cartBlockArray)
        self.cartMinX = cartBoard[0][0]
        self.cartMinY = cartBoard[0][1]
        self.cartMaxX = cartBoard[3][0]
        self.cartMaxY = cartBoard[3][1]
    
    def findIsometricCenters(self):
        boardCenters = getIsometricBoardCenters(blockArray)
        self.minCenterX = boardCenters[2][0] 
        self.minCenterY = boardCenters[0][1]
        self.maxCenterX = boardCenters[1][0]
        self.maxCenterY = boardCenters[3][1]

    def convertIsometricToCartesian(self, isoX, isoY):
        cartesianX = (isoX + isoY * 2) / 2
        # cartesianY = -isoX + cartesianX
        cartesianY = (2*isoY - isoX) / 2
        return (cartesianX, cartesianY)

    def convertCartesianToIsometric(self, cartX, cartY):
        isoX = (cartX - cartY)
        isoY = ((cartX + cartY) / 2)
        return (isoX, isoY)
    
    def findImageDimensions(self):
        self.charWidth, self.charHeight = self.image.get_size()

    def scaleImage(self):
        location = (self.boardCellWidth, self.boardCellHeight)
        self.image = pygame.transform.scale(self.image, location)
    
    def getCartesianRow(self, isoX, isoY):
        cartesianX, cartesianY = self.convertIsometricToCartesian(self, isoX, isoY)
        row = (self.cartMaxY - (self.cartMaxY - cartesianY)) / self.boardCellWidth
        return row

    def getCartesianCol(self, isoX, isoY):
        cartesianX, cartesianY = self.convertIsometricToCartesian(self, isoX, isoY)
        col = (self.cartMaxX - (self.cartMaxX - cartesianX)) / self.boardCellWidth  
        return col

    def moveRight(self):
        # still debugging bounded movement
        # print("rectx, recty", self.rect.x, self.rect.y)
        print("right")
        if (not self.walkable(1, 0)):
            return
        # cartesianX, cartesianY = self.convertIsometricToCartesian(self.rect.x, self.rect.y)
        # # find current col
        # # col = (self.cartMaxX - (self.cartMaxX - cartesianX)) / self.boardCellWidth  
        # print("x, y", cartesianX, cartesianY)
        # print("back", self.convertCartesianToIsometric(cartesianX, cartesianY))
        # temp = cartesianX + self.boardCellWidth
        # print("plus cell width", temp)
        # print("cartmax", self.cartMaxX)
        # # print("print offsets", offsetX, offsetY)
        # # print("with offset", self.cartMaxX + offsetX)
        # # print("x edge", startX + (blockCols * self.boardCellWidth))
        # if (temp < self.cartMaxX):
        #     self.rect.x += self.boardCellWidth
        #     self.rect.y += 0.5 * self.boardCellHeight

        self.rect.x += self.boardCellWidth
        self.rect.y += 0.5 * self.boardCellHeight
        
    def moveLeft(self):
        print("left")
        if (not self.walkable(-1, 0)):
            return
        self.rect.x -= self.boardCellWidth
        self.rect.y -= 0.5 * self.boardCellHeight

    def moveUp(self):
        print("up")
        if (not self.walkable(0, -1)):
            return
        self.rect.y -= 0.5 * self.boardCellHeight
        self.rect.x += self.boardCellWidth
 
    def moveDown(self):
        print("down")
        if (not self.walkable(0, 1)):
            return
        self.rect.y += 0.5 * self.boardCellHeight
        self.rect.x -= self.boardCellWidth

    def jump(self, posX, posY):
        print("jump after", posX, posX)
        self.rect.x = posX
        self.rect.y = posY

    def walkable(self, dX, dY):
        print("curr self.cartx, self.carty", self.cartX, self.cartY)
        newX = self.cartX + dX * self.boardCellWidth
        newY = self.cartX + dY * self.boardCellHeight
        print("newx, newy", newX, newY)
        print("cartmins and maxs", self.cartMinX, self.cartMinY, self.cartMaxX, self.cartMaxY)
        print("less x", newX < self.cartMinX, "more x", newX > self.cartMaxX, 
            "less y", newY < self.cartMinY, "more y", newY > self.cartMaxY)
        if (newX < self.cartMinX or newX > self.cartMaxX or newY < self.cartMinY or newY > self.cartMaxY):
            return False
        self.cartX = newX
        self.cartY = newY
        return True

    # fix to check within isometric board
    def mousePressed(self, event):
        posX, posY = event.pos
        print("cartesian", posX, posY)
        posX = posX - self.charWidth // 2
        if (posX < 0):
            posX = 0
        elif (posX + self.charWidth > width):
            posX = width - self.charWidth
        posY = posY - self.charHeight // 2
        if (posY < 0):
            posY = 0
        elif (posY + self.charHeight > height):
            posY = height - self.charHeight
        self.jump(posX, posY)

def createCharacter(image, charSprites, cellWidth, cellHeight, cartesianBlockArray):
    character = Character(image, cellWidth, cellHeight, cartesianBlockArray)
    charSprites.add(character)
    return character