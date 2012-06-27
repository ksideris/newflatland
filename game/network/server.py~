#!/usr/bin/env python
#
# The core networking module. Transmits the serialized state to the clients-phones and reads their

import logging
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
import cPickle as pickle,time



class GameStateTransmitter(RequestHandler):

	def get(self):
		gest= self.request.arguments
		env = pickle.load(  open( "env.p", "rb" ) )  
		
		if(env<>None):
			self.write(env)
		else:
			self.write('move along sir,nothing to see here')
		self.flush()
		
		self.finish()
		'''try:
			gestures = pickle.load(  open( "gest.p", "rb" ) ) 
			gestures.append((self.request.arguments['action'],time.time()))
			if(len(gestures)>10):
				gestures=gestures[1:]
			pickle.dump(gestures, open( "gest.p", "wb" ) )
		except Exception:
			print Exception
		'''
		#print gestures
class Server():

	def start(self,server_address,server_port):
	
	
		app = Application([('/', GameStateTransmitter)])
		app.listen(server_port, address=server_address)
	   
		IOLoop.instance().start()


if __name__ == '__main__':
	s=Server()
	s.start('192.168.1.102','7020')
