import threading
import time
import pygame
import random
from character import *
from island import *

class Enemy(Character):
    # enemy picture: https://www.gamedevmarket.net/asset/evil-tree-pixel-art-monster-enemy-10227/
    def __init__(self, character, cellWidth, cellHeight, blockArray, cartesianBlockArray, offsetX, offsetY, thread):
        super().__init__("enemy.gif", cellWidth, cellHeight, blockArray, cartesianBlockArray, offsetX, offsetY)
        self.character = character
        self.thread = thread

    def kill(self):
        self.thread.stopRunning()
        super().kill()

    def scaleImage(self):
        location = (self.boardCellWidth * 2, self.boardCellHeight * 2)
        self.image = pygame.transform.scale(self.image, location)
        self.rect = self.image.get_rect()


# learned about threading in python from: https://pymotw.com/3/threading/
class EnemyThread(threading.Thread):
    def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.isRunning = True
      self.name = name
    #   self.enemy = enemy

    def setEnemy(self, enemy):
        self.enemy = enemy

    def getDirection(self):
        return random.randint(0, 3)

    def run(self):
        while (self.isRunning):
            time.sleep(3)
            if (not self.isRunning):
                return
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
    
    def stopRunning(self):
        self.isRunning = False


def createEnemies(character, charSprites, cellWidth, cellHeight, blockArray, 
    cartesianBlockArray, offsetX, offsetY):
    thread = EnemyThread(1, "Thread-1")
    enemy = Enemy(character, cellWidth, cellHeight, blockArray, cartesianBlockArray, offsetX, offsetY, thread)
    enemy.daemon = True
    enemySprites.add(enemy)
    thread.setEnemy(enemy)
    thread.start()
    return thread