import pygame
import numpy as np
import random
from variables import *
from character import *
from island import *
from resources import *

class Trees(pygame.sprite.Sprite):
    def __init__(self, character, blockArray, cartesianBlockArray, inventoryBar):
        super().__init__()
        self.character = character
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        self.blockArray = blockArray
        self.cartBlockArray = cartesianBlockArray
        self.inventoryBar = inventoryBar
        # tree image: https://www.reddit.com/r/PixelArt/comments/6ktv32/newbiecc_looking_for_tips_how_to_improve_this_tree/
        self.image = pygame.image.load("tree.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.image, self.rect = self.scaleImage(self.image, self.rect)
        self.rect.centerx, self.rect.centery = self.getRandomBoardCenter(blockArray1)
        self.findCartesianBounds(self.cartBlockArray)
        self.wood = 0
        self.carbonDioxide = 10
        self.cutDown = False
    
    def scaleImage(self, image, rect):
        location = (int(self.boardCellWidth * 1.5), int(self.boardCellHeight * 1.5))
        image = pygame.transform.scale(image, location)
        rect = image.get_rect()
        return image, rect

    def findBlockCenter(self, block):
        centerX = (block.rect.centerx + block.rect.midtop[0]) // 2
        centerY = (block.rect.centery + block.rect.midtop[1]) // 2
        return centerX, centerY

    def pickRandomRowAndCol(self, boardRows, boardCols):
        randRow = random.randint(0, boardRows - 1)
        randCol = random.randint(0, boardCols - 1)
        return randRow, randCol
    
    def removeTrees(self, event, offsetX, offsetY):
        posX, posY = event.pos
        # print("before offset", posX, posY)
        posX, posY = self.convertIsometricToCartesian(posX - offsetX, posY - offsetY)
        # posX += startX + self.boardCellWidth
        posX += startX - (self.boardCellWidth / 2)
        posY += startY + (self.boardCellHeight / 2)
        # print("clicked", posX, posY)
        # print("cartmins and maxs", self.cartMinX, self.cartMinY, self.cartMaxX, self.cartMaxY)
        # a1 = posX < self.cartMinX
        # a2 = posX > self.cartMaxX
        # a3 = posY < self.cartMinY
        # a4 = posY > self.cartMaxY
        # print("FIRST If less x", a1, "more x", a2, "less y", a3, "more y", a4)
        # a = a1 or a2 or a3 or a4
        if (posX < self.cartMinX or posX > self.cartMaxX or posY < self.cartMinY or posY > self.cartMaxY):
            # print("here")
            return
        treeX, treeY = self.convertIsometricToCartesian(self.rect.centerx - offsetX,
            self.rect.centery - offsetY)
        treeX += startX
        treeY += startY + (self.boardCellHeight / 2)
        cellMinX = treeX - self.boardCellWidth / 2
        cellMaxX = treeX + self.boardCellWidth / 2
        cellMinY = treeY - self.boardCellHeight / 2
        cellMaxY = treeY + self.boardCellHeight / 2
        # print("cell mins and maxs", cellMinX, cellMinY, cellMaxX, cellMaxY)
        # print("more x", posX >= cellMinX, "less x", posX <= cellMaxX, "more y", 
        #     posY >= cellMinY, "less y", posY <= cellMaxY)
        if (posX >= cellMinX and posX <= cellMaxX and posY >= cellMinY and
            posY <= cellMaxY):
            self.kill()
            self.wood += 1
            self.addWoodToInventory()
            return True
        return False
    
    # log image from: https://www.deviantart.com/chunsmunkey/art/Pixel-Log-750792001
    def addWoodToInventory(self):
        logImage = "log.png"
        logResource = Resource(logImage, "Wood", 1, self.wood, self.inventoryBar)
        logResource.placeInInventory()
        resourceSprites.add(logResource)
        print("resourceSprites", resourceSprites)

    def findCartesianBounds(self, cartBlockArray):
        cartBoard = getBoardBounds(cartBlockArray)
        self.cartMinX = cartBoard[0][0]
        self.cartMinY = cartBoard[0][1]
        self.cartMaxX = cartBoard[3][0]
        self.cartMaxY = cartBoard[3][1]
        
    def findIsometricBounds(self, blockArray):
        # organized top left, top right, bottom left, bottom right
        boardCoordinates = getBoardBounds(blockArray)
        self.isoMinX = boardCoordinates[2][0] 
        self.isoMinY = boardCoordinates[0][1]
        self.isoMaxX = boardCoordinates[1][0] 
        self.isoMaxY = boardCoordinates[3][1] 
    
    def convertIsometricToCartesian(self, isoX, isoY):
        cartesianX = (isoX + isoY * 2) / 2
        cartesianY = (2*isoY - isoX) / 2
        return (cartesianX, cartesianY)

    def convertCartesianToIsometric(self, cartX, cartY):
        isoX = (cartX - cartY)
        isoY = ((cartX + cartY) / 2)
        return (isoX, isoY)

    # retrieves a random isometric board center that doesn't already have
    # something on it to place a tree on
    def getRandomBoardCenter(self, blockArray):
        seenCenters = []
        for sprite in treeSprites:
            seenCenters.append((sprite.rect.centerx, sprite.rect.centery))
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
            centerX, centerY = self.findBlockCenter(block)
        return centerX, centerY
    
def sumCarbon(self):
    totCarbon = 0
    for sprite in treeSprites:
        totCarbon += sprite.carbonDioxide
    return totCarbon