import pygame
import numpy as np
import random
from variables import *
from character import *
from island import *
# from resources import *
import resources
# from score import *
import score

class RawResources(pygame.sprite.Sprite):
    def __init__(self, image, character, blockArray, cartesianBlockArray, 
            inventoryBar, offsetX, offsetY, scaleLocation):
        super().__init__()
        self.character = character
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
        self.rect.centerx, self.rect.centery, self.block = self.getRandomBoardCenter(self.blockArray)
        self.originalX, self.originalY = self.rect.centerx, self.rect.centery
        # self.adjustBlockCenter()
        print("after placed", self.rect.centerx, self.rect.centery)
        self.findCartesianBounds(self.cartBlockArray)
    
    def scaleImage(self, image, rect, location):
        image = pygame.transform.scale(image, location)
        rect = image.get_rect()
        return image, rect

    def findBlockCenter(self, block):
        # centerX = (block.rect.centerx)
        # centerY = (block.rect.centery)
        centerX = (block.rect.centerx + block.rect.midtop[0]) / 2
        centerY = (block.rect.centery + block.rect.midtop[1]) / 2
        return centerX, centerY

    def pickRandomRowAndCol(self, boardRows, boardCols):
        randRow = random.randint(0, boardRows - 1)
        randCol = random.randint(0, boardCols - 1)
        return randRow, randCol
    
    def findCartesianBounds(self, cartBlockArray):
        cartBoard = getBoardBounds(cartBlockArray)
        self.cartMinX = cartBoard[0][0]
        self.cartMinY = cartBoard[0][1]
        self.cartMaxX = cartBoard[3][0]
        self.cartMaxY = cartBoard[3][1]
    
    def findOtherIslandCartesianBounds(self, cartBlockArray):
        # top left, top right, bottom left, bottom right
        cartBoard = getBoardBounds(cartBlockArray)
        cartMinX = cartBoard[0][0]
        cartMinY = cartBoard[0][1]
        cartMaxX = cartBoard[3][0]
        cartMaxY = cartBoard[3][1]
        return cartMinX, cartMinY, cartMaxX, cartMaxY
        
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

    def findOriginalCenter(self, block):
        trueCenterX = (2 * block.rect.centerx) - block.rect.midtop[0]
        trueCenterY = (2 * block.rect.centery) - block.rect.midtop[1]
        return trueCenterX, trueCenterY

    # fix bug to not place on trees or character
    def getRandomBoardCenter(self, blockArray):
        # global treeSprites
        # seenCenters = []
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
                return centerX, centerY, block
            count += 1
            if (count > maxVal):
                print("Try times exceeds max value")
        # for sprite in treeSprites:
        #     # trueCenterX, trueCenterY = self.findOriginalCenter(sprite.block)
        #     # seenCenters.append((trueCenterX, trueCenterY))
        #     # print("appending", sprite.rect.centerx, sprite.rect.centery)
        #     seenCenters.append((sprite.rect.centerx, sprite.rect.centery))
        # # print("after trees", seenCenters)
        # for sprite in ironSprites:
        #     seenCenters.append((sprite.rect.centerx, sprite.rect.centery))
        # for sprite in enemySprites:
        #     seenCenters.append((sprite.rect.centerx, sprite.rect.centery))
        # charCenterX = self.character.rect.centerx
        # charCenterY = self.character.rect.centery
        # seenCenters.append((charCenterX, charCenterY))
        # centerX, centerY = self.findBlockCenter(block)
        # # centerX, centerY = block.rect.centerx, block.rect.centery
        # # print("before while centerX and y", centerX, centerY)
        # # print("after character", seenCenters)
        # while ((centerX, centerY) in seenCenters):
        #     randRow, randCol = self.pickRandomRowAndCol(boardRows, boardCols)
        #     block = blockArray[randRow, randCol]
        #     centerX, centerY = self.findBlockCenter(block)
        #     # centerX, centerY = block.rect.centerx, block.rect.centery
        #     # print("currCenterX and y", centerX, centerY)
        # # print("placed")
        # return centerX, centerY, block


class Trees(RawResources):
    def __init__(self, image, character, blockArray, cartesianBlockArray, inventoryBar, offsetX, offsetY, location):
        super().__init__(image, character, blockArray, cartesianBlockArray, inventoryBar, offsetX, offsetY, location)
        self.wood = 0
        self.carbonDioxide = 10
        self.cutDown = False
    def removeTrees(self, event):
        posX, posY = event.pos
        # print("before offset", posX, posY)
        posX, posY = self.convertIsometricToCartesian(posX - self.offsetX, posY - self.offsetY)
        posX += startX - (self.boardCellWidth / 2)
        posY += startY + (self.boardCellHeight / 2)
        print("clicked raw resources", posX, posY)
        print("cartmins and maxs", self.cartMinX, self.cartMinY, self.cartMaxX, self.cartMaxY)
        a1 = posX < self.cartMinX
        a2 = posX > self.cartMaxX
        a3 = posY < self.cartMinY
        a4 = posY > self.cartMaxY
        print("FIRST If less x", a1, "more x", a2, "less y", a3, "more y", a4)
        a = a1 or a2 or a3 or a4
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
        print("cell mins and maxs", cellMinX, cellMinY, cellMaxX, cellMaxY)
        print("more x", posX >= cellMinX, "less x", posX <= cellMaxX, "more y", 
            posY >= cellMinY, "less y", posY <= cellMaxY)
        if (posX >= cellMinX and posX <= cellMaxX and posY >= cellMinY and
            posY <= cellMaxY):
            self.kill()
            self.block.isEmpty = True
            self.addWoodToInventory()
            score.pointsDict["trees collected"] += 1
            return True
        return False
    # log image from: https://www.deviantart.com/chunsmunkey/art/Pixel-Log-750792001
    def addWoodToInventory(self):
        logImage = "log.png"
        logResource = resources.Wood(logImage, "Wood", 1, self.inventoryBar)
        logResource.placeInInventory(0)
        resourceSprites.add(logResource)
        logResource.updateAmount(resources.Wood)
    
    def adjustBlockCenter(self):
        self.rect.centerx = (self.block.rect.centerx + self.block.rect.midtop[0]) / 2
        self.rect.centery = (self.block.rect.centery + self.block.rect.midtop[1]) / 2
        # return centerX, centerY

class RawIron(RawResources):
    def __init__(self, image, character, blockArray, cartesianBlockArray, inventoryBar, offsetX, offsetY, location):
        super().__init__(image, character, blockArray, cartesianBlockArray, inventoryBar, offsetX, offsetY, location)

    def adjustBlockCenter(self):
        self.rect.centerx = (self.block.rect.centerx)
        self.rect.centery = (self.block.rect.centery)
        # return centerX, centerY

    def addIronToInventory(self):
        self.block.isEmpty = True
        # picture from: http://iconbug.com/detail/icon/8273/minecraft-iron-ingot/
        ironImage = "metalBar.png"
        ironResource = resources.Iron(ironImage, "Iron", 2, self.inventoryBar)
        ironResource.placeInInventory(1)
        resourceSprites.add(ironResource)
        ironResource.updateAmount(resources.Iron)

# makes Tree objects to place on the board
def makeTrees(character, blockArray, cartBlockArray, inventoryBar, offsetX, offsetY, cellWidth, cellHeight, number):
    global treeSprites
    # tree image: https://www.reddit.com/r/PixelArt/comments/6ktv32/newbiecc_looking_for_tips_how_to_improve_this_tree/
    for i in range(number):
        image = "tree.png"
        location = (int(cellWidth * 1.5), int(cellHeight * 1.5))
        tree = Trees(image, character, blockArray, cartBlockArray, inventoryBar, offsetX, offsetY, location)
        print("in make trees", tree.rect.centerx, tree.rect.centery)
        treeSprites.add(tree)
        # for sprite in treeSprites:
        #     currx, curry = sprite.rect.centerx, sprite.rect.centery
        #     oldx, oldy = sprite.findOriginalCenter(sprite.block)
        #     originX, originY = sprite.originalX, sprite.originalY
        #     # convertx, converty = sprite.findBlockCenter(sprite.)
        #     print("after converted", currx, curry, "function", oldx, oldy, "true", originX, originY)

def placeIron(character, blockArray, cartBlockArray, inventoryBar, offsetX, offsetY, cellWidth, cellHeight):
    # picture from: http://iconbug.com/detail/icon/8273/minecraft-iron-ingot/
    image = "metalBar.png"
    location = (int(cellWidth * .6), int(cellHeight * .6))
    iron = RawIron(image, character, blockArray, cartBlockArray, inventoryBar, offsetX, offsetY, location)
    ironSprites.add(iron)

def sumCarbon():
    totCarbon = 0
    for sprite in treeSprites:
        totCarbon += sprite.carbonDioxide
    return totCarbon
