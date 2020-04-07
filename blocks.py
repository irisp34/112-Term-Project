import pygame
import os

width = 400
height = 400
fps = 50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("112 Project")

class Character(pygame.sprite.Sprite):
    # def __init__(self, charWidth, charHeight, changeInPos):
    def __init__(self, image, changeInPos):
        super().__init__()
        self.changeInPos = changeInPos
        # self.image = pygame.Surface([charWidth, charHeight])
        self.image = pygame.image.load(image).convert()
        print(self.image.get_size())
        # self.newImage = self.image.copy()
        self.charWidth, self.charHeight = self.image.get_size()
        print(self.charWidth, self.charHeight)
        self.image = pygame.transform.scale(self.image, (width//5, height//3))
        self.charWidth, self.charHeight = self.image.get_size()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()

    def moveRight(self):
        # if (self.rect.x )
        self.rect.x += self.changeInPos
 
    def moveLeft(self):
        self.rect.x -= self.changeInPos

    def moveUp(self):
        self.rect.y -= self.changeInPos
 
    def moveDown(self):
        self.rect.y += self.changeInPos

    def jump(self, posX, posY):
        self.rect.x = posX
        self.rect.y = posY

    def mousePressed(self, event, posX, posY):
        posX, posY = event.pos
        print("before", posX)
        posX = posX - self.charWidth // 2
        print("original", posX)
        if (posX < 0):
            posX = 0
        elif (posX + self.charWidth > width):
            print(posX + self.charWidth)
            posX = width - self.charWidth
            print("new", posX)
        posY = posY - self.charHeight // 2
        if (posY < 0):
            posY = 0
        elif (posY + self.charHeight > height):
            posY = height - self.charHeight
        self.jump(posX, posY)

# def mousePressed(event, charWidth, charHeight):
#     posX, posY = event.pos
#     posX = posX - charWidth // 2
#     if (posX < 0):
#         posX = 0
#     posY = posY - charHeight // 2
#     if (posY < 0):
#         posY = 0
#     return posX, posY

def playGame():
    pygame.init()
    
    allSprites = pygame.sprite.Group()
    

    posX = 200
    posY = 200
    image = "mouse.png"
    character = Character(image, 2)
    # charWidth = character.rect.width
    # charHeight = character.rect.height
    
    allSprites.add(character)
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

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0),(posX, posY, 50, 30))
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
    os._exit(0)

playGame()





