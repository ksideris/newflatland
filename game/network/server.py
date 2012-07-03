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
            serverInfile=open( "ServerIn.p", "rb" ) 
            env = pickle.load( serverInfile )
            serverInfile.close()
        except Exception:
            print sys.exc_info()[0],'unpickling ServerIn'

        if(env<>None):
            self.write(env)
        else:
            self.write('move along sir,nothing to see here')
        self.flush()
		
        self.finish()
        gestures=[]
        try:
            serverOutfile=open( "ServerOut.p", "rb" )
            gestures =  pickle.load(  serverOutfile )
            serverOutfile.close()
            #gestures =[]    
            #print  gest   
            
            for g in gestures:
                if(gest['id']==g[0] and float(g[4][0])<float(gest['time'][0])):
                        gestures.remove(g)
            gestures.append((gest['id'],gest['team'],gest['action'],gest['pos'],gest['time']))
            #if(len(gestures)>self.GESTURE_HISTORY):
            #    gestures=gestures[1:]
            
        except Exception:
            print sys.exc_info()[0],'unpickling ServerOut'

        try:    
            serverOutfile=open( "ServerOut.p", "wb" )
            pickle.dump(gestures, serverOutfile)
            serverOutfile.close()	
        except Exception:
            print sys.exc_info()[0],'pickling ServerOut'
	

class Server():

	def start(self,server_address,server_port):
	
	
		app = Application([('/', GameStateTransmitter)])
		app.listen(server_port, address=server_address)
	   
		IOLoop.instance().start()


if __name__ == '__main__':
	s=Server()
	s.start('192.168.1.102','7020')
