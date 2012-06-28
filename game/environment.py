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

import time
import pickle,sys #TODO change to cPickle for speed

GAME_DURATION = 15*60#15 seconds #15 * 60 # 15 minutes

class Environment(): #in an MVC system , this would be a controller
	''' The environment class contains the state of the game. The server has the master version, the clients have slave versions (updated through the network) '''
	NEXT_PLAYER_ID=1
    
	def __init__(self):
		'''State: Players,Buildings, Time, Resourse Pool'''
		self.players 	= {}
		self.buildings 	= {}
		self.TimeLeft = 0 
		
		self.width = 80.0
		self.height = 48.0
		self.view =None
		self.ResourcePool = ResourcePool()
		

	#Helper Functions
	def createPlayer(self, team):
		'''add a player to the given team'''
		player = Player()
		player.team = team

		playerId = id(player)
		player.player_id = Environment.NEXT_PLAYER_ID
		Environment.NEXT_PLAYER_ID = Environment.NEXT_PLAYER_ID + 1
        
		self.players[playerId] = player
        
		return player

	def createBuilding(self, team):
		'''add a building to the given team'''
		building = Building()
		building.team = team
		bid = id(building)
		self.buildings[bid] = building
        
		return building

	
	def draw(self,view):
		'''Draw the state of the environment. This is called by view after drawing the background. 
		   This function draws the timer and calls the drawing functions of the players/buildings/resource pool'''
		
		self.ResourcePool.draw(view,view.screenCoord(Vector2D(0,0)))

		for b in self.buildings.itervalues():# draw all buildings. TODO : should i restrict to viewport for speed?
			b.draw(view,view.screenCoord(b.position))

		for p in self.players.itervalues(): # draw all players. TODO : should i restrict to viewport for speed?
			p.draw(view,view.screenCoord(p.position))
		
	def Update(self):
		for p in self.players.itervalues():
				p.position+=Vector2D(.2,0)
                if(p.position[0]>20 or p.position[1]>20 ):
                    p.position+=Vector2D(-40,0)
		self.writeStateToServer()
		self.readStateFromServer()
		self.processNewState()
		self.view.paint()
	
	def processNewState(self):
		for action in self.actions:
			print action
	
	def start(self):
		'''controls the environment by initiating the looping calls'''

		pickle.dump( [], open( "ServerOut.p", "wb" ) )
		self.view.start('Server')
		self._renderCall = LoopingCall(self.Update) #TODO can i avoid it?
		self._renderCall.start(0.03)	


	#FUNCTIONS FOR NETWORKING
	def writeStateToServer(self):
				
		pickle.dump( self.cSerialize(), open( "ServerIn.p", "wb" ) )
		
		
	def readStateFromServer(self):
				
		try:
			self.actions = pickle.load(  open( "ServerOut.p", "rb" ) ) 
			#if(len(self.actions)>0):		
			#	print 'read',self.actions
			pickle.dump( [], open( "ServerOut.p", "wb" ) )
		except Exception:
			print 'env1',sys.exc_info()[0]
	
	def Serialize(self):
		s=''
		for p in self.players.itervalues():
			s+= str(p.player_id)+'&'+str(p.team)+'&'+str(p.position)+'&'+str(p.sides)+'&'+str(p.resources )+'&'+str(p.action)+'$'
		for b in self.buildings.itervalues():
			s+= str(b.sides)+'&'+str(b.team)+'&'+str(b.position)+'&'+str(b.sides)+'&'+str(b.resources )+'$'
        
		return s

	def cSerialize(self):
		
		s=pickle.dumps(self.players)#+'$'+pickle.dumps(self.buildings)
		#print len(s),s		
		return s

	

	def _serialize(self):
		s =''
		for p in self.players.itervalues():
			s+= pickle.dumps(p)+'$'
		for b in self.buildings.itervalues():
			s+= pickle.dumps(b)+'$'
		
		return s
	
 
