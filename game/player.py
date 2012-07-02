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
from game.view import AnimatedActions
import random,time



class PlayerScan:
    def __init__(self):
        self.reset()

    def reset(self):
        self.startTime = 0
        self._radius = 0
        self._isScanning = False

    def start(self):
        
        self.startTime = time.time()
        self._isScanning = True

    def stop(self,radius):
        self._isScanning = False
        self._radius = radius-.01
        self.startTime = time.time()

    def radius(self):

        if self.startTime == 0:
            return 0

        dt = (time.time() - self.startTime)*1000.0
        
        if(dt<1000):
                value = 2*(min(1, (dt / 1000.0)  * .9) + 0.1)
                self._radius=value
        else:
                value = self._radius * (1 - ((dt-1000.0) / 5000.0))
                if(value<0):
                        value=0
                        self._isScanning = False
   
        return  value



    def isScanning(self):
        return self._isScanning


class Player():
        IDLE    = 0
        ATTACK  = 1
        SCAN    = 2
        BUILD    = 3
        UPGRADE    =4

        def __init__(self):
                self.player_id=-1
                self.team=0
                self.animations = AnimatedActions()
                self.position = Vector2D(random.randint(1, 10), random.randint(1, 10)) 
                self.sides = 3
                self.resources = 2
                self.partialResources = 0 
                self.NoPartial = 3 
                self.action = 0
                self.scanning = PlayerScan()
            
        def getScanRadius(self):
                return self.scanning.radius()

        def hit(self):
                if self.resources:
                    self.resources -= 1
                else:
                    self.animations.addAnimation( AnimatedActions.PLAYER_UPGRADE)
                    if self.sides>0:
                        self.sides -= 1 
                        if(self.sides>2):
                                self.resources = self.sides   
        def mine(self):   
                self.partialResources += 1
                if self.partialResources==self.NoPartial :
                        self.partialResources=0
                        if self.sides < 3:
                                self.sides += 1
                                self.animations.addAnimation( AnimatedActions.PLAYER_UPGRADE)
                        elif self.resources < self.sides:
                                self.resources += 1
        def upgrade(self):
                if(self.sides >= 3 and self.sides==self.resources and self.sides<6):
                       self.animations.addAnimation( AnimatedActions.PLAYER_UPGRADE)
                       self.resources=0
                       self.sides+=1 

        def scan(self):
                if(not self.scanning.isScanning()):
                        self.scanning.start()
        
        def performAttack(self):
                self.animations.addAnimation(AnimatedActions.PLAYER_ATTACK)

        def performBuild(self):
                self.animations.addAnimation(AnimatedActions.PLAYER_BUILD)
                        
                
            
             



class Building():
        UPGRADED = 1
        ATTACKED = 2
        EXPLODED = 3
        
        SENTRY_RANGE = 2.75

        def __init__(self):
                self.sides = 1
                self.resources = 1
                self.team=1
                self.size = 1 #TODO make size variable depending on type, then determine range by it.
                self.partialResources = 0 
                self.position =-1
                self.partialResources = 0 
                self.NoPartial = 3 
                self.animations = AnimatedActions()

            
        def explode(self,player):
                
                self.animations.addAnimation(AnimatedActions.BUILDING_EXPLODED)

                player.sides = 0
                player.resources = 0
                self.sides=0            
                


    
        def build(self,player):
                self.partialResources += 1
                if self.partialResources==self.NoPartial :
                        self.partialResources=0
                        buildingLeveledUp = False
                        
                        player.resources -=1
                        if self.sides==2:
                                self.sides = 3
                                self.resources = 1
                                buildingLeveledUp = True
                           
                        elif self.sides<5 or self.resources<5:
                            # if armor is full
                            if self.sides == self.resources :
                                self.sides += 1
                                self.resources = 1
                                buildingLeveledUp = True
                            else:
                                self.resources += 1

                        if buildingLeveledUp:
                                self.size = self.sides
                                self.animations.addAnimation(AnimatedActions.BUILDING_UPGRADED)
                

        def isTrap(self):
                if self.sides == 3:
                        return True
                return False

        def isSentry(self):
                return self.sides == 4

        def isPolyFactory(self):
                return self.sides == 5

        def hit(self):
                self.animations.addAnimation(AnimatedActions.BUILDING_ATTACKED)
                if not (self.sides and self.resources):
                    return 0
                elif self.resources:
                    self.resources -= 1
                    return self.resources               

      
       


                
class ResourcePool():
        def __init__(self):
                self.size = 6.5
                self.position =Vector2D(0,0)

    
        def draw(self, view, position):
                view.images.images["resource_pool_zone"].draw(view.screen, position)
                view.images.images["resource_pool"].draw(view.screen, position)


