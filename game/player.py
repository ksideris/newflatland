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
import random,time

IDLE    =0
ATTACK  =1
SCAN    =2
MINE    =3
UPGRADE    =3

class Player():
	def __init__(self):
		self.player_id=-1
		self.team=0
		self.animationCounter = 0 
		self.animationEnd = 0 
		self.animation = None 
		self.animationLastFired = 0 
		self.armor = dict()
		self.position = Vector2D(random.randint(1, 10), random.randint(1, 10)) 
		self.sides = 3
		self.resources = 0
		self.action = 0 
		

	def drawAnimation(self,view, position):
	    if(self.animationCounter>= self.animationEnd):
	        self.animationCounter = 0 
	        self.animationLastFired = 0 
	        self.animation = None 
	        return
	    else:
	        anim = view.images.images[self.animation]
	        image = anim.getImage(self.animationCounter)
	        image.draw(view.screen, position)
            if(time.time()-  self.animationLastFired>0.03 ):
                self.animationCounter+=1
            
            
        
	def draw(self,view, position, isVisible):
	    if isVisible:
	        image = view.images.images["Player", self.team, self.sides]
	        image.draw(view.screen, position)
	        if( self.animation <> None):
	            self.drawAnimation(view, position)
	            '''updated=self.animation.update() 
	            if(updated<>None):
	                updated.draw(view.screen, position)#drawAnimation(view, position)
	            else:
	                self.animation = None'''
	    else:
	        image = view.images.images["Enemy", self.team]
	        image.draw(view.screen, position)
	    
        
	def addAction(self,action,view):
	    if(self.animation == None):
	        self.action   =action
	        self.animation = "mining"
	        self.animationLastFired =time.time()
	        self.animationCounter = 0 
	        self.animationEnd = 3 
	    
             



class Building():
	def __init__(self):
		self.sides = 5
		self.resources = 3
		self.team=1
		self.size = 1
		self.position = Vector2D(random.randint(-10, 10), random.randint(-10, 10))

	def draw(self,view, position,isVisible):
	    if isVisible:
	        if self.sides:
	            view.images.images["Building", self.sides, self.team].draw(view.screen, position)
	            view.images.images["BuildingHealth", self.team, self.sides, self.resources].draw(view.screen, position)
	        else:
	            image = view.images.images["Building", self.resources, self.team].draw(view.screen, position)
		
class ResourcePool():
	def __init__(self):
		self.size = 3

    
	def draw(self, view, position):
		view.images.images["resource_pool_zone"].draw(view.screen, position)
		view.images.images["resource_pool"].draw(view.screen, position)


