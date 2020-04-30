# this is the Enemy class which is a subclass of Character. This gives the enemy
# the ability to consume iron, kill the character, and move on its own on a Thread

import threading
import time
import pygame
import random
from character import *
from island import *
import variables

class Enemy(Character):
    # enemy picture: https://www.gamedevmarket.net/asset/evil-tree-pixel-art-monster-enemy-10227/
    def __init__(self, character, cellWidth, cellHeight, blockArray,
        cartesianBlockArray, offsetX, offsetY, thread, characterPosition):
        super().__init__("enemy.gif", cellWidth, cellHeight, blockArray,
            cartesianBlockArray, offsetX, offsetY, characterPosition)
        self.character = character
        self.thread = thread

    # overrides the built in kill function to also stop the thread from running
    # after the enemy is killed.
    def kill(self):
        self.thread.stopRunning()
        super().kill()

    # scales image to the cell width and height
    def scaleImage(self):
        location = (self.boardCellWidth, self.boardCellHeight)
        self.image = pygame.transform.scale(self.image, location)
        self.rect = self.image.get_rect()
    
    # enemy eats up iron but character doesn't get the resource
    def collectIron(self):
        for sprite in ironSprites:
            if (self.rect.colliderect(sprite.rect)):
                sprite.kill()


# learned about threading in python from: https://pymotw.com/3/threading/
class EnemyThread(threading.Thread):
    def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.isRunning = True
      self.name = name

    def setEnemy(self, enemy):
        self.enemy = enemy

    def getDirection(self):
        return random.randint(0, 3)

    # enemy picks a random direction and attempts to move there if the user is
    # on the main screen for the game. If the direction cannot be moved to, the
    # enemy picks a new direction to try to move to
    def run(self):
        while (self.isRunning):
            time.sleep(2)
            if (not self.isRunning):
                return
            if (variables.isShopping or variables.isInstructionsScreen or 
                variables.isSplashScreen):
                continue
            isWalkable = False
            while (not isWalkable):
                direction = self.getDirection()
                if (direction == 0):
                    isWalkable = self.enemy.isWalkable(1, 0)
                elif (direction == 1):
                    isWalkable = self.enemy.isWalkable(-1, 0)
                elif (direction == 2):
                    isWalkable = self.enemy.isWalkable(0, -1)
                else:
                    isWalkable = self.enemy.isWalkable(0, 1)
            
            if (direction == 0):
                self.enemy.moveRight()
            elif (direction == 1):
                self.enemy.moveLeft()
            elif (direction == 2):
                self.enemy.moveUp()
            else:
                self.enemy.moveDown()
            self.enemy.collectIron()
    
    def stopRunning(self):
        self.isRunning = False

# creates an enemy on the board and starts the thread
def createEnemies(character, charSprites, cellWidth, cellHeight, blockArray, 
    cartesianBlockArray, offsetX, offsetY, enemyPosition = None):
    thread = EnemyThread(1, "Thread-1")
    enemy = Enemy(character, cellWidth, cellHeight, blockArray,
        cartesianBlockArray, offsetX, offsetY, thread, enemyPosition)
    enemy.daemon = True
    enemySprites.add(enemy)
    thread.setEnemy(enemy)
    thread.start()
    return enemy

# checks if the character and enemy have collided and sets game over if this
# is true
def checkEnemyCollision(character, enemySprites):
    for sprite in enemySprites:
        if (character.rect.colliderect(sprite.rect)):
            variables.isGameOver = True

            
