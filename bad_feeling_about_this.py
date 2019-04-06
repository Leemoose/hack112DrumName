import pygame
BG = (16, 8, 47)
BLACK = (0,0,0)


pygame.init()
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
done = False
clock = pygame.time.Clock()
image = pygame.image.load('coolCircle.jpg')
image1 = pygame.image.load("otherCoolCircle.jpg")
image2 = pygame.image.load("otherOtherCoolCircle.jpg")
image = pygame.transform.smoothscale(image, (50, 50))
image1 = pygame.transform.smoothscale(image1, (50, 50))
image2 = pygame.transform.smoothscale(image2, (50, 50))
image.set_colorkey(BG)
image1.set_colorkey(BLACK)
image2.set_colorkey(BLACK)


while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        screen.fill((255, 255, 255))
        
        screen.blit(image, (width - 50, height/2))
        screen.blit(image1, (width - 50, height/3))
        screen.blit(image2, (width - 50, height*2/3))

        
        pygame.display.flip()
        clock.tick(60)