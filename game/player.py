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
import random

class Player():
	def __init__(self):
		self.player_id=-1
		self.team=0
		self.position = Vector2D(random.randint(1, 10), random.randint(1, 10)) # this should range from -1,-1 to 1,1
		self.sides = 3
		self.resources = 0
		self.action = 0 #Convention Idle - 0 ,Moving - 1, Attacking - 2, Building/Mining - 3,Scanning - 4 
	
	def draw(self,view, position):
		image = view.images.images["Player", self.team, self.sides]
		image.draw(view.screen, position)

class Building():
	def __init__(self):
		self.sides = 3
		self.resources = 0
		self.team=1
		self.size = 1
		self.position = Vector2D(random.randint(-10, 10), random.randint(-10, 10))

	def draw(self,view, position):
		image = view.images.images["Building", self.sides,self.team]
		image.draw(view.screen, position)
		
class ResourcePool():
	def __init__(self):
		self.size = 3

    
	def draw(self, view, position):
		view.images.images["resource_pool_zone"].draw(view.screen, position)
		view.images.images["resource_pool"].draw(view.screen, position)


