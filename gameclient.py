import pygame
import game.view as view
import game.clientEnvironment as environment
from twisted.internet import reactor
import sys, platform


pygame.init()
if platform.machine() == "armv7l":
    
    print 'GOING FULLSCREEN'
    displayFlags = pygame.DOUBLEBUF | pygame.FULLSCREEN
    pygame.mouse.set_visible(False)
    
    pygame.display.set_mode((800, 480), displayFlags)
else:
    displayFlags = pygame.DOUBLEBUF
    pygame.display.set_mode((800, 480), displayFlags)

tenv = environment.Environment()

a=view.Window(tenv)


tenv.start()

reactor.run()


