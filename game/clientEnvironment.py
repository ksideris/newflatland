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


import time
import pickle,sys #TODO change to cPickle for speed



class Environment(): #in an MVC system , this would be a controller
    ''' The environment class contains the state of the game. The server has the master version, the clients have slave versions (updated through the network) '''



    def __init__(self):
		'''State: Players,Buildings, Time, Resourse Pool'''
		self.players 	= {}
		self.buildings 	= {}
		self.TimeLeft = 0 
		#self.conn = 
		self.width = 80.0
		self.height = 48.0
		self.view =None
		self.ResourcePool = ResourcePool()
		self.client = AsyncClient()
    

    def updateState(self):
        s=None
        try:
            s = pickle.load(open( "ClientData.p", "rb" ) )
        except Exception:
			print sys.exc_info()[0]
        
        if(s<>None):
            try:
                players =  pickle.loads(s)
                self.players.clear()
                for p in players.itervalues():
                    #print p
                    self.players[id(p)] = p
            except Exception:
			    print 'b',sys.exc_info()[0]
        else:
            print 'None?'
            
    def Update(self):
		
		self.updateState()
		self.view.paint()
	

    def start(self):
		'''controls the environment by initiating the looping calls'''

		
		self.view.start('c')
		self.client.start('192.168.1.102','7022')
		self._renderCall = LoopingCall(self.Update) 
		self._requestCall = LoopingCall(self.client.MakeRequest) 
		self._renderCall.start(0.03)	
		self._requestCall.start(0.03)	


	#FUNCTIONS FOR NETWORKING

	
    def deSerialize(self):
		s=''
		for p in self.players.itervalues():
			s+= str(p.player_id)+'&'+str(p.team)+'&'+str(p.position)+'&'+str(p.sides)+'&'+str(p.resources )+'&'+str(p.action)+'$'
		for b in self.buildings.itervalues():
			s+= str(b.sides)+'&'+str(b.team)+'&'+str(b.position)+'&'+str(b.sides)+'&'+str(b.resources )+'$'
		return s


	
 
