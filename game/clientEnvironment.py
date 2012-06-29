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



class Environment(): #in an MVC system , this would be a controller
    ''' The environment class contains the state of the game. The server has the master version, the clients have slave versions (updated through the network) '''

    

    def __init__(self):
		'''State: Players,Buildings, Time, Resourse Pool'''
		self.players 	= {}
		self.buildings 	= {}
		self.TimeLeft = 15*60 
		self.width = 80.0
		self.height = 48.0
		self.view =None
		self.GameOver =False
		self.playerID =1
		self.action = 0
		self.lastAction = 0# time at which we activated the last action. Used to regulate action activations
		self.team =1
		self.otherTeam = 2 if self.team==1 else  1 
		self.scores =[0,0]
		self.IsServer = False
		self.ResourcePool = None
		self.client = AsyncClient()
    

    def readGestures(self):
        self.action = 1 #attack

    def updateTime(self):
		
		if(	self.TimeLeft<=0):
		    self.GameOver =True
		       
    def Update(self):
		self.deSerialize()
		self.updateTime()
		self.readGestures()
		self.view.paint()
	
    def makeRequest(self):
        self.client.MakeRequest(self.playerID,random.randint(1,3))


    def start(self):
		'''controls the environment by initiating the looping calls'''

		
		self.view.start('client')
		self.client.start('192.168.1.102','7022')
		self._renderCall = LoopingCall(self.Update) 
		self._requestCall = LoopingCall(self.makeRequest) 
		self._renderCall.start(0.03)	
		self._requestCall.start(0.03)	


	#FUNCTIONS FOR NETWORKING
	
    def deSerialize(self):
        s=None
        try:
            s = pickle.load(open( "ClientData.p", "rb" ) )
        except Exception:
			print 'Error Loading Client Data',sys.exc_info()[0]
        
        if(s<>None):
            t = s.split('$')
            #print len(t)
            try:
                players =  pickle.loads(t[0]) #update players
                self.players.clear()
                for p in players.itervalues():                    
                    self.players[id(p)] = p

                buildings =  pickle.loads(t[1]) #update buildings
                self.buildings.clear()
                for b in buildings.itervalues():                    
                    self.buildings[id(b)] = b
                self.ResourcePool = pickle.loads(t[2])
                self.scores =pickle.loads(t[3])
                self.TimeLeft =int(t[4])

                
            except Exception:
			    print 'Something went wrong while deserializing:',sys.exc_info()[0]
        else:
            print sys.exc_info()[0]


	
 
