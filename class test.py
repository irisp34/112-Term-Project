import module_manager
module_manager.review()

import pygame


class PygameGame(object):
    def __init__(self, width=400, height=400, fps=50, title="112 Project"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.allSprites = pygame.sprite.Group()
        self.screen = pygame.display.set_mode((self.width, self.height))
        # pygame.init()
    def init(self):
        pygame.init()

    # def mousePressed(event, posX, posY):
    #     self.posX, self.posY = event.pos
    #     self.posX, self.posY = (self.posX - charWidth // 2, 
    #         self.posY - charHeight // 2)
    #     # return posX, posY

    # def keyPressed(event, posX, posY):
    #     if (event.key == pygame.K_UP):
    #         self.posY -= changeInPos
    #     elif (event.key == pygame.K_DOWN):
    #         self.posY += changeInPos
    
    # def updateSprite(self):
    #     # pygame.draw.rect(self.screen, (0, 255, 0),(posX, posY, charWidth, charHeight))
    #     self.allSprites.add(self)

    def runGame(self):
        self.init()
        
        clock = pygame.time.Clock()
        playing = True
        while playing:
            time = clock.tick(self.fps) # waits for next frame
            for event in pygame.event.get():
                # print(event)
                if (event.type == pygame.QUIT):
                    playing = False
                elif (event.type == pygame.MOUSEBUTTONDOWN):
                    self.mousePressed(event)
                elif (event.type == pygame.KEYDOWN):
                    # posX, posY = keyPressed(event)
                    if (event.key == pygame.K_DOWN):
                        # posY += changeInPos
                        self.keyPressed(event, posX, posY)
                        print("down")
                    elif (event.key == pygame.K_UP):
                        # posY -= changeInPos
                        self.keyPressed(event, posX, posY)
                    elif (event.key == pygame.K_LEFT):
                        posX -= changeInPos
                        print("left")
                    elif (event.key == pygame.K_RIGHT):
                        posX += changeInPos
                        print("right")
                # print("event", posX, posY)
            screen.fill((0, 0, 0))
            # print(posX, posY)
            self.allSprites.update()
            pygame.display.flip()
        pygame.quit()

class Character(pygame.sprite.Sprite):
    def __init__(self, posX, posY, charWidth, charHeight, changeInPos):
        super(PygameGame).__init__()
        self.posX = posX #width // 2
        self.posY = posY #height // 2
        self.changeInPos = changeInPos #5
        self.charWidth = charWidth #50
        self.charHeight = charHeight #60
        # self.updateCharacter()
        self.image = pygame.image.load("testPerson.png").convert_alpha()
        self.rect = self.image.get_rect()


character = Character(200, 200, 50, 60, 5)

game = PygameGame()
game.runGame()