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





class Player():
        IDLE    = 0
        ATTACK  = 1
        SCAN    = 2
        BUILD    = 3
        UPGRADE    =4
        def __init__(self):
                self.player_id=-1
                self.team=0
                
                self.position = Vector2D(random.randint(1, 10), random.randint(1, 10)) 
                self.sides = 3
                self.resources = 2
                self.action = None 
                self.partialResources = 0 
                self.NoPartial = 3 

                #animation related variables
                self.animationCounter = 0 
                self.animationFps =0
                self.animationSize = 0 
                self.animation = [] 
                self.animationLastFired = 0 

        def drawAnimation(self,view, position):
            if(self.animationCounter>= self.animationSize):
                self.animationCounter = 0 
                self.animationLastFired = time.time() 
                self.animation = self.animation[1:] 
                return
            else:
                anim = view.images.images[self.animation[0]]
                image = anim.getImage(self.animationCounter)
                image.draw(view.screen, position)
                if(time.time()-  self.animationLastFired>1.0/self.animationFps ):
                    self.animationCounter+=1
            
            
        
        def draw(self,view, position, isVisible):
            if isVisible:
                image = view.images.images["Player", self.team, self.sides]
                image.draw(view.screen, position)
                if( len(self.animation)>0):
                        self.drawAnimation(view, position)
                
                for i in range(0,self.resources):
                        view.images.images["Armor", self.sides, i+1].draw(view.screen, position)
            else:
                image = view.images.images["Enemy", self.team]
                image.draw(view.screen, position)

        def hit(self):
                if self.resources:
                    self.resources -= 1
                else:
                    self.addAnimation( Player.UPGRADE)
                    if self.sides>0:
                        self.sides -= 1  
        def mine(self):   
                self.partialResources += 1
                if self.partialResources==self.NoPartial :
                        self.partialResources=0
                        if self.sides < 3:
                                self.sides += 1
                                self.addAnimation( Player.UPGRADE)
                        elif self.resources < self.sides:
                                self.resources += 1
                
        def addAnimation(self,animtype):

                if(len(self.animation)==0):
                        self.animationFps = 30                
                        self.animationLastFired =time.time()
                        self.animationCounter = 0 
                        self.animationSize = 6 
            
                if(animtype == Player.ATTACK): 
                        self.animation.append("Attack")
                elif(animtype == Player.BUILD): 
                        self.animation.append("mining")

                elif(animtype == Player.UPGRADE): 
                        self.animation.append("LevelUp")
                        
                
            
             



class Building():
        UPGRADED = 1
        ATTACKED = 2
        EXPLODED = 3

        def __init__(self):
                self.sides = 3
                self.resources = 1
                self.team=0
                self.size = 1 #TODO make size variable depending on type, then determine range by it.
                self.partialResources = 0 
                self.position =-1
                self.partialResources = 0 
                self.NoPartial = 3 


                self.animationCounter = 0 
                self.animationFps =0
                self.animationSize = 0 
                self.animation = [] 
                self.animationLastFired = 0 

        def drawAnimation(self,view, position):
            if(self.animationCounter>= self.animationSize):
                
                self.animationCounter = 0 
                self.animationLastFired = time.time() 
                self.animation = self.animation[1:] 
                return
            else:
                anim = view.images.images[self.animation[0]]
                image = anim.getImage(self.animationCounter)
                image.draw(view.screen, position)
                if(time.time()-  self.animationLastFired>1.0/self.animationFps ):
                    self.animationCounter+=1
            
        def explode(self,player):
                
                self.addAnimation(Building.EXPLODED)
                player.sides = 0
                player.resources = 0
                self.sides=0
                
                


    
        def build(self,player):
                self.partialResources += 1
                if self.partialResources==self.NoPartial :
                        self.partialResources=0
                        buildingLeveledUp = False
                        if not self.sides:
                            if self.resources == 2:
                                self.sides = 3
                                self.resources = 0
                                buildingLeveledUp = True
                            else:
                                self.resources += 1
                                player.resources -=1
                        elif self.sides<5 or self.resources<5:
                            # if armor is full
                            if self.sides == self.resources :
                                self.sides += 1
                                self.resources = 1
                                buildingLeveledUp = True
                            else:
                                self.resources += 1
                                player.resources -=1

                        if buildingLeveledUp:
                            
                                self.addAnimation(Building.UPGRADED)
                

        def isTrap(self):
                if self.sides == 3:
                        return True
                return False

        def isSentry(self):
                return self.sides == 4

        def isPolyFactory(self):
                return self.sides == 5

        def hit(self):
                self.addAnimation(Building.ATTACKED)
                if not (self.sides and self.resources):
                    return 0
                elif self.resources:
                    self.resources -= 1
                    return self.resources
                    

      
        def draw(self,view, position,isVisible):
            if( len(self.animation)>0):
                        self.drawAnimation(view, position)
            if not (self.sides and self.resources):
                return 0

            if isVisible:
                if self.sides >= 3:
                        view.images.images["Building Zone", self.sides, self.team].draw(view.screen, position)
                if self.sides:
                        view.images.images["Building", self.sides, self.team].draw(view.screen, position)
                        view.images.images["BuildingHealth", self.team, self.sides, self.resources].draw(view.screen, position)
                else:
                        image = view.images.images["Building", self.resources, self.team].draw(view.screen, position) 
                
                
        
        def addAnimation(self,animtype):
                if(len(self.animation)==0):
                        self.animationFps = 30                
                        self.animationLastFired =time.time()
                        self.animationCounter = 0 
                        self.animationSize = 6 

                if(animtype == Building.ATTACKED): 
                        self.animation.append("BuildingAttacked")

                elif(animtype == Building.EXPLODED): 
                        self.animation.append("TrapExplosion")
              

                elif(animtype == Building.UPGRADED): 
                        self.animation.append("building upgraded")

                
class ResourcePool():
        def __init__(self):
                self.size = 3
                self.position =Vector2D(0,0)

    
        def draw(self, view, position):
                view.images.images["resource_pool_zone"].draw(view.screen, position)
                view.images.images["resource_pool"].draw(view.screen, position)


