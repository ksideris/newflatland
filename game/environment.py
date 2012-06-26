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
from game.player import Player,Building

import time
import cPickle as pickle

GAME_DURATION = 15*60#15 seconds #15 * 60 # 15 minutes

class Environment():
    
	NEXT_PLAYER_ID=1
    
	def __init__(self):
		self.observers = []
		self.players = {}
		self.buildings = {}
		self.state = ''

	def createPlayer(self, team):
		player = Player()
		player.team = team

		playerId = id(player)
		player.player_id = Environment.NEXT_PLAYER_ID
		Environment.NEXT_PLAYER_ID = Environment.NEXT_PLAYER_ID + 1
        
		self.players[playerId] = player
        
		return player

	def createBuilding(self, team):
		building = Building()
		building.team = team
		bid = id(building)
		self.buildings[bid] = building
        
		return building

	def Serialize(self):
		s =''
		for playerId in self.players:
			s+= pickle.dumps(self.players[playerId])+'$'
		for buildingId in self.buildings:
			s+= pickle.dumps(self.buildings[buildingId])+'$'
		return s

	def cSerialize(self):
		s =''
		s=pickle.dumps(self.players)+'$'+pickle.dumps(self.buildings)
		return s
	def ccSerialize(self):
		s=''
		for playerId in self.players:
			s+= str(self.players[playerId].player_id)+'&'+str(self.players[playerId].team)+'&'+str(self.players[playerId].position[0])+'&'+str( self.players[playerId].position[1])+'&'+str(self.players[playerId].sides)+'&'+str(self.players[playerId].resources )+'&'+str(self.players[playerId].action)+'$'
		for buildingId in self.buildings:
			s+= str(self.buildings[buildingId].sides)+'&'+str(self.players[playerId].team)+'&'+str(self.players[playerId].position[0])+'&'+str( self.players[playerId].position[1])+'&'+str(self.players[playerId].sides)+'&'+str(self.players[playerId].resources )+'&'+str(self.players[playerId].action)+'$'
		return s


	
 
