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
enemySprites = pygame.sprite.Group()
ironSprites = pygame.sprite.Group()
treeSprites = pygame.sprite.Group()
resourceSprites = pygame.sprite.Group()
inventoryBarSprite = pygame.sprite.Group()
bridgeSprites = pygame.sprite.Group()

shopImage = None
shopButtonRect = 0
buyImage = None
buyButtonRect = 0
isShopping = False
purchasableItems = dict()
betweenItemsOffset = 30
drawOutline = False
drawUnaffordableMessage = False
isGameOver = False
# keyword is the currently selected item
keyword = None
baseX = 100
baseY = 100
# various resource costs
# bridgeCost = 3
# bridgeResource = "wood"
bridgeDict = dict()
bridgeDict["wood"] = 3
# hammerCosts = [1, 1]
# hammerResources = ["wood", "iron"]
hammerDict = dict()
hammerDict["wood"] = 1
hammerDict["iron"] = 1

# place board in center of screen
offsetX1 = (width // 2) - startX
offsetY1 = (height // 2) - startY
offsetX2 = 0
offsetY2 = 0

walkToIsland2 = False

score = 0



    