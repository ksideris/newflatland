

#!/usr/bin/env python

"""clientEnvironment.py: Environment contains all the higher level state of the game.
This is the client version. The relation between server-client is a master/slave
one. That is the client reads the current state and updates itself. It also
notifies the server of any client side events (actions /position updates)

"""

__author__      = "Konstantinos Sideris"
__copyright__   = "Copyright 2012, UCLA game lab"



import pygame
from vector import Vector2D
from game.player import Player,Building,ResourcePool
from game.network.SimpleClient import SimpleClient
from game.network.asyncClient import AsyncClient
from twisted.internet.task import LoopingCall


import time,random
import pickle,sys #TODO change to cPickle for speed

import shelve,os
CLIENTLOCALDATA = 'ClientLocalData.db'

class Environment(): #in an MVC system , this would be a controller
    ''' The environment class contains the state of the game. The server has the master version, the clients have slave versions (updated through the network) '''
    ATTACK_RADIUS = 3
    SCAN_RADIUS = 3
    FPS=30
    

    def __init__(self,player_id,team,serverIP,serverPort):
		'''State: Players,Buildings, Time, Resourse Pool'''
		self.players 	= {}
		self.buildings 	= {}
		self.TimeLeft = 15*60 
		self.width = 80.0
		self.height = 48.0
		self.view =None
		self.GameOver =False
		self.playerID =player_id
		self.player = None
		self.action = 0
		self.attemptedAction = 0
		self.lastAction = 0
		self.ActionTimeout = 1
		
		self.team =team
		self.otherTeam = 2 if self.team==1 else  1 
		self.scores =[0,0]
		self.IsServer = False
		self.ResourcePool = None
		self.client = AsyncClient()
		self.serverIP =serverIP
		self.serverPort = serverPort
                self.Tick = 0
                self.Position = (0,0)
                self.lastUpdate = 0

    def readGestures(self):
     
            if(self.player.action == Player.ATTACK): #ATTACK
                                self.handleAttack()

            elif(self.player.action == Player.BUILD): #building
                                self.handleBuild()

            elif(self.player.action == Player.UPGRADE): #building
                                self.handleUpgrade()

            elif(self.player.action == Player.SCAN): #building
                                self.handleScan()

            elif(self.player.action == Player.IDLE):
                                self.handleIdle()
                                              
           ## for b in self.buildings.itervalues():
            ##            if   (b.getPosition() - self.player.getPosition()).length < b.size and b.isTrap() and b.team<>self.player.team:         
             ##                           b.explode(self,self.Tick)   
        

    def handleAttack(self):
                if(self.player.sides>=3):
                        self.player.performAttack(self.Tick)  
                       
    def handleBuild(self):
                ACTION = "BUILD"
                if((self.ResourcePool.getPosition()-self.player.getPosition()).length< self.ResourcePool.size):
                        ACTION ="MINE"
                else:
                        for b in self.buildings.itervalues():
                                
                                if(b.team == self.player.team and b.isPolyFactory() and b.resources == 5 and (b.getPosition()- player.getPosition()).length <b.size):
                                        ACTION ="MINE"
                                        break      
                if( ACTION =="MINE"):
                        self.player.performBuild(self.Tick)  
                        
                                         
                else:
                        if(self.player.resources>0):
                                BUILDING =None
                                for b in self.buildings.itervalues():
                                        if   (b.getPosition() - self.player.getPosition()).length < b.size:
                                                BUILDING =b
                                                break
                                

                                if BUILDING.team ==self.player.team:
                                        self.player.performBuild(self.Tick) 
        
    def handleUpgrade(self):
                allowedUpgradeLoc = False
                if((self.ResourcePool.getPosition()-self.player.getPosition()).length< self.ResourcePool.size):
                        allowedUpgradeLoc=True
                else:
                        for b in self.buildings.itervalues():
                                if(b.team == self.player.team and b.isPolyFactory() and b.resources == 5 and (b.getPosition()- self.player.getPosition()).length <b.size): 
                                        allowedUpgradeLoc=True
                                        break
                if(allowedUpgradeLoc):
                       self.player.upgrade(self.Tick) 

    def handleScan(self):
             self.player.scan(self.Tick)    

    def handleIdle(self):

             pass  
      
    def updateTime(self):
		self.Tick+= 1.0/Environment.FPS
		#if( self.TimeLeft<=0):
		#    self.GameOver =True
            
    def Update(self):
		self.deSerialize()
		self.updateTime()
		self.updatePositions()
		#self.readGestures()
		self.view.paint(self.Tick )
                
		
    def makeRequest(self,action,Position):
        #print self.action
        if self.player:
            self.player.action = action
            self.player.position = Position
            self.readGestures()
        self.client.MakeRequest(self.playerID,self.team,action,Position)
        
        self.action = 0
    
    def updatePositions(self):
            for playerId in self.players:
                     
                     if self.players[playerId].player_id <> self.playerID:
                         
                         self.players[playerId].updatePosition( 1.0/Environment.FPS)
                     
    def start(self):
		'''controls the environment by initiating the looping calls'''

		self.lastUpdate =time.time()
		self.view.start('client-'+str(self.playerID))
		self.client.start(self.serverIP,self.serverPort)
		
                if os.path.exists(CLIENTLOCALDATA.split('.')[0]+str(self.playerID)+'.'+CLIENTLOCALDATA.split('.')[1]):		
                    os.remove(CLIENTLOCALDATA.split('.')[0]+str(self.playerID)+'.'+CLIENTLOCALDATA.split('.')[1])
		
		self._renderCall = LoopingCall(self.Update) 
		#self._requestCall = LoopingCall(self.makeRequest) 
		self._renderCall.start(1.0/Environment.FPS)	
		#self._requestCall.start(1.0/Environment.FPS)	


	#FUNCTIONS FOR NETWORKING
	
    def deSerialize(self):
        state=None
        localdb = shelve.open(CLIENTLOCALDATA.split('.')[0]+str(self.playerID)+'.'+CLIENTLOCALDATA.split('.')[1])
        if localdb.has_key('data'):
                
            try:

                state = localdb['data']['string']             

            finally:
                localdb.close()
                    
            if(state<>None):
                t = state.split('$')
                players =  pickle.loads(t[0]) #update players
                #self.players.clear()
                                      
                for p in players.itervalues():
                    found =False
                    pkey = 0
                    if p.player_id == self.playerID and self.player==None:
                        self.player = p
                        self.players[id( self.player)] = self.player
                        
                      
                    for ep in self.players.itervalues():
                            
                        if ep.player_id == p.player_id:
                               
                                found=True
                                pkey = id(ep)
                                break
                    if found:
                        if p.player_id == self.playerID:
                                   
                                    self.players[pkey].position = self.player.position
                                    self.players[pkey].action = self.player.position

                        else:
                            self.players[pkey].targetPosition = p.position
                            self.players[pkey].action = p.action
                            self.players[pkey].animations.extend(p.animations)

                        self.players[pkey].sides = p.sides
                        self.players[pkey].resources = p.resources
                        self.players[pkey].partialResources = p.partialResources

                        
                    else:
                        self.players[id(p)]=p

                buildings =  pickle.loads(t[1]) #update buildings
                self.buildings.clear()
                for b in buildings.itervalues():                    
                    self.buildings[id(b)] = b

                self.ResourcePool = pickle.loads(t[2])
                self.scores =pickle.loads(t[3])
                self.TimeLeft =int(t[4])
                
               
                self.GameOver = not bool(t[6]) #weird
              
