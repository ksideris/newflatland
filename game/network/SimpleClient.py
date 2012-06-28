

import httplib,pickle,time,sys

SHOW_STATISTICS =True
class SimpleClient():

    def MakeRequest(self):
        player_id=1
        try:
            actions = ['attack','idle','scan','build']
            start=time.time()   
     
            
            conn = httplib.HTTPConnection(self.server_address+':'+self.server_port)
            conn.request("GET", '/?id=1&action=attack')
            
            s = conn.getresponse()
            data =s.read()
            pickle.dump(data, open( "ClientData.p", "wb" ) )
            
            if(SHOW_STATISTICS):
                print 'Time Taken:',time.time()-start
            
        except Exception:
			print 'Exception in Simple Client:', sys.exc_info()[0]

    def start(self,serv_addr,serv_port):
        self.server_address = serv_addr
        self.server_port =   serv_port
