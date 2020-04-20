import threading
import time
import pygame
import random
from character import *
from island import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, character, cellWidth, cellHeight, blockArray, cartesianBlockArray, offsetX, offsetY):
        super().__init__()
        self.cartBlockArray = cartesianBlockArray
        self.blockArray = blockArray
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.scrollX = 0
        self.scrollY = 0
        self.cartScrollX = 0
        self.cartScrollY = 0
        self.scrollMargin = 100
        self.image = pygame.image.load("mouse.png").convert_alpha()
        self.scaleImage()
        self.findImageDimensions()
        self.rect = self.image.get_rect()
        self.findIsometricBounds(self.blockArray)
        self.findCartesianBounds(self.cartBlockArray)
        self.rect.centerx, self.rect.centery = self.getRandomBoardCenter(self.blockArray)
        self.justMoved = False

    def scaleImage(self):
        location = (self.boardCellWidth, self.boardCellHeight)
        self.image = pygame.transform.scale(self.image, location)
        self.rect = self.image.get_rect()

    def findImageDimensions(self):
        self.charWidth, self.charHeight = self.image.get_size()

    def findIsometricBounds(self, blockArray):
        # organized top left, top right, bottom left, bottom right
        boardCoordinates = getBoardBounds(blockArray)
        self.minX = boardCoordinates[2][0] #+ self.boardCellWidth / 4
        self.minY = boardCoordinates[0][1] #+ self.boardCellHeight / 4
        self.maxX = boardCoordinates[1][0] #+ self.boardCellWidth / 4
        self.maxY = boardCoordinates[3][1] #+ self.boardCellHeight / 4

    def findCartesianBounds(self, cartBlockArray):
        cartBoard = getBoardBounds(cartBlockArray)
        self.cartMinX = cartBoard[0][0]
        self.cartMinY = cartBoard[0][1]
        self.cartMaxX = cartBoard[3][0]
        self.cartMaxY = cartBoard[3][1]

    # retrieves a random isometric board center
    def getRandomBoardCenter(self, blockArray):
        randRow = random.randint(0, blockRows - 1)
        randCol = random.randint(0, blockCols - 1)
        block = blockArray[randRow, randCol]
        centerX = (block.rect.centerx + block.rect.midtop[0]) // 2
        centerY = (block.rect.centery + block.rect.midtop[1]) // 2
        return centerX, centerY

    def addScroll(self, scrollX, scrollY):
        self.scrollX += scrollX
        self.scrollY += scrollY
        cartScrollX, cartScrollY = self.convertIsometricToCartesian(scrollX, scrollY)
        self.cartScrollX += cartScrollX
        self.cartScrollY += cartScrollY

    def moveRight(self):
        print("right")
        if (not self.isWalkable(1, 0)):
            return
        self.rect.centerx += self.boardCellWidth
        self.rect.centery += 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
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
            scrollX = -self.boardCellWidth / 2
            scrollY = (-0.5 * self.boardCellHeight) / 2
            self.addScroll(scrollX, scrollY)
            self.justMoved = True

    def moveUp(self):
        print("Up")
        if (not self.isWalkable(0, -1)):
            return
        self.rect.centerx += self.boardCellWidth
        self.rect.centery -= 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
            scrollX = self.boardCellWidth / 2
            scrollY = (-0.5 * self.boardCellHeight) / 2
            self.addScroll(scrollX, scrollY)
            self.justMoved = True
 
    def moveDown(self):
        print("Down")
        if (not self.isWalkable(0, 1)):
            return
        self.rect.centerx -= self.boardCellWidth
        self.rect.centery += 0.5 * self.boardCellHeight
        if (self.makePlayerVisible()):
            scrollX = -self.boardCellWidth / 2
            scrollY = (0.5 * self.boardCellHeight) / 2
            self.addScroll(scrollX, scrollY)
            self.justMoved = True

    # loosely adapted from SideScroller2 example in 112 Notes to fit isometric 
    # coordinates and desired scrolling effect: 
    # http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
    def makePlayerVisible(self):
        isScrollable = False
        if (self.cartX < self.scrollMargin + self.scrollX):
            isScrollable = True
        elif (self.cartX + self.scrollMargin > self.scrollX + width):
            isScrollable = True
        if (self.cartY < self.scrollMargin + self.scrollY):
            isScrollable = True
        elif (self.cartY + self.scrollMargin > self.scrollX + height):
            isScrollable = True
        return isScrollable

    def isWalkable(self, dx, dy):
        self.findCartesianBounds(self.cartBlockArray)
        # My code: fix offsetX and offsetY
        self.cartX, self.cartY = self.convertIsometricToCartesian(self.rect.centerx - self.offsetX, 
            self.rect.centery - self.offsetY)
        self.cartX += startX #+ (self.boardCellWidth // 2)
        self.cartY += startY + (self.boardCellHeight / 2)
        newX = self.cartX + dx * self.boardCellWidth
        newY = self.cartY + dy * self.boardCellHeight
        if (newX < self.cartMinX or newX > self.cartMaxX or newY < self.cartMinY or newY > self.cartMaxY):
            return False
        self.cartX = newX
        self.cartY = newY
        return True

    def convertIsometricToCartesian(self, isoX, isoY):
        cartesianX = (isoX + isoY * 2) / 2
        cartesianY = (2*isoY - isoX) / 2
        return (cartesianX, cartesianY)
        
class EnemyThread(threading.Thread):
    def __init__(self, threadID, name, enemy):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.enemy = enemy

    def run(self):
        while (True):
            time.sleep(1)
            direction = random.randint(0, 3)
            print("Wake up! Direction:", direction)
            if (direction == 0):
                self.enemy.moveRight()
            elif (direction == 1):
                self.enemy.moveLeft()
            elif (direction == 2):
                self.enemy.moveUp()
            else:
                self.enemy.moveDown()

def createEnemies(character, charSprites, cellWidth, cellHeight, blockArray, 
    cartesianBlockArray, offsetX, offsetY):
    enemy = Enemy(character, cellWidth, cellHeight, blockArray, cartesianBlockArray, offsetX, offsetY)
    enemy.daemon = True
    charSprites.add(enemy)
    thread = EnemyThread(1, "Thread-1", enemy)
    thread.start()
