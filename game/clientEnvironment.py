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
from twisted.internet.task import LoopingCall
import httplib


import time
import pickle,sys #TODO change to cPickle for speed


class Environment(): #in an MVC system , this would be a controller
    ''' The environment class contains the state of the game. The server has the master version, the clients have slave versions (updated through the network) '''

    server_address  = '192.168.1.102'
    server_port     = '7022'

    

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
		

    def MakeRequest(self):
        player_id=1
        try:
            actions = ['attack','idle','scan','build']
            start=time.time()            
            conn = httplib.HTTPConnection(self.server_address+':'+self.server_port)
            conn.request("GET", '/?id=1&action=attack')
            
            s = conn.getresponse()
            print time.time()-start
            #pickle.dump(s, open( "ClientData.p", "wb" ) )
        except Exception:
			print sys.exc_info()[0]
    def Update(self):
		
		
		self.view.paint()
	

    def start(self):
		'''controls the environment by initiating the looping calls'''

		
		self.view.start('c')
		self._renderCall = LoopingCall(self.Update) #TODO can i avoid it?
		self._requestCall = LoopingCall(self.MakeRequest) #TODO can i avoid it?
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


	
 
