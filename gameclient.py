#!/usr/bin/env python

"""gameclient.py: Script to launch a game client.
    Need to be invoked as follows:
    python gameclient.py player_id team
    TODO: make the server location more configurable
"""

__author__      = "Konstantinos Sideris"
__copyright__   = "Copyright 2012, UCLA game lab"

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
    from game.actions_keyboard import PlayerController
    
if (len(sys.argv) == 3):
        tenv = environment.Environment(int(sys.argv[1]),int(sys.argv[2]),\
                                       '192.168.130.1','80')
        a=view.Window(tenv)
        
        controller = PlayerController(a)
        controller.go()
        tenv.start()
        
        reactor.run()

else:
        print 'Usage: gameclient.py player_id team'


