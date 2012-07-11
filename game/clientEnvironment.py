#TODO UPDATE documentation
'''
Environment contains all the higher level state of the game.
Naturally, the server keeps one, but each client/player has
there own copy as well.

* It contains the top level paint function [!!!] This is where the HUD is generated and drawn
* It is where network messages are received, and passed along to the player module
NOTE: All the network functions come in pairs, the function name, and observe_<function name>
You call the un-prefixed function, if you are the originator of some state change, and subsequently
the observe_ prefixed function will get called by all the other players, server etc...
'''

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
        pass

    def updateTime(self):
		self.Tick+=0.03
		if( self.TimeLeft<=0):
		    self.GameOver =True
            
    def Update(self):
		self.deSerialize()
		self.updateTime()
		self.readGestures()
		self.view.paint(self.Tick )
		
    def makeRequest(self,action,Position):
        #print self.action
        self.client.MakeRequest(self.playerID,self.team,action,Position)
        
        self.action = 0

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
                self.players.clear()
                for p in players.itervalues():                    
                    self.players[id(p)] = p
                    if p.player_id == self.playerID:
                                p.position = Vector2D(self.Position)
                                p.action = self.action

                buildings =  pickle.loads(t[1]) #update buildings
                self.buildings.clear()
                for b in buildings.itervalues():                    
                    self.buildings[id(b)] = b

                self.ResourcePool = pickle.loads(t[2])
                self.scores =pickle.loads(t[3])
                self.TimeLeft =int(t[4])
                #if(abs(self.Tick-float(t[5]) ) > 1):
                #    
                #self.Tick =float(t[5])
 
