# stores all the variables which influences the world generation such as creating
# sprite groups and setting island sizes
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
blockRows = 10
blockCols = 10

# all sprite groups
blockArray1 = np.empty(shape=(blockRows, blockCols), dtype = object)
cartesianBlockArray1 = np.empty(shape=(blockRows, blockCols), dtype = object)
blockArray2 = np.empty(shape=(blockRows, blockCols), dtype = object)
cartesianBlockArray2 = np.empty(shape=(blockRows, blockCols), dtype = object)
blockSprites1 = pygame.sprite.Group()
blockSprites2 = pygame.sprite.Group()
waterSprites = pygame.sprite.Group()
buildingSprites = pygame.sprite.Group()
charSprites = pygame.sprite.Group()
enemySprites = pygame.sprite.Group()
ironSprites = pygame.sprite.Group()
treeSprites = pygame.sprite.Group()
resourceSprites = pygame.sprite.Group()
inventoryBarSprite = pygame.sprite.Group()
bridgeSprites = pygame.sprite.Group()

# shopImage = None
# shopButtonRect = 0
# buyImage = None
# buyButtonRect = 0
isShopping = False
purchasableItems = dict()
betweenItemsOffset = 75
drawOutline = False
drawUnaffordableMessage = False
isGameOver = False
isSplashScreen = True
isInstructionsScreen = False
mainInstructionsButton = None
startInstructionsButton = None
# keyword is the currently selected item
keyword = None
baseX = 100
baseY = 100
# various resource costs
bridgeDict = dict()
bridgeDict["wood"] = 3
hammerDict = dict()
hammerDict["wood"] = 1
hammerDict["iron"] = 1
farmDict = dict()
farmDict["wood"] = 4
farmDict["hammer"] = 1
factoryDict = dict()
factoryDict["wood"] = 3
factoryDict["iron"] = 5
factoryDict["hammer"] = 1

isBuildingProduction = False
# place board in center of screen
offsetX1 = (width // 2) - startX
offsetY1 = (height // 2) - startY
offsetX2 = 0
offsetY2 = 0
isNewGame = True

walkToIsland2 = False

# score = 0



    