# creates the Character object and allows him to move

import numpy as np
import random
import pygame
from island import *
from variables import *

# character class that controls the main person
class Character(pygame.sprite.Sprite):
    def __init__(self, image, cellWidth, cellHeight, blockArray, cartesianBlockArray, offsetX, offsetY):
        super().__init__()
        self.cartBlockArray = cartesianBlockArray
        self.blockArray = blockArray
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        self.offsetX = offsetX
        self.offsetY = offsetY
        # scrolling loosely adapted (adjusted to fit isometric) from CMU Animations
        # Notes: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
        self.scrollX = 0
        self.scrollY = 0
        self.cartScrollX = 0
        self.cartScrollY = 0
        self.scrollMargin = 100
        # self.image = pygame.Surface([charWidth, charHeight])
        self.image = pygame.image.load(image).convert_alpha()
        self.scaleImage()
        self.findImageDimensions()
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.findIsometricBounds(self.blockArray)
        self.findCartesianBounds(self.cartBlockArray)
        self.rect.centerx, self.rect.centery = self.getRandomBoardCenter(self.blockArray)
        print("centerx, centery", self.rect.centerx, self.rect.centery)
        print("mins and maxs", self.cartMinX, self.cartMinY, self.cartMaxX, self.cartMaxY)
        self.justMoved = False

    def addScroll(self, scrollX, scrollY):
        self.scrollX += scrollX
        self.scrollY += scrollY
        cartScrollX, cartScrollY = self.convertIsometricToCartesian(scrollX, scrollY)
        self.cartScrollX += cartScrollX
        self.cartScrollY += cartScrollY

    # retrieves a random isometric board center
    def getRandomBoardCenter(self, blockArray):
        randRow = random.randint(0, blockRows - 1)
        randCol = random.randint(0, blockCols - 1)
        block = blockArray[randRow, randCol]
        centerX = (block.rect.centerx + block.rect.midtop[0]) // 2
        centerY = (block.rect.centery + block.rect.midtop[1]) // 2
        # print("block centers", block.rect.centerx, block.rect.centery)
        # print("midtop", block.rect.midtop)
        # print("average", (block.rect.centerx + block.rect.midtop[0]) // 2,
        #     (block.rect.centery + block.rect.midtop[1]) // 2)
        # centerX = block.rect.centerx
        # centerY = block.rect.centery
        return centerX, centerY
    
    def placeInCenterOfBlock(self):
        # self.rect.centerx -= 0.5 * self.boardCellHeight
        # self.rect.centery -= 0.25 * self.boardCellWidth
        self.rect.centerx -= 0.25 * self.boardCellHeight
        self.rect.centery += 0.5 * self.boardCellWidth
    
    def findIsometricBounds(self, blockArray):
        # organized top left, top right, bottom left, bottom right
        boardCoordinates = getBoardBounds(blockArray)
        self.minX = boardCoordinates[2][0] #+ self.boardCellWidth / 4
        self.minY = boardCoordinates[0][1] #+ self.boardCellHeight / 4
        self.maxX = boardCoordinates[1][0] #+ self.boardCellWidth / 4
        self.maxY = boardCoordinates[3][1] #+ self.boardCellHeight / 4
    
    def findCartesianBounds(self, cartBlockArray):
        # cartesianX, cartesianY = self.convertIsometricToCartesian(self.rect.centerx, self.rect.centery)
        # top left, top right, bottom left, bottom right
        # print("in character", self.cartBlockArray)
        cartBoard = getBoardBounds(cartBlockArray)
        # print("IN CHARACTER", cartBoard)
        self.cartMinX = cartBoard[0][0]
        self.cartMinY = cartBoard[0][1]
        self.cartMaxX = cartBoard[3][0]
        self.cartMaxY = cartBoard[3][1]
    
    def findIsometricCenters(self, blockArray):
        boardCenters = getIsometricBoardCenters(blockArray)
        self.minCenterX = boardCenters[2][0] 
        self.minCenterY = boardCenters[0][1]
        self.maxCenterX = boardCenters[1][0]
        self.maxCenterY = boardCenters[3][1]

    def convertIsometricToCartesian(self, isoX, isoY):
        cartesianX = (isoX + isoY * 2) / 2
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
        self.rect = self.image.get_rect()
    
    def getCartesianRow(self, isoX, isoY):
        cartesianX, cartesianY = self.convertIsometricToCartesian(self, isoX, isoY)
        row = (self.cartMaxY - (self.cartMaxY - cartesianY)) / self.boardCellWidth
        return row

    def getCartesianCol(self, isoX, isoY):
        cartesianX, cartesianY = self.convertIsometricToCartesian(self, isoX, isoY)
        col = (self.cartMaxX - (self.cartMaxX - cartesianX)) / self.boardCellWidth  
        return col

    def moveRight(self):
        print("right")
        if (not self.isWalkable(1, 0)):
            return
        self.rect.centerx += self.boardCellWidth
        self.rect.centery += 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
            # scrollX = self.boardCellWidth
            # scrollY = 0.5 * self.boardCellHeight
            scrollX = self.boardCellWidth / 2
            scrollY = (0.5 * self.boardCellHeight) / 2
            self.addScroll(scrollX, scrollY)
            self.justMoved = True
        
    def moveLeft(self):
        print("left")
        if (not self.isWalkable(-1, 0)):
            return
        self.rect.centerx -= self.boardCellWidth
        self.rect.centery -= 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
            # scrollX = -self.boardCellWidth
            # scrollY = -0.5 * self.boardCellHeight
            scrollX = -self.boardCellWidth / 2
            scrollY = (-0.5 * self.boardCellHeight) / 2
            self.addScroll(scrollX, scrollY)
            self.justMoved = True

    def moveUp(self):
        print("up")
        if (not self.isWalkable(0, -1)):
            return
        self.rect.centerx += self.boardCellWidth
        self.rect.centery -= 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
            # scrollX = self.boardCellWidth
            # scrollY = -0.5 * self.boardCellHeight
            scrollX = self.boardCellWidth / 2
            scrollY = (-0.5 * self.boardCellHeight) / 2
            self.addScroll(scrollX, scrollY)
            self.justMoved = True
 
    def moveDown(self):
        print("down")
        if (not self.isWalkable(0, 1)):
            return
        self.rect.centerx -= self.boardCellWidth
        self.rect.centery += 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
            # scrollX = -self.boardCellWidth
            # scrollY = 0.5 * self.boardCellHeight
            scrollX = -self.boardCellWidth / 2
            scrollY = (0.5 * self.boardCellHeight) / 2
            self.addScroll(scrollX, scrollY)
            self.justMoved = True
        

    def isWalkable(self, dx, dy):
        self.findCartesianBounds(self.cartBlockArray)
        self.cartX, self.cartY = self.convertIsometricToCartesian(self.rect.centerx - self.offsetX, 
            self.rect.centery - self.offsetY)
        self.cartX += startX #+ (self.boardCellWidth // 2)
        self.cartY += startY + (self.boardCellHeight / 2)
        # print("curr self.cartx, self.carty", self.cartX, self.cartY)
        # print("dx", dx, dx * self.boardCellWidth, "dy", dy, dy * self.boardCellHeight)
        newX = self.cartX + dx * self.boardCellWidth
        newY = self.cartY + dy * self.boardCellHeight
        # print("newx, newy", newX, newY)
        # print("cartmins and maxs", self.cartMinX, self.cartMinY, self.cartMaxX, self.cartMaxY)
        # print("less x", newX < self.cartMinX, "more x", newX > self.cartMaxX, 
        #     "less y", newY < self.cartMinY, "more y", newY > self.cartMaxY)
        for sprite in treeSprites:
            # print("NEW SPRITE")
            # print("centerx, centery", sprite.rect.centerx, self.rect.centery)
            treeX, treeY = sprite.convertIsometricToCartesian(sprite.rect.centerx
                - sprite.offsetX, self.rect.centery - sprite.offsetY)
            # print("treex, treey before", treeX, treeY)
            treeX += startX
            treeY += startY + (self.boardCellHeight / 2)
            # treeX += (self.boardCellWidth / 2)
            # treeY += (self.boardCellHeight / 2)
            # treeX += startX - (self.boardCellWidth/ 2)
            # treeY += startY
            # print("treeX, treeY", treeX, treeY)
            # print("treeX, treeY", treeX - (self.boardCellWidth/ 2), treeY - (self.boardCellHeight / 2))
            cellMinX = treeX - self.boardCellWidth / 2
            cellMaxX = treeX + self.boardCellWidth / 2
            cellMinY = treeY - self.boardCellHeight / 2
            cellMaxY = treeY + self.boardCellHeight / 2
            # print("cell mins and maxs", cellMinX, cellMinY, cellMaxX, cellMaxY)
            # print("more x", newX >= cellMinX, "less x", newX <= cellMaxX, "more y", 
            # newY >= cellMinY, "less y", newY <= cellMaxY)
            if ((newX >= cellMinX and newX <= cellMaxX) and (newY >= cellMinY 
                    and newY <= cellMaxY)):
                return False
        #     # if (newX == treeX and newY == treeY):
        #     #     return False
        if (newX < self.cartMinX or newX > self.cartMaxX or newY < self.cartMinY 
                or newY > self.cartMaxY):
            return False
        self.cartX = newX
        self.cartY = newY
        return True

    # loosely adapted from SideScroller2 example in 112 Notes to fit isometric 
    # coordinates and desired scrolling effect: 
    # http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
    def makePlayerVisible(self):
        isScrollable = False
        # cartScrollX = self.boardCellWidth * dx
        # cartScrollY = self.boardCellHeight * dy
        if (self.cartX < self.scrollMargin + self.scrollX):
            # self.scrollX = self.cartX - self.scrollMargin
            isScrollable = True
        elif (self.cartX + self.scrollMargin > self.scrollX + width):
            # self.scrollX = self.cartX + self.scrollMargin - width
            isScrollable = True
        if (self.cartY < self.scrollMargin + self.scrollY):
            # self.scrollY = self.cartY - self.scrollMargin
            isScrollable = True
        elif (self.cartY + self.scrollMargin > self.scrollX + height):
            # self.scrollX = self.cartX + self.scrollMargin - height
            isScrollable = True
        return isScrollable

    # fix to check within isometric board
    def jump(self, event):
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
        self.rect.centerx = posX
        self.rect.centery = posY

    def killEnemy(self, event):
        posX, posY = event.pos
        posX, posY = self.convertIsometricToCartesian(posX - self.offsetX, posY - self.offsetY)
        # posX += startX + self.boardCellWidth
        posX += startX - (self.boardCellWidth / 2)
        posY += startY + (self.boardCellHeight / 2)
        print("clicked", posX, posY)
        # print("cartmins and maxs", self.cartMinX, self.cartMinY, self.cartMaxX, self.cartMaxY)
        a1 = posX < self.cartMinX
        a2 = posX > self.cartMaxX
        a3 = posY < self.cartMinY
        a4 = posY > self.cartMaxY
        print("FIRST If less x", a1, "more x", a2, "less y", a3, "more y", a4)
        a = a1 or a2 or a3 or a4
        if (posX < self.cartMinX or posX > self.cartMaxX or posY < self.cartMinY or posY > self.cartMaxY):
            return
        for sprite in enemySprites:
            enemyX, enemyY = self.convertIsometricToCartesian(self.rect.centerx - self.offsetX,
                self.rect.centery - self.offsetY)
            enemyX += startX
            enemyY += startY + (self.boardCellHeight / 2)
            cellMinX = enemyX - self.boardCellWidth / 2
            cellMaxX = enemyX + self.boardCellWidth / 2
            cellMinY = enemyY - self.boardCellHeight / 2
            cellMaxY = enemyY + self.boardCellHeight / 2
            print("cell mins and maxs", cellMinX, cellMinY, cellMaxX, cellMaxY)
            print("more x", posX >= cellMinX, "less x", posX <= cellMaxX, "more y", 
                posY >= cellMinY, "less y", posY <= cellMaxY)
            if (posX >= cellMinX and posX <= cellMaxX and posY >= cellMinY and
                posY <= cellMaxY):
                sprite.kill()
                # self.enemyThread.stopRunning()
            #     return True
            # return False

def createCharacter(image, charSprites, cellWidth, cellHeight, blockArray, 
    cartesianBlockArray, offsetX, offsetY):
    character = Character(image, cellWidth, cellHeight, blockArray, 
        cartesianBlockArray, offsetX, offsetY)
    charSprites.add(character)
    return character