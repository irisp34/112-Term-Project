# This file creates a class that manages all the raw resources on the screen
# before they are collected by the user (ie trees and iron) and then updates
# the user's inventory once they are collected

import pygame
import numpy as np
import random
import variables
from character import *
from island import *
import resources
import score

class RawResources(pygame.sprite.Sprite):
    def __init__(self, image, character, blockArray, cartesianBlockArray, 
            inventoryBar, offsetX, offsetY, scaleLocation, island, position = None):
        super().__init__()
        self.character = character
        self.island = island
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        self.blockArray = blockArray
        self.cartBlockArray = cartesianBlockArray
        self.inventoryBar = inventoryBar
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.scaleLocation = scaleLocation
        self.image, self.rect = self.scaleImage(self.image, self.rect, self.scaleLocation)
        self.findCartesianBounds(self.cartBlockArray)
        if (position is not None):
            self.rect.centerx = position['x']
            self.rect.centery = position['y']
            self.row = position['row']
            self.col = position['col']
            self.block = blockArray[self.row, self.col]
            self.block.isEmpty = False
        elif (not variables.isBuildingProduction):
            self.rect.centerx, self.rect.centery, self.row, self.col, self.block = self.getRandomBoardCenter(self.blockArray)
        self.originalX, self.originalY = self.rect.centerx, self.rect.centery
    
    # scales an image to the appropriate size 
    def scaleImage(self, image, rect, location):
        image = pygame.transform.scale(image, location)
        rect = image.get_rect()
        return image, rect

    # finds the center of where the block is (with an adjustment for taller
    # images)
    def findBlockCenter(self, block):
        centerX = (block.rect.centerx + block.rect.midtop[0]) / 2
        centerY = (block.rect.centery + block.rect.midtop[1]) / 2
        return centerX, centerY

    # randomly generates a row and col based on the board size
    def pickRandomRowAndCol(self, boardRows, boardCols):
        randRow = random.randint(0, boardRows - 1)
        randCol = random.randint(0, boardCols - 1)
        return randRow, randCol
    
    # finds the bounds for a cartesian block array
    def findCartesianBounds(self, cartBlockArray):
        cartBoard = getBoardBounds(cartBlockArray)
        self.cartMinX = cartBoard[0][0]
        self.cartMinY = cartBoard[0][1]
        self.cartMaxX = cartBoard[3][0]
        self.cartMaxY = cartBoard[3][1]
    
    # functionality is similar to above function but can find for arrays other
    # than self.
    def findOtherIslandCartesianBounds(self, cartBlockArray):
        # top left, top right, bottom left, bottom right
        cartBoard = getBoardBounds(cartBlockArray)
        cartMinX = cartBoard[0][0]
        cartMinY = cartBoard[0][1]
        cartMaxX = cartBoard[3][0]
        cartMaxY = cartBoard[3][1]
        return cartMinX, cartMinY, cartMaxX, cartMaxY
    
    # finds bounds of an isometric array
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

# tree class which manages all trees on the board
class Trees(RawResources):
    def __init__(self, image, character, blockArray, cartesianBlockArray,
        inventoryBar, offsetX, offsetY, location, island, position = None):
        super().__init__(image, character, blockArray, cartesianBlockArray,
            inventoryBar, offsetX, offsetY, location, island, position)
        self.wood = 0
        self.carbonDioxide = 10
        self.cutDown = False

    # checks if the user has clicked to remove them and kills the sprite if they
    # did and adds it to the inventory
    def removeTrees(self, event):
        posX, posY = event.pos
        posX, posY = self.convertIsometricToCartesian(posX - self.offsetX, posY - self.offsetY)
        posX += startX - (self.boardCellWidth / 2)
        posY += startY + (self.boardCellHeight / 2)
        if (posX < self.cartMinX or posX > self.cartMaxX or posY < self.cartMinY or posY > self.cartMaxY):
            return
        treeX, treeY = self.convertIsometricToCartesian(self.rect.centerx - self.offsetX,
            self.rect.centery - self.offsetY)
        treeX += startX
        treeY += startY + (self.boardCellHeight / 2)
        cellMinX = treeX - self.boardCellWidth / 2
        cellMaxX = treeX + self.boardCellWidth / 2
        cellMinY = treeY - self.boardCellHeight / 2
        cellMaxY = treeY + self.boardCellHeight / 2
        if (posX >= cellMinX and posX <= cellMaxX and posY >= cellMinY and
            posY <= cellMaxY):
            self.block.isEmpty = True
            self.kill()
            self.addWoodToInventory()
            score.pointsDict["trees collected"] += 1
            return True
        return False

    # adds the tree to inventory
    # log image from: https://www.deviantart.com/chunsmunkey/art/Pixel-Log-750792001
    def addWoodToInventory(self):
        logImage = "log.png"
        logResource = resources.Wood(logImage, "Wood", 1, self.inventoryBar)
        logResource.placeInInventory(0)
        variables.resourceSprites.add(logResource)
        logResource.updateAmount(resources.Wood)

class RawIron(RawResources):
    def __init__(self, image, character, blockArray, cartesianBlockArray,
        inventoryBar, offsetX, offsetY, location, island, position = None):
        super().__init__(image, character, blockArray, cartesianBlockArray,
            inventoryBar, offsetX, offsetY, location, island, position)

    def addIronToInventory(self):
        if (not variables.isBuildingProduction):
            self.block.isEmpty = True
        # picture from: http://iconbug.com/detail/icon/8273/minecraft-iron-ingot/
        ironImage = "metalBar.png"
        ironResource = resources.Iron(ironImage, "Iron", 2, self.inventoryBar)
        ironResource.placeInInventory(1)
        variables.resourceSprites.add(ironResource)
        ironResource.updateAmount(resources.Iron)

# makes Tree objects to place on the board
def makeTrees(character, blockArray, cartBlockArray, inventoryBar, offsetX,
    offsetY, cellWidth, cellHeight, number, island, treeList = None):
    # tree image: https://www.reddit.com/r/PixelArt/comments/6ktv32/newbiecc_looking_for_tips_how_to_improve_this_tree/
    count = number
    if (treeList is not None):
        count = len(treeList)

    image = "tree.png"
    location = (int(cellWidth * 1.5), int(cellHeight * 1.5))
    for i in range(count):
        tree = None
        if (treeList is not None):
            treeDic = treeList[i]
            tree = Trees(image, character, blockArray, cartBlockArray, 
                inventoryBar, offsetX, offsetY, location, island, treeDic)
        else:
            tree = Trees(image, character, blockArray, cartBlockArray,
                inventoryBar, offsetX, offsetY, location, island)
        variables.treeSprites.add(tree)

# creates RawIron instances to place on the board
def placeIron(character, blockArray, cartBlockArray, inventoryBar, offsetX,
    offsetY, cellWidth, cellHeight, island, position = None):
    # picture from: http://iconbug.com/detail/icon/8273/minecraft-iron-ingot/
    image = "metalBar.png"
    location = (int(cellWidth * .6), int(cellHeight * .6))
    iron = RawIron(image, character, blockArray, cartBlockArray, inventoryBar,
        offsetX, offsetY, location, island, position)
    variables.ironSprites.add(iron)

# counts how many trees are on an island
def sumTreesOnIsland(island):
    count = 0
    for tree in treeSprites:
        if (tree.island == island):
            count += 1
    return count
