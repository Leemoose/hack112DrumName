#Framework for pygame
import pygame

def init(data):
    pass

def keyDownEvent(event, data):
    pass

def mousePressedEvent(event, data):
    pass    

def timerFired(data):
    pass

def dirtyRectBlit(data):
    pass

def blitMovers(data):
    pass

## Pygame frame work ##

def run(width=680, height=540):
    pygame.init()

    class Struct(): pass
    data = Struct()

    data.screen=pygame.display.set_mode((width,height)) 
    data.screenrect = data.screen.get_rect()
    data.width = width
    data.height = height

    init(data)       

    data.clock = pygame.time.Clock()     #create pygame clock object
    mainloop = True
    FPS = 60                 # desired max. framerate in frames per second. 
    playtime = 0
    while mainloop:
        milliseconds = data.clock.tick(FPS)  # millisecs passed since last frame
        data.seconds = milliseconds / 1000.0 # seconds passed since last frame 
        playtime += data.seconds #total playtime
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressedEvent(event, data)
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                else: keyDownEvent(event, data) 
            #mousePressed and others to be added

        pygame.display.set_caption("CHANGE ME") #window caption

        #paint current location of items about to move (or just blit the whole
        #   bg)
        dirtyRectBlit(data)
        #move the items
        timerFired(data)
        #paint moved items
        blitMovers(data)

        pygame.display.flip()          # update the screen
    print("This 'game' was played for {:.2f} seconds".format(playtime))
    pygame.quit()

run()