import numpy as np
import pygame
from island import *
from variables import *

class Character(pygame.sprite.Sprite):
    def __init__(self, image, cellWidth, cellHeight):
        super().__init__()
        # self.changeInPos = changeInPos
        self.boardCellWidth = cellWidth
        self.boardCellHeight = cellHeight
        # self.image = pygame.Surface([charWidth, charHeight])
        self.image = pygame.image.load(image).convert_alpha()
        # self.newImage = self.image.copy()
        self.findImageDimensions()
        self.scaleImage()
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.initialCharacterPosition()
        print("min", self.minX, self.minY)
        print("max", self.maxX, self.maxY)
        self.rect.x = self.maxX
        self.rect.y = self.maxY
        self.placeInCenterOfBlock()
    
    def placeInCenterOfBlock(self):
        self.rect.x += 0.5 * self.boardCellHeight
        self.rect.y -= 0.25 * self.boardCellWidth
    
    def initialCharacterPosition(self):
        boardCoordinates = getIsometricBoardBounds(blockArray)
        self.minX = boardCoordinates[0][0]
        self.minY = boardCoordinates[0][1]
        self.maxX = boardCoordinates[1][0]
        self.maxY = boardCoordinates[1][1]
    
    def findImageDimensions(self):
        self.charWidth, self.charHeight = self.image.get_size()

    def scaleImage(self):
        location = (self.boardCellWidth, self.boardCellHeight)
        self.image = pygame.transform.scale(self.image, location)

    def moveRight(self):
        self.rect.x += self.boardCellWidth
        self.rect.y += 0.5 * self.boardCellHeight
 
    def moveLeft(self):
        self.rect.x -= self.boardCellWidth
        self.rect.y -= 0.5 * self.boardCellHeight

    def moveUp(self):
        self.rect.y -= 0.5 * self.boardCellHeight
        self.rect.x += self.boardCellWidth
 
    def moveDown(self):
        self.rect.y += 0.5 * self.boardCellHeight
        self.rect.x -= self.boardCellWidth

    def jump(self, posX, posY):
        self.rect.x = posX
        self.rect.y = posY

    def mousePressed(self, event, posX, posY):
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
        self.jump(posX, posY)

def createCharacter(image, charSprites, cellWidth, cellHeight):
    character = Character(image, cellWidth, cellHeight)
    charSprites.add(character)
    return character