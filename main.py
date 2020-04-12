# main while loop which starts the game 
import pygame
import os
import numpy as np
from island import *
from character import *
from variables import *

class Water(pygame.sprite.Sprite):
    def __init__(self, image, location):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        # self.rect.x, self.rect.y = location

def createWater(waterSprites, image, rect):
    rect.width, rect.height = rect[2], rect[3]
    for xPixel in range(0, width, rect.width):
        for yPixel in range(int(height/2), height, rect.height):
            water = Water(image, (xPixel, yPixel))
            waterSprites.add(water)


def playGame():
    pygame.init()
    make2DBoard(blockSprites, blockArray, blockRows, blockCols, cellWidth, 
                cellHeight, startX, startY)
    makeBoardIsometric(blockArray)

    charSprites = pygame.sprite.Group()
    # character picture from: https://ya-webdesign.com/imgdownload.html
    character = createCharacter("character.png", charSprites, cellWidth, cellHeight)

    waterImage = pygame.image.load("water.png").convert_alpha()
    rect = waterImage.get_rect()
    print("rect", rect)
    createWater(waterSprites, waterImage, rect)

    clock = pygame.time.Clock()
    playing = True
    while playing:
        time = clock.tick(fps) # waits for next frame
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                playing = False
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                character.mousePressed(event)
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
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_DOWN]):
            character.moveDown()
        elif (keys[pygame.K_UP]):
            character.moveUp()
        elif (keys[pygame.K_RIGHT]):
            character.moveRight()
        elif (keys[pygame.K_LEFT]):
            character.moveLeft()

        screen.fill((255, 255, 255))
        # screen.blit(background.image, background.rect)
        pygame.draw.rect(screen, (0, 255, 0),(200, 200, 50, 30))

        waterSprites.update()
        waterSprites.draw(screen)
        blockSprites.update()
        blockSprites.draw(screen)
        charSprites.update()
        charSprites.draw(screen)
        # pygame.draw.rect(screen, (0, 0, 255),(450, 450, 10, 10))
        # pygame.draw.rect(screen, (255, 0, 255),(300, 450, 10, 10))
        # pygame.draw.rect(screen, (255, 0, 255),(300, 300, 10, 10))
        # pygame.draw.rect(screen, (0, 0, 255),(250, 525, 10, 10))
        # pygame.draw.rect(screen, (255, 0, 255),(400, 550, 10, 10))
        pygame.draw.rect(screen, (255, 0, 255),(400, 400, 10, 10))
        # pygame.draw.rect(screen, (255, 0, 255),(450, 400, 10, 10))
        pygame.draw.rect(screen, (255, 0, 0),(400, 550, 10, 10))
        pygame.display.flip()
    pygame.quit()
    os._exit(0)


playGame()
