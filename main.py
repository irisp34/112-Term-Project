import module_manager
module_manager.review()

import pygame

# must always call constructor
# pygame.init()



# dimensions of game
width = 400
height = 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

posX = width // 2
posY = height // 2
changeInPos = 5
charWidth = 50
charHeight = 60

image = pygame.image.load("testPerson.png")

def mousePressed(event):
    posX, posY = event.pos
    posX, posY = posX - charWidth // 2, posY - charHeight // 2
    return posX, posY

#???
def keyPressed(event, posX, posY):
    if (event.key == pygame.K_UP):
        posY -= changeInPos
    elif (event.key == pygame.K_DOWN):
        posY += changeInPos
    return posX, posY

playing = True
while playing:
    time = clock.tick(100) # waits for next frame
    for event in pygame.event.get():
        # print(event)
        if (event.type == pygame.QUIT):
            playing = False
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            posX, posY = mousePressed(event)
        elif (event.type == pygame.KEYDOWN):
            # posX, posY = keyPressed(event)
            if (event.key == pygame.K_DOWN):
                # posY += changeInPos
                posX, posY = keyPressed(event, posX, posY)
                print("down")
            elif (event.key == pygame.K_UP):
                # posY -= changeInPos
                posX, posY = keyPressed(event, posX, posY)
            elif (event.key == pygame.K_LEFT):
                posX -= changeInPos
                print("left")
            elif (event.key == pygame.K_RIGHT):
                posX += changeInPos
                print("right")
        print("event", posX, posY)
    screen.fill((0, 0, 0))
    screen.blit(image, (100, 100))
    pygame.draw.rect(screen, (0, 255, 0),(posX, posY, charWidth, charHeight))
    # print(posX, posY)
    pygame.display.flip()
pygame.quit()
