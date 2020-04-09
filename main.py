import pygame
import os
import numpy as np
from island import *
from character import *
from variables import *

def playGame():
    pygame.init()
    
    make2DBoard(blockSprites, blockArray, blockRows, blockCols, cellWidth, cellHeight, startX, startY)
    makeBoardIsometric(blockArray)

    charSprites = pygame.sprite.Group()
    character = createCharacter("character.png", charSprites, cellWidth, cellHeight)

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
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                character.mousePressed(event, posX, posY)
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
        pygame.draw.rect(screen, (0, 255, 0),(200, 200, 50, 30))
        blockSprites.update()
        blockSprites.draw(screen)
        charSprites.update()
        charSprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
    os._exit(0)


playGame()
