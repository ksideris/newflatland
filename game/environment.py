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

import time,random
import pickle,sys #TODO change to cPickle for speed

import shelve

class Environment(): #in an MVC system , this would be a controller
        ''' The environment class contains the state of the game. The server has the master version, the clients have slave versions (updated through the network) '''
        NEXT_PLAYER_ID=1
        FPS=30
        ATTACK_DISTANCE =3
        BUILDING_DISTANCE =6
        GAME_DURATION = 15*60#15 seconds #15 * 60 # 15 minutes
    
        def __init__(self):
                '''State: Players,Buildings, Time, Resourse Pool'''
                self.players    = {}
                self.buildings  = {}
                self.TimeLeft = 0 
                self.TrueTimeLeft = 0         
                self.scores =[0,0]     
                self.GameOver =False
                self.GameStarted =False
                self.width = 80.0
                self.height = 48.0
                self.view =None
                self.team =None
                self.actions =None
                self.IsServer = True
                self.ResourcePool = ResourcePool()
                

        #Helper Functions
        def createPlayer(self, player_id,team):
                '''add a player to the given team'''
                player = Player()
                player.team = team

                playerId = id(player)
                player.player_id = player_id
                #player.player_id = Environment.NEXT_PLAYER_ID
                #Environment.NEXT_PLAYER_ID = Environment.NEXT_PLAYER_ID + 1
        
                self.players[playerId] = player
        
                return player

        def createBuilding(self, team,pos):
                '''add a building to the given team'''
                building = Building()
                building.team = team
                building.position =pos
                bid = id(building)
                self.buildings[bid] = building
                
        
                return building

        
        def StartGame(self):
                self.GameStarted=True
                for playerId in self.players:
                     self.players[playerId].sides=3
                     self.players[playerId].resources=0
                     
                self.buildings.clear()

                
        def updateTime(self):
                if(self.GameStarted):
                        self.TrueTimeLeft-=1.0/Environment.FPS
                        self.TimeLeft = int(self.TrueTimeLeft)  
                        if(     self.TrueTimeLeft<=0):
                            self.GameOver =True
                            self.TrueTimeLeft =0




        def Update(self):
                
                startTime = time.time()
                self.updateTime()
                self.scores =self.calculateScores()
                if(self.actions<>None):
                        self.processNewState()
                self.view.paint()
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key==pygame.K_s:
                                        self.StartGame()
                print time.time()-startTime
        def processNewState(self):
            
                for action in self.actions:
                    found= False
                    for playerId in self.players:
                        if(self.players[playerId].player_id)==int(action[0]):
                            self.players[playerId].action=int(action[2])
                            pos = action[3].split(',')
                            self.players[playerId].position = Vector2D(float(pos[0]),float(pos[1]))
                            found =True
                            break

                    if(not found):
                        self.createPlayer(int(action[0]),int(action[1]))
                     

                for playerId in self.players:
                        
                        player = self.players[playerId]
                        

                        if(player.action == Player.ATTACK): #ATTACK
                                self.handleAttack(player)

                        elif(player.action == Player.BUILD): #building
                                self.handleBuild(player)

                        elif(player.action == Player.UPGRADE): #building
                                self.handleUpgrade(player)

                        elif(player.action == Player.SCAN): #building
                                self.handleScan(player)

                        elif(player.action == Player.IDLE):
                                self.handleIdle(player)
                                              
                        for b in self.buildings.itervalues():
                             if   (b.position - player.position).length < b.size and b.isTrap() and b.team<>player.team:         
                                        b.explode(player)   
        

        def handleAttack(self,player):
                player.performAttack()  
                for p in self.players.itervalues():
                        if (p.team != player.team) and (p.position - player.position).length < Environment.ATTACK_DISTANCE:
                                p.hit()
                for b in self.buildings.itervalues():
                        if (b.team != player.team) and (b.position - player.position).length < Environment.ATTACK_DISTANCE:
                                b.hit()

        def handleBuild(self,player):
                ACTION = "BUILD"
                if((self.ResourcePool.position-player.position).length< self.ResourcePool.size):
                        ACTION ="MINE"
                else:
                        for b in self.buildings.itervalues():
                                
                                if(b.team == player.team and b.isPolyFactory() and b.resources == 5 and (b.position- player.position).length <b.size):
                                        ACTION ="MINE"
                                        break      
                if( ACTION =="MINE"):
                        player.performBuild()  
                        player.mine()
                                         
                else:
                        if(player.resources>0):
                                BUILDING =None
                                for b in self.buildings.itervalues():
                                        if   (b.position - player.position).length < b.size:
                                                BUILDING =b
                                                break
                                if BUILDING ==None :
                                        self.createBuilding(  player.team, player.position)                       
                                        player.resources-=1 

                                elif BUILDING.team ==player.team:
                                        player.performBuild() 
                                        BUILDING.build(player) 
        
        def handleUpgrade(self,player):
                allowedUpgradeLoc = False
                if((self.ResourcePool.position-player.position).length< self.ResourcePool.size):
                        allowedUpgradeLoc=True
                else:
                        for b in self.buildings.itervalues():
                                if(b.team == player.team and b.isPolyFactory() and b.resources == 5 and (b.position- player.position).length <b.size): 
                                        allowedUpgradeLoc=True
                                        break
                if(allowedUpgradeLoc):
                       player.upgrade() 

        def handleScan(self,player):
             player.scan()    

        def handleIdle(self,player):

             pass  

        def start(self):
                '''controls the environment by initiating the looping calls'''
                self.TrueTimeLeft=Environment.GAME_DURATION
                self.TimeLeft = int(self.TrueTimeLeft)
                self.view.start('Server')
                self._renderCall = LoopingCall(self.Update)
                self._renderCall.start(1.0/Environment.FPS)
                self._writeCall = LoopingCall( self.writeStateToServer )
                self._writeCall.start(1.0/Environment.FPS) 
                self._readCall = LoopingCall( self.readStateFromServer)
                self._readCall.start(1.0/Environment.FPS) 
                


        def calculateScores(self):
        
                score=[0,0]
                for team in range(1,3):
                    for playerId in self.players:

                            player = self.players[playerId]

                            if player.team == team:
                                score[team-1] += player.sides
                                score[team-1] += player.resources

                    for buildingId in self.buildings:
                            building = self.buildings[buildingId]
                            if building.team == team:
                                score[team-1]  += building.sides
                                score[team-1]  += building.resources
                    score[team-1] *= 1000
                return score ;


        #FUNCTIONS FOR NETWORKING
        def writeStateToServer(self):
                string =self.cSerialize()
                
                serv_db = shelve.open('ServerState.db')
                try:
                        serv_db['data']= { 'time': str(time.time()), 'string': string }                      
                finally:
                        serv_db.close()
                
        def readStateFromServer(self):

                client_db = shelve.open('ClientState.db')
                try:
                        self.actions =[]
                        for key in client_db:
                                self.actions.append(client_db[key]['string'].split('$'))
                        
                finally:
                        client_db.close()
                '''  
                try:

                        
                        actionFile =  open( "ServerOut.p", "rb" )         
                        self.actions     = pickle.load(  actionFile )
                        actionFile.close()
                        actionFile =  open( "ServerOut.p", "wb" )     
                        pickle.dump( [],  actionFile )
                        actionFile.close()
                       
                except Exception:
                        print 'env1',sys.exc_info()[0]
                '''
                #print self.actions   

        def cSerialize(self):

                s=pickle.dumps(self.players)+'$'+pickle.dumps(self.buildings)+'$'+\
                pickle.dumps(self.ResourcePool)+'$'+pickle.dumps(self.scores)+'$'+str(self.TimeLeft)
                #print len(s),s         
                return s

        

        def _serialize(self):
                s =''
                for p in self.players.itervalues():
                        s+= pickle.dumps(p)+'$'
                for b in self.buildings.itervalues():
                        s+= pickle.dumps(b)+'$'
                
                return s
        def Serialize(self):
                s=''
                for p in self.players.itervalues():
                        s+= str(p.player_id)+'&'+str(p.team)+'&'+str(p.position)+'&'+str(p.sides)+'&'+str(p.resources )+'$'+str(partialResources.resources )+'&'+str(p.action)+'$'
                for b in self.buildings.itervalues():
                        s+= str(b.sides)+'&'+str(b.team)+'&'+str(b.position)+'&'+str(b.sides)+'&'+str(b.resources )+'$'
        
                return s
        
 
