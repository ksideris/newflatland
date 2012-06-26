import pygame
import game.view as view

from twisted.internet import reactor
pygame.init()
pygame.display.set_mode((1600, 960), pygame.DOUBLEBUF)


a=view.Window()

a.start('Server')
reactor.run()


