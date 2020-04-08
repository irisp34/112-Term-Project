import pygame
import numpy as np
import os

width = 800
height = 800
fps = 50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("112 Project")

# Block class creates each of the blocks for the ground
class Block(pygame.sprite.Sprite):
    def __init__(self, cellWidth, cellHeight, color, posX, posY, startX, startY):
        super().__init__()
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.color = color
        self.startX = startX
        self.startY = startY
        # self.image = pygame.Surface([self.cellWidth, self.cellHeight])
        # self.image.fill(self.color)

        # grass image from https://clipart.info/natural-grass-png-top-view-12874
        self.originalImage = pygame.image.load("grass.png").convert_alpha()
        self.image = self.originalImage
        self.image = self.scaleImage()
        
        self.rect = self.image.get_rect()
        # position of top left corner
        self.rect.x = posX
        self.rect.y = posY
    
    def makeBlockIsometric(self, row, col):
        # self.rotatedImage = self.image
        self.angle = 45
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.cellWidth = self.cellWidth * 2
        self.image = self.scaleImage()
        self.convertCartesianToIsometric(row, col)
    
    def convertCartesianToIsometric(self, row, col):
        halfWidth = self.cellWidth / 2
        halfHeight = self.cellHeight / 2
        offsetX = (width // 2) - self.startX
        offsetY = (height // 2) - self.startY
        self.rect.x = ((col - row) * halfWidth) + offsetX
        self.rect.y = ((row + col) * halfHeight) + offsetY
    
    def scaleImage(self):
        self.image = pygame.transform.scale(self.image, (self.cellWidth, self.cellHeight))
        self.cellWidth, self.cellHeight = self.image.get_size()
        return self.image

# adds Block instances to the array
def addBlockToArray(blockArray, block, row, col):
    blockArray[row, col] = block 

# generates a new Block with the correct properties
def createBlock(blockSprites, blockArray, cellWidth, cellHeight, color, posX,
                posY, startX, startY, row, col):
    block = Block(cellWidth, cellHeight, color, posX, posY, startX, startY)
    addBlockToArray(blockArray, block, row, col)
    blockSprites.add(block)

# loops through the desired rows and columns for the board to make the entire
# board
def make2DBoard(blockSprites, blockArray, blockRows, blockCols):
    cellWidth = 50
    cellHeight = 50
    startX = 100
    startY = 100
    newStartX, newStartY = startX - cellWidth, startY - cellHeight
    color = (255, 0, 255)
    for row in range(blockRows):
        newStartX += cellWidth
        for col in range(blockCols):
            newStartY += cellHeight
            createBlock(blockSprites, blockArray, cellWidth, cellHeight, color,
                        newStartX, newStartY, startX, startY, row, col)
        newStartY = startY - cellHeight

def makeBoardIsometric(blockArray):
    for row in range(blockArray.shape[0]):
        for col in range(blockArray.shape[1]):
            print("before x",blockArray[row, col].rect.x, "y", blockArray[row, col].rect.y)
            blockArray[row, col].makeBlockIsometric(row, col)
            print("after x", blockArray[row, col].rect.x, "y", blockArray[row, col].rect.y)

def playGame():
    pygame.init()
    
    blockSprites = pygame.sprite.Group()
    blockRows = 2
    blockCols = 2
    blockArray = np.empty(shape=(blockRows, blockCols), dtype = object)
    make2DBoard(blockSprites, blockArray, blockRows, blockCols)
    makeBoardIsometric(blockArray)

    # print(blockSprites)
    # for block in blockSprites:
    #     print(block.rect.x, block.rect.y)

    clock = pygame.time.Clock()
    playing = True
    while playing:
        time = clock.tick(fps) # waits for next frame
        for event in pygame.event.get():
            # print(event)
            if (event.type == pygame.QUIT):
                playing = False
            # elif (event.type == pygame.MOUSEBUTTONDOWN):
            #     character.mousePressed(event, posX, posY)
                # character.jump(posX, posY)
            # elif (event.type == pygame.KEYDOWN):
            #     if (event.key == pygame.K_DOWN):
            #         character.moveDown()
            #     elif (event.key == pygame.K_UP):
            #         character.moveUp()
            #     elif (event.key == pygame.K_LEFT):
            #         character.moveLeft()
            #     elif (event.key == pygame.K_RIGHT):
            #         character.moveRight()
        # keys = pygame.key.get_pressed()
        # if (keys[pygame.K_DOWN]):
        #     character.moveDown()
        # elif (keys[pygame.K_UP]):
        #     character.moveUp()
        # elif (keys[pygame.K_RIGHT]):
        #     character.moveRight()
        # elif (keys[pygame.K_LEFT]):
        #     character.moveLeft()

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 255, 0),(200, 200, 50, 30))
        blockSprites.update()
        blockSprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
    os._exit(0)


playGame()
