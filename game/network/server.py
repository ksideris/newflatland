#!/usr/bin/env python
#
# The core networking module. Transmits the serialized state to the clients-phones and reads their

import logging
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
import pickle,time,sys #TODO change to cPickle for speed



class GameStateTransmitter(RequestHandler):
    GESTURE_HISTORY = 10
    def get(self):
        gest= self.request.arguments
        #print gest
        env = None
        try:
            env = pickle.load(  open( "ServerIn.p", "rb" ) )  
        except Exception:
            pass

        if(env<>None):
            self.write(env)
        else:
            self.write('move along sir,nothing to see here')
        self.flush()
		
        self.finish()
        try:
            gestures=[]
            gestures = pickle.load(  open( "ServerOut.p", "rb" ) ) 
            gestures.append((gest['id'],gest['action'],time.time()))
            #if(len(gestures)>self.GESTURE_HISTORY):
            #    gestures=gestures[1:]
            pickle.dump(gestures, open( "ServerOut.p", "wb" ) )
        except Exception:
            print sys.exc_info()[0]
        
		

	

class Server():

	def start(self,server_address,server_port):
	
	
		app = Application([('/', GameStateTransmitter)])
		app.listen(server_port, address=server_address)
	   
		IOLoop.instance().start()


if __name__ == '__main__':
	s=Server()
	s.start('192.168.1.102','7020')
