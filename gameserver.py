import pygame
import game.view as view
import game.environment as environment
from twisted.internet import reactor
from threading import Thread
import sys

pygame.init()
pygame.display.set_mode((800, 480), pygame.DOUBLEBUF)

tenv = environment.Environment()


a=view.Window(tenv)


tenv.start()
reactor.run()


