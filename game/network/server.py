#!/usr/bin/env python
#
# Downloads a large file in chunked encoding with both curl and simple clients

import logging
from tornado.curl_httpclient import CurlAsyncHTTPClient #not necessary - should remove
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line #not necessary - should remove
from tornado.web import RequestHandler, Application
import cPickle as pickle


class GameState():
	def __init__(self,environment):
		self.environment = environment
		
		
	'''This should not be here. It should go under the server'''
	def serialize(self):
		s =''
		for p in self.environment.players.itervalues():
			s+= pickle.dumps(p)+'$'
		for b in self.environment.buildings.itervalues():
			s+= pickle.dumps(b)+'$'
		
		return s

	def cSerialize(self):
		s =''
		s=pickle.dumps(self.environment.players)+'$'+pickle.dumps(self.environment.buildings)
		return s

	def ccSerialize(self):
		s=''
		for p in self.environment.players.itervalues():
			s+= str(p.player_id)+'&'+str(p.team)+'&'+str(p.position[0])+'&'+str( p.position[1])+'&'+str(p.sides)+'&'+str(p.resources )+'&'+str(p.action)+'$'
		for b in self.environment.buildings.itervalues():
			s+= str(b.sides)+'&'+str(b.team)+'&'+str(b.position[0])+'&'+str( b.position[1])+'&'+str(b.sides)+'&'+str(b.resources )+'&'+str(b.action)+'$'
		return s

_gamestate =None
class GameStateTransmitter(RequestHandler):

	def get(self):
		
		env = pickle.load(  open( "env.p", "rb" ) )  
		if(env<>None):
			self.write(env)
		else:
			self.write('move along sir,nothing to see here')
		print 'a'
		self.flush()
		
		self.finish()

class Server():

	def start(self,server_address,server_port):
	
	
		app = Application([('/', GameStateTransmitter)])
		app.listen(server_port, address=server_address)
	   
		IOLoop.instance().start()


if __name__ == '__main__':
	s=Server()
	s.start('192.168.1.102','7020')
