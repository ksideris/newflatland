'''
This file includes the player, the buildings, and the resource pool.

Drawing, sound playing, and the various player/building state is contained here.

In regards to sound playing, you will notice that most functions have a playSound function.
This is present because when you're testing, and have the player and the server running
on the same computer, both the servers copy of the player, and the clients copy of the player
will attempt to play the sound, and since the computer only has one mixer, it doesn't really
work, and thus, sounds only play for the client.
'''

import math
import pygame.mixer
from vector import Vector2D

#This comment is still not important.
sounds = dict()

def _initSounds():
#    pygame.mixer.init(frequency=16000)#, size=-8, channels=1)
    sounds["trigger trap"] = pygame.mixer.Sound("data/sfx/alex_sfx/Trigger Trap.wav")
    sounds["explosion"] = pygame.mixer.Sound("data/sfx/alex_sfx/Attack Hit.wav")

    sounds["attack"] = pygame.mixer.Sound("data/sfx/alex_sfx/attack.wav")
    sounds["poly armor full"] = pygame.mixer.Sound("data/sfx/alex_sfx/Points Full.wav")
    sounds["player upgrade"] = pygame.mixer.Sound("data/sfx/alex_sfx/You upgraded.wav")

    sounds["accept upgrade"] = pygame.mixer.Sound("data/sfx/alex_sfx/accept_upgrade.wav")

    sounds["gain poly armor"] = pygame.mixer.Sound("data/sfx/alex_sfx/gain resource.wav")
    sounds["lose poly armor"] = pygame.mixer.Sound("data/sfx/alex_sfx/pay resource.wav")
    sounds["poly armor depleted"] = pygame.mixer.Sound("data/sfx/alex_sfx/resources depleted.wav")

    sounds["mining"] = pygame.mixer.Sound("data/sfx/alex_sfx/In Resource Pool(loop).wav")

    sounds["building",3] = pygame.mixer.Sound("data/sfx/alex_sfx/Building 3-sided.wav")
    sounds["building",4] = pygame.mixer.Sound("data/sfx/alex_sfx/Building 4-sided.wav")
    sounds["building",5] = pygame.mixer.Sound("data/sfx/alex_sfx/Building 5-sided.wav")

    sounds["finish building",3] = pygame.mixer.Sound("data/sfx/alex_sfx/Finish 3-sided.wav")
    sounds["finish building",4] = pygame.mixer.Sound("data/sfx/alex_sfx/Finish 4-sided.wav")
    sounds["finish building",5] = pygame.mixer.Sound("data/sfx/alex_sfx/Finish 5-sided.wav")

    sounds["scanning"] = pygame.mixer.Sound("data/sfx/alex_sfx/Sweeping.wav")

def getSound(strIdx, nIndex = None):
    if not nIndex == None:
        return sounds[strIdx, nIndex]
    else:
        return sounds[strIdx]


class Player():
    def __init__(self):
		self.player_id=-1
		self.team=-1
		self.position = Vector2D(20, 120)
		self.sides = 3
		self.resources = 0
		self.action = 0 #Convention Idle - 0 ,Moving - 1, Attacking - 2, Building/Mining - 3,Scanning - 4 


class Building():
    def __init__(self):
        self.sides = 0
        self.resources = 0
        self.size = 1


