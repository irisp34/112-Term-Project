# stores all the global variables which influences the look of the grid
import pygame
import numpy as np

width = 1200
height = 800
fps = 50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("112 Project")
cellWidth = 50
cellHeight = 50
startX = 100
startY = 100
# startX = 0
# startY = 0
blockRows = 4
blockCols = 4

blockArray1 = np.empty(shape=(blockRows, blockCols), dtype = object)
cartesianBlockArray1 = np.empty(shape=(blockRows, blockCols), dtype = object)
blockArray2 = np.empty(shape=(blockRows, blockCols), dtype = object)
cartesianBlockArray2 = np.empty(shape=(blockRows, blockCols), dtype = object)
blockSprites1 = pygame.sprite.Group()
blockSprites2 = pygame.sprite.Group()
waterSprites = pygame.sprite.Group()
charSprites = pygame.sprite.Group()
treeSprites = pygame.sprite.Group()
# place board in center of screen
offsetX = (width // 2) - startX
offsetY = (height // 2) - startY
# offsetX = 0
# offsetY = 0

def change(blockArray):
    global cartesianBlockArray
    cartesianBlockArray = blockArray
    # print("invariable, correct", blockArray)
    # print("in varaible, result", cartesianBlockArray)

    