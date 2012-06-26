#!/usr/bin/env python
#
# Downloads a large file in chunked encoding with both curl and simple clients

import logging
from tornado.curl_httpclient import CurlAsyncHTTPClient #not necessary - should remove
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line #not necessary - should remove
from tornado.web import RequestHandler, Application


class GameState():
	def __init__(self):
		self.playerLocs = []
		self.playerStates = []
		for i in range(10):	
			self.playerLocs.append((i,20+2*i,30))
			self.playerStates.append((i,'10000011010'))
		
	def asString(self):
		rvalue=''
		for tup in self.playerLocs:	
			rvalue+='('+str(tup[0])+','+str(tup[1])+','+str(tup[2])+'),'
		print len(rvalue)
		return rvalue
state= GameState().asString()

class GameStateTransmitter(RequestHandler):

	def get(self):
		global state
		        
		self.write(state)
		self.flush()
		
		self.finish()

def start(server_address,server_port):
    parse_command_line()
    app = Application([('/', GameStateTransmitter)])
    app.listen(server_port, address=server_address)
   
    IOLoop.instance().start()


if __name__ == '__main__':
    start('192.168.1.102','7020')
