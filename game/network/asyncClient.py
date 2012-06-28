import asyncore, socket,pickle,time,string

SHOW_STATISTICS =True
class HTTPClient(asyncore.dispatcher):

    def __init__(self, host,port, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, int(port)) )
        self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
		
		s= self.recv(20000)
		if(len(s)>0):
		    bodyIndex =  string.index(s, "\r\n\r\n") +4
		    pickle.dump(s[bodyIndex:], open( "ClientData.p", "wb" ) )
		    
		    #print s[:86]
    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


class AsyncClient():

    def MakeRequest(self):

        start =time.time()
    
        client = HTTPClient(self.server_address,self.server_port, '/?id=2&action=attack')
        asyncore.loop(0.03)
    
        
        if(SHOW_STATISTICS):
            print 'Time Taken:',time.time()-start

   
    
    def start(self,serv_addr,serv_port):
        
        self.server_address = serv_addr
        self.server_port =   serv_port