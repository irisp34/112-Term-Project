# creates the Character object and allows him to move based on where he can
# Constrains motion based on other elements on the board and controls both the
# main character and the enemy

import numpy as np
import random
import pygame
from island import *
from buildings import *
import variables
import score


# character class that controls the main person
class Character(pygame.sprite.Sprite):
    def __init__(self, image, cellWidth, cellHeight, blockArray,
        cartesianBlockArray, offsetX, offsetY, characterPosition =  None):
        super().__init__()
        self.cartBlockArray = cartesianBlockArray
        self.blockArray = blockArray
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.scrollMargin = 150
        self.image = pygame.image.load(image).convert_alpha()
        self.scaleImage()
        self.findImageDimensions()
        self.rect = self.image.get_rect()
        self.findIsometricBounds(self.blockArray)
        self.findCartesianBounds(self.cartBlockArray)
        # sets the character's position if the game is continuing from last time
        if (characterPosition is not None):
            self.rect.centerx = characterPosition["x"]
            self.rect.centery = characterPosition["y"]
            self.scrollX = characterPosition["scrollX"]
            self.scrollY = characterPosition["scrollY"]
            self.cartScrollX = characterPosition["cartScrollX"]
            self.cartScrollY = characterPosition["cartScrollY"]
        else:
            self.rect.centerx, self.rect.centery = self.getRandomBoardCenter(self.blockArray)
            # scrolling loosely adapted (adjusted to fit isometric) from CMU Animations
            # Notes: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
            self.scrollX = 0
            self.scrollY = 0
            self.cartScrollX = 0
            self.cartScrollY = 0
        self.justMoved = False

    # adds scrolls to the character
    def addScroll(self, scrollX, scrollY):
        self.scrollX += scrollX
        self.scrollY += scrollY
        cartScrollX, cartScrollY = self.convertIsometricToCartesian(scrollX, scrollY)
        self.cartScrollX += cartScrollX
        self.cartScrollY += cartScrollY

    # retrieves a random isometric board center
    def getRandomBoardCenter(self, blockArray):
        randRow = random.randint(0, variables.blockRows - 1)
        randCol = random.randint(0, variables.blockCols - 1)
        block = blockArray[randRow, randCol]
        centerX = (block.rect.centerx + block.rect.midtop[0]) // 2
        centerY = (block.rect.centery + block.rect.midtop[1]) // 2
        return centerX, centerY
    
    def placeInCenterOfBlock(self):
        self.rect.centerx -= 0.25 * self.boardCellHeight
        self.rect.centery += 0.5 * self.boardCellWidth
    
    # finds the boundaries of the board in isometric
    def findIsometricBounds(self, blockArray):
        # organized top left, top right, bottom left, bottom right
        boardCoordinates = getBoardBounds(blockArray)
        self.minX = boardCoordinates[2][0]
        self.minY = boardCoordinates[0][1]
        self.maxX = boardCoordinates[1][0]
        self.maxY = boardCoordinates[3][1]
    
    # finds the boundaries of the board in cartesian
    def findCartesianBounds(self, cartBlockArray):
        # top left, top right, bottom left, bottom right
        cartBoard = getBoardBounds(cartBlockArray)
        self.cartMinX = cartBoard[0][0]
        self.cartMinY = cartBoard[0][1]
        self.cartMaxX = cartBoard[3][0]
        self.cartMaxY = cartBoard[3][1]
    
    # takes in another block array and finds those cartesian bounds
    def findOtherIslandCartesianBounds(self, cartBlockArray):
        # top left, top right, bottom left, bottom right
        cartBoard = getBoardBounds(cartBlockArray)
        cartMinX = cartBoard[0][0]
        cartMinY = cartBoard[0][1]
        cartMaxX = cartBoard[3][0]
        cartMaxY = cartBoard[3][1]
        return cartMinX, cartMinY, cartMaxX, cartMaxY
    
    # finds the boundaries of the centers of blocks in a certain island in isometric
    def findIsometricCenters(self, blockArray):
        boardCenters = getIsometricBoardCenters(blockArray)
        self.minCenterX = boardCenters[2][0] 
        self.minCenterY = boardCenters[0][1]
        self.maxCenterX = boardCenters[1][0]
        self.maxCenterY = boardCenters[3][1]

    # takes in two isometric coordinates and converts them to cartesian
    def convertIsometricToCartesian(self, isoX, isoY):
        cartesianX = (isoX + isoY * 2) / 2
        cartesianY = (2 * isoY - isoX) / 2
        return (cartesianX, cartesianY)

    # takes in two cartesian coordinates and converts them to isometric
    def convertCartesianToIsometric(self, cartX, cartY):
        isoX = (cartX - cartY)
        isoY = ((cartX + cartY) / 2)
        return (isoX, isoY)
    
    # determines the size of the image
    def findImageDimensions(self):
        self.charWidth, self.charHeight = self.image.get_size()

    # scales the image to fit the size of a board square
    def scaleImage(self):
        location = (int (self.boardCellWidth), int(self.boardCellHeight))
        self.image = pygame.transform.scale(self.image, location)
        self.rect = self.image.get_rect()
    
    # returns the current cartesian row that the character is in
    def getCartesianRow(self, isoX, isoY):
        cartesianX, cartesianY = self.convertIsometricToCartesian(self, isoX, isoY)
        row = (self.cartMaxY - (self.cartMaxY - cartesianY)) / self.boardCellWidth
        return row

    # returns the current cartesian col that the character is in
    def getCartesianCol(self, isoX, isoY):
        cartesianX, cartesianY = self.convertIsometricToCartesian(self, isoX, isoY)
        col = (self.cartMaxX - (self.cartMaxX - cartesianX)) / self.boardCellWidth  
        return col

    # checks if the character can move right and adds to the scroll if necessary
    def moveRight(self):
        if (not self.isWalkable(1, 0)):
            return
        self.rect.centerx += self.boardCellWidth
        self.rect.centery += 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
            scrollX = self.boardCellWidth
            scrollY = (0.5 * self.boardCellHeight)
            self.addScroll(scrollX, scrollY)
            self.justMoved = True
        
    def moveLeft(self):
        if (not self.isWalkable(-1, 0)):
            return
        self.rect.centerx -= self.boardCellWidth
        self.rect.centery -= 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
            scrollX = -self.boardCellWidth
            scrollY = (-0.5 * self.boardCellHeight)
            self.addScroll(scrollX, scrollY)
            self.justMoved = True

    def moveUp(self):
        if (not self.isWalkable(0, -1)):
            return
        self.rect.centerx += self.boardCellWidth
        self.rect.centery -= 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
            scrollX = self.boardCellWidth
            scrollY = (-0.5 * self.boardCellHeight)
            self.addScroll(scrollX, scrollY)
            self.justMoved = True
 
    def moveDown(self):
        if (not self.isWalkable(0, 1)):
            return
        self.rect.centerx -= self.boardCellWidth
        self.rect.centery += 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
            scrollX = -self.boardCellWidth
            scrollY = (0.5 * self.boardCellHeight)
            self.addScroll(scrollX, scrollY)
            self.justMoved = True
        
    # checks if the place that the character is trying to walk to has something
    # else that should impede movement. Returns False if it is a valid place
    # for the character to walk to
    def isWalkable(self, dx, dy):
        self.findCartesianBounds(self.cartBlockArray)
        self.cartX, self.cartY = self.convertIsometricToCartesian(self.rect.centerx - self.offsetX, 
            self.rect.centery - self.offsetY)
        self.cartX += startX
        self.cartY += startY + (self.boardCellHeight / 2)
        newX = self.cartX + dx * self.boardCellWidth
        newY = self.cartY + dy * self.boardCellHeight
        for sprite in treeSprites:
            treeX, treeY = sprite.convertIsometricToCartesian(sprite.rect.centerx
                - sprite.offsetX, sprite.rect.centery - sprite.offsetY)
            treeX += startX
            treeY += startY + (self.boardCellHeight / 2)
            cellMinX = treeX - self.boardCellWidth / 2
            cellMaxX = treeX + self.boardCellWidth / 2
            cellMinY = treeY - self.boardCellHeight / 2
            cellMaxY = treeY + self.boardCellHeight / 2
            if ((newX >= cellMinX and newX <= cellMaxX) and (newY >= cellMinY 
                    and newY <= cellMaxY)):
                return False
        # checks if the character is trying to walk into a building
        for sprite in buildingSprites:
            if (isinstance(sprite, Farm)):
                farmX, farmY = sprite.convertIsometricToCartesian(sprite.rect.centerx
                    - sprite.offsetX, sprite.rect.centery - sprite.offsetY)
                farmX += farmX
                farmY += farmY + (self.boardCellHeight / 2)
                cellMinX = farmX - self.boardCellWidth 
                cellMaxX = farmX + self.boardCellWidth
                cellMinY = farmY - self.boardCellHeight / 2
                cellMaxY = farmY + self.boardCellHeight / 2
                if ((newX >= cellMinX and newX <= cellMaxX) and (newY >= cellMinY 
                        and newY <= cellMaxY)):
                    return False
            elif (isinstance(sprite, Factory)):
                factoryX, factoryY = sprite.convertIsometricToCartesian(sprite.rect.centerx
                - sprite.offsetX, sprite.rect.centery - sprite.offsetY)
                factoryX += startX
                factoryY += startY + (self.boardCellHeight / 2)
                cellMinX = factoryX - self.boardCellWidth / 2
                cellMaxX = factoryX + self.boardCellWidth / 2
                cellMinY = factoryY - self.boardCellHeight / 2
                cellMaxY = factoryY + self.boardCellHeight / 2
                if ((newX >= cellMinX and newX <= cellMaxX) and (newY >= cellMinY 
                        and newY <= cellMaxY)):
                    return False
        # check if out of island 1
        if (newX < self.cartMinX or newX > self.cartMaxX or newY < self.cartMinY 
                or newY > self.cartMaxY):
            if (len(bridgeSprites) != 0):
                if (self.canWalkAcrossBridge(newX, newY)):
                    self.setNewPosition(newX, newY)
                    return True
            # sets new boundaries if the character can walk to island 2 and is
            # doing so
            if (variables.walkToIsland2):
                cartMinX2, cartMinY2, cartMaxX2, cartMaxY2 = self.findOtherIslandCartesianBounds(variables.cartesianBlockArray2)
                result = self.checkInIsland(cartMinX2, cartMinY2, cartMaxX2, cartMaxY2, newX, newY)
                if (result):
                    self.setNewCartBoundaries(variables.cartesianBlockArray2)
                    return True
            return False
        
        self.setNewPosition(newX, newY)
        return True
    
    # sets the character position to the new one
    def setNewPosition(self, newX, newY):
        self.cartX = newX
        self.cartY = newY
    
    # sets new cartesian boundaries for the appropriate island
    def setNewCartBoundaries(self, cartBlockArray):
        cartMinX, cartMinY, cartMaxX, cartMaxY = self.findOtherIslandCartesianBounds(cartBlockArray)
        self.cartMinX = cartMinX
        self.cartMinY = cartMinY
        self.cartMaxX = cartMaxX
        self.cartMaxY = cartMaxY

    # checks if the new coordinates the character is trying to move to is contained
    # within the island boundaries
    def checkInIsland(self, cartMinX, cartMinY, cartMaxX, cartMaxY, newX, newY):
        if (newX < cartMinX or newX > cartMaxX or newY < cartMinY 
                or newY > cartMaxY):
            return False
        else:
            return True
    
    # generates a bounding rectangle for where the bridge is and checks if the
    # character can move across the bridge (if the bridge is built)
    def canWalkAcrossBridge(self, newX, newY):
        for sprite in bridgeSprites:
            #.04 for 10, .1 for 4 blocks
            rightBottomCorner = (sprite.rect.bottomleft[0] + .04 * sprite.rect.width, 
                sprite.rect.bottomleft[1])
            rightBottomX, rightBottomY = self.convertIsometricToCartesian(rightBottomCorner[0]
                - self.offsetX, rightBottomCorner[1] - self.offsetY)
            leftTopCorner = (sprite.rect.topright[0] - .04 * sprite.rect.width, 
                sprite.rect.topright[1])
            leftTopX, leftTopY = self.convertIsometricToCartesian(leftTopCorner[0]
                - self.offsetX, leftTopCorner[1] - self.offsetY)
            bridgeMinX = leftTopX + startX
            bridgeMinY = leftTopY + startY + (self.boardCellHeight / 2)
            bridgeMaxX = rightBottomX + startX
            bridgeMaxY = rightBottomY + startY + (self.boardCellHeight / 2)
            if (newX > bridgeMinX and newX < bridgeMaxX and newY > bridgeMinY
                and newY < bridgeMaxY):
                if (sprite.bridgeName == "1to2"):
                    variables.walkToIsland2 = True
                return True
        return False
    
    # loosely adapted from SideScroller2 example in 112 Notes to fit isometric 
    # coordinates and desired scrolling effect: 
    # http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
    # checks if scrolling is necessary at the characters current position
    def makePlayerVisible(self):
        isScrollable = False
        if (self.cartX < self.scrollMargin + self.scrollX):
            isScrollable = True
        elif (self.cartX + self.scrollMargin > width + self.scrollX):
            isScrollable = True
        if (self.cartY < self.scrollMargin + self.scrollY):
            isScrollable = True
        elif (self.cartY + self.scrollMargin > height + self.scrollY):
            isScrollable = True
        return isScrollable

    # fix to check within isometric board
    def jump(self, event):
        posX, posY = event.pos
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

    # checks if the user has clicked on an enemy and if so, removes the enemy from
    # the sprite group
    # Note: can only kill enemy if it is on the same island as the character
    def killEnemy(self, event):
        posX, posY = event.pos
        posX, posY = self.convertIsometricToCartesian(posX - self.offsetX, posY - self.offsetY)
        posX += startX - (self.boardCellWidth / 2)
        posY += startY + (self.boardCellHeight / 2)
        if (posX < self.cartMinX or posX > self.cartMaxX or posY < self.cartMinY or posY > self.cartMaxY):
            return
        for sprite in enemySprites:
            enemyX, enemyY = self.convertIsometricToCartesian(sprite.rect.centerx - sprite.offsetX,
                sprite.rect.centery - sprite.offsetY)
            enemyX += startX
            enemyY += startY + (self.boardCellHeight / 2)
            cellMinX = enemyX - self.boardCellWidth / 2
            cellMaxX = enemyX + self.boardCellWidth / 2
            cellMinY = enemyY - self.boardCellHeight / 2
            cellMaxY = enemyY + self.boardCellHeight / 2
            if (posX >= cellMinX and posX <= cellMaxX and posY >= cellMinY and
                posY <= cellMaxY):
                sprite.kill()
                score.pointsDict["enemies killed"] += 1

# this class inherits from the parent class Character and creates special functions
# for the boy that the user controls when playing the game
class MainCharacter(Character):
    def __init__(self, image, cellWidth, cellHeight, blockArray, 
        cartesianBlockArray, offsetX, offsetY, characterPosition = None):
        super().__init__(image, cellWidth, cellHeight, blockArray, 
            cartesianBlockArray, offsetX, offsetY, characterPosition)
        self.totalIsoScrollX = 0
        self.totalIsoScrollY = 0
        self.totalCartScrollX = 0
        self.totalCartScrollY = 0

    # adds iron to the user's inventory if the user has stepped into a square with
    # iron in it
    def collectIron(self):
        for sprite in ironSprites:
            if (self.rect.colliderect(sprite.rect)):
                sprite.kill()
                sprite.addIronToInventory()
                score.pointsDict["iron collected"] += 1
    
    # adds the scroll to the character's current scroll and also tracks the total
    # scrolling (scrollX/Y and cartScrollX/Y are constantly reset in redraw all)
    def addScroll(self, scrollX, scrollY):
        self.scrollX += scrollX
        self.scrollY += scrollY
        cartScrollX, cartScrollY = self.convertIsometricToCartesian(scrollX, scrollY)
        self.cartScrollX += cartScrollX
        self.cartScrollY += cartScrollY
        self.totalIsoScrollX += scrollX
        self.totalIsoScrollY += scrollX
        self.totalCartScrollX += cartScrollX
        self.totalCartScrollY += cartScrollY

# generates the main character by creating an instance of MainCharacter
def createCharacter(image, charSprites, cellWidth, cellHeight, blockArray, 
    cartesianBlockArray, offsetX, offsetY, characterPosition = None):
    character = MainCharacter(image, cellWidth, cellHeight, blockArray, 
        cartesianBlockArray, offsetX, offsetY, characterPosition)
    charSprites.add(character)
    return character