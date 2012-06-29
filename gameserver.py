import pygame
import game.view as view
import game.environment as environment
from twisted.internet import reactor
from threading import Thread
import sys


pygame.init()
pygame.display.set_mode((800, 480), pygame.DOUBLEBUF)

tenv = environment.Environment()
tenv.createPlayer(1)
tenv.createPlayer(2)
tenv.createPlayer(1)
tenv.createPlayer(2)
tenv.createPlayer(1)
tenv.createPlayer(2)

tenv.createBuilding(1)
tenv.createBuilding(2)
tenv.createBuilding(1)

a=view.Window(tenv)


tenv.start()
reactor.run()


