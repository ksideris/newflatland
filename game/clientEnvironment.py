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
import httplib,asyncore,socket


import time
import pickle,sys #TODO change to cPickle for speed


class HTTPClient(asyncore.dispatcher):

    def __init__(self, host,port, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, port) )
        self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
		global count
		s= self.recv(500)
		if(len(s)>0):
		    print len(s),s	
		    #print pickle.loads(s)
		    #pickle.dump(s, open( "ClientData.p", "wb" ) )

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]




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
            #client = HTTPClient('192.168.1.102',7022, '/?id=2&action=attack')
            #asyncore.loop()         
            
            conn = httplib.HTTPConnection(self.server_address+':'+self.server_port)
            conn.request("GET", '/?id=1&action=attack')
            
            s = conn.getresponse()
            data =s.read(700)
            pickle.dump(data, open( "ClientData.p", "wb" ) )
            #print time.time()-start
            #
        except Exception:
			print 'a', sys.exc_info()[0]

    def updateState(self):
        s=None
        try:
            s = pickle.load(open( "ClientData.p", "rb" ) )
            #print s
            #pickle.dump([], open( "ClientData.p", "wb" ) )
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
		self._renderCall = LoopingCall(self.Update) #TODO can i avoid it?
		self._requestCall = LoopingCall(self.MakeRequest) #TODO can i avoid it?
		self._renderCall.start(0.03)	
		self._requestCall.start(0.01)	


	#FUNCTIONS FOR NETWORKING

	
    def deSerialize(self):
		s=''
		for p in self.players.itervalues():
			s+= str(p.player_id)+'&'+str(p.team)+'&'+str(p.position)+'&'+str(p.sides)+'&'+str(p.resources )+'&'+str(p.action)+'$'
		for b in self.buildings.itervalues():
			s+= str(b.sides)+'&'+str(b.team)+'&'+str(b.position)+'&'+str(b.sides)+'&'+str(b.resources )+'$'
		return s


	
 
