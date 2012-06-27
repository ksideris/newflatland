import pygame
import game.view as view
import game.environment as environment
from twisted.internet import reactor
from game.network.server import Server
from threading import Thread
import sys


pygame.init()
pygame.display.set_mode((800, 480), pygame.DOUBLEBUF)

tenv = environment.Environment()
tenv.createPlayer(1)

tenv.createBuilding(1)
a=view.Window(tenv)

t=Thread(target=Server().start, args=('192.168.1.102','7022'))
t.start()
	
tenv.start()
reactor.run()


