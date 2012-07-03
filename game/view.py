# Python
from collections import deque

# pyGame
import pygame,time,pygame.mixer

# twisted
from twisted.python.filepath import FilePath
from twisted.internet.task import LoopingCall

# local
from vector import Vector2D
from settings import Images


def loadImage(path):
    """
    Load an image from the L{FilePath} into a L{pygame.Surface}.

    @type path: L{FilePath}

    @rtype: L{pygame.Surface}
    """
    return pygame.image.load(path.path)

sounds = dict()

def _initSounds():
#    pygame.mixer.init(frequency=16000)#, size=-8, channels=1)
    sounds["trigger trap"] = pygame.mixer.Sound("data/sfx/alex_sfx/Trigger Trap.wav")
    sounds["explosion"] = pygame.mixer.Sound("data/sfx/alex_sfx/Attack Hit.wav")

    sounds["attack"] = pygame.mixer.Sound("data/sfx/alex_sfx/attack.wav")
    sounds["poly armor full"] = pygame.mixer.Sound("data/sfx/alex_sfx/Points Full.wav")
    sounds["player upgrade"] = pygame.mixer.Sound("data/sfx/alex_sfx/You upgraded.wav")

    sounds["accept upgrade"] = pygame.mixer.Sound("data/sfx/alex_sfx/accept_upgrade.wav")

    sounds["gain poly armor"] = pygame.mixer.Sound("data/sfx/alex_sfx/gain resource.wav")
    sounds["lose poly armor"] = pygame.mixer.Sound("data/sfx/alex_sfx/pay resource.wav")
    sounds["poly armor depleted"] = pygame.mixer.Sound("data/sfx/alex_sfx/resources depleted.wav")

    sounds["mining"] = pygame.mixer.Sound("data/sfx/alex_sfx/In Resource Pool(loop).wav")

    sounds["building",3] = pygame.mixer.Sound("data/sfx/alex_sfx/Building 3-sided.wav")
    sounds["building",4] = pygame.mixer.Sound("data/sfx/alex_sfx/Building 4-sided.wav")
    sounds["building",5] = pygame.mixer.Sound("data/sfx/alex_sfx/Building 5-sided.wav")

    sounds["finish building",3] = pygame.mixer.Sound("data/sfx/alex_sfx/Finish 3-sided.wav")
    sounds["finish building",4] = pygame.mixer.Sound("data/sfx/alex_sfx/Finish 4-sided.wav")
    sounds["finish building",5] = pygame.mixer.Sound("data/sfx/alex_sfx/Finish 5-sided.wav")

    sounds["scanning"] = pygame.mixer.Sound("data/sfx/alex_sfx/Sweeping.wav")

def getSound(strIdx, nIndex = None):
    if not nIndex == None:
        return sounds[strIdx, nIndex]
    else:
        return sounds[strIdx]



class AnimatedActions():

    PLAYER_ATTACK       = 1
    PLAYER_SCAN         = 2
    PLAYER_BUILD        = 3
    PLAYER_UPGRADE      = 4
    PLAYER_DOWNGRADE    = 5
    PLAYER_LOSE_RESOURCE= 6
    PLAYER_GAIN_RESOURCE= 7
    BUILDING_UPGRADED   = 8
    BUILDING_ATTACKED   = 9
    BUILDING_EXPLODED   = 10

    def __init__(self):  
        #animation related variables
        self.animationCounter = 0 
        self.animationFps =0
        self.animationSize = 0 
        self.animation = [] 
        self.animationLastFired = 0 
        

    def addAnimation(self,animtype,clean):
        
        if(len(self.animation)==0 or clean):
                self.animation = []
                self.animationFps = 30                
                self.animationLastFired =time.time()
                self.animationCounter = 0 
                self.animationSize = 6 
            
        if(animtype == AnimatedActions.PLAYER_ATTACK): 
                pygame.mixer.Channel(1).play(getSound("attack"))
                self.animation.append("Attack")
        elif(animtype == AnimatedActions.PLAYER_BUILD): 
                if not pygame.mixer.Channel(2).get_busy():
                            pygame.mixer.Channel(2).play(getSound("mining"))
                else:
                            pygame.mixer.Channel(2).queue(getSound("mining"))
                self.animation.append("mining")
        elif(animtype == AnimatedActions.PLAYER_UPGRADE):
                pygame.mixer.Channel(3).play(getSound("player upgrade")) 
                pygame.mixer.Channel(2).stop()
                self.animation.append("LevelUp")
        elif(animtype == AnimatedActions.PLAYER_DOWNGRADE):
                pygame.mixer.Channel(4).play(getSound("lose poly armor")) 
                self.animation.append("LevelUp")
        elif(animtype == AnimatedActions.PLAYER_LOSE_RESOURCE): 
                pygame.mixer.Channel(4).play(getSound("lose poly armor")) 
        elif(animtype == AnimatedActions.PLAYER_GAIN_RESOURCE): 
                pygame.mixer.Channel(4).play(getSound("gain poly armor")) 
        elif(animtype == AnimatedActions.BUILDING_ATTACKED): 
                self.animation.append("BuildingAttacked")
        elif(animtype == AnimatedActions.BUILDING_EXPLODED):
                pygame.mixer.Channel(5).play(getSound("trigger trap"))
                pygame.mixer.Channel(6).play(getSound("explosion")) 
                self.animation.append("TrapExplosion")
        elif(animtype == AnimatedActions.BUILDING_UPGRADED): 
                pygame.mixer.Channel(7).play(getSound("finish building", 3), 0)
                pygame.mixer.Channel(2).stop()
                self.animation.append("building upgraded")
    
    def drawAnimation(self,view, position):
        if(len(self.animation)==0):
                return
        if(self.animationCounter>= self.animationSize):
                self.animationCounter = 0 
                self.animationLastFired = time.time() 
                self.animation = self.animation[1:] 
                return
        else:
                anim = view.images.images[self.animation[0]]
                image = anim.getImage(self.animationCounter)
                image.draw(view.screen, position)
                if(time.time()-  self.animationLastFired>1.0/self.animationFps ):
                    self.animationCounter+=1       


class Window(object):
    def __init__(self, environment):
        self.environment = environment
        _initSounds()
        self.environment.view = self
        self.images = Images(FilePath("data").child("img2"))
        self.images.load()
        self.center = Vector2D((0,0))


    def paint(self): # Draw Background
        """
        Call C{paint} on all views which have been directly added to
        this Window.
        """
        bg = self.images.images["background"]
        bgWidth = bg.width
        bgHeight = bg.height
        x = -(self.center * 20).x
        y = -(self.center * 20).y
        while x > 0:
            x -= bgWidth;
        while y > 0:
            y -= bgHeight
        while x < self.screen.get_width():#800:#480:
            j = y
            while j < self.screen.get_height():#480:#800:
                self.screen.blit(bg._image, pygame.Rect(x, j, bgWidth, bgHeight))
                j += bgHeight
            x += bgWidth

        self.drawEnvironment()
       	self.drawHUD()
		
        pygame.display.flip()
       	pygame.time.Clock().tick(300)
    def isVisible(self, entity):
        if not self.environment.team:
            return True
        # See objects on your team
        if self.environment.team == entity.team:
            return True
        # Object in range of my sentries
        for b in self.environment.buildings.itervalues():
            if b.isSentry() and (b.team == self.environment.team) and (entity.position - b.position).length < b.SENTRY_RANGE*5.0:
                return True
            
        # object in range of a scanning player
        for p in self.environment.players.itervalues():
            if (self.environment.team == p.team):
                if (entity.position - p.position).length < p.getScanRadius()*5 :
                    return True
        
        return False

    

    def drawEnvironment(self):
		'''Draw the state of the environment. This is called by view after drawing the background. 
		   This function draws the timer and calls the drawing functions of the players/buildings/resource pool'''
		if(self.environment.ResourcePool<>None):
		    self.environment.ResourcePool.draw(self,self.screenCoord(Vector2D(0,0)))

		for b in self.environment.buildings.itervalues():
                        self.drawBuilding(b,self.screenCoord(b.position),self.isVisible(b))
			
		for p in self.environment.players.itervalues(): 
			self.drawPlayer(p,self.screenCoord(p.position),self.isVisible(p))
			
    def drawPlayer(self,player,position,isVisible):

        if isVisible:
                image = self.images.images["Player", player.team, player.sides]
                image.draw(self.screen, position)
                
                player.animations.drawAnimation(self, position)
                
                for i in range(0,player.resources):
                        self.images.images["Armor", player.sides, i+1].draw(self.screen, position)
                
                if player.scanning.isScanning():
                        self.images.images["PlayerScan"].drawScaled(self.screen, position, player.getScanRadius())
                        if not pygame.mixer.Channel(7).get_busy():
                                pygame.mixer.Channel(7).play(getSound("scanning"))
                                pygame.mixer.Channel(7).fadeout(4000)
        else:
                image = self.images.images["Enemy", player.team]
                image.draw(self.screen, position)

    def drawBuilding(self,building,position,isVisible):
        
        building.animations.drawAnimation(self, position)

        if not (building.sides and building.resources):
                return 0

        if isVisible:
                
                if building.sides:
                        self.images.images["Building", building.sides, building.team].draw(self.screen, position)
                if building.sides >= 3:
                        self.images.images["Building Zone", building.sides, building.team].draw(self.screen, position)
                        self.images.images["BuildingHealth", building.team, building.sides, building.resources].draw(self.screen, position)
                if building.isSentry():
                        self.images.images["SentryScan"].drawScaled(self.screen, position, building.SENTRY_RANGE)


    def drawHUD(self): 
        ''' Draw the HUD . It includes scores, time, and other info'''

        #Draw time left
        minRemaining = self.environment.TimeLeft / 60
        secRemaining = self.environment.TimeLeft % 60
        secStr = str(secRemaining)
        if secRemaining <= 9: secStr = "0" + secStr

        minStr = str(minRemaining)
        if minRemaining <= 9: minStr = "0" + minStr
        
        if(self.environment.IsServer):
            font = pygame.font.Font("data/Deutsch.ttf", 70)
            text = font.render(minStr + ":" + secStr, True, (255, 255, 255))
            
            textrect = text.get_rect(left = 15, top = 40)
        else:
            

            font = pygame.font.Font("data/Deutsch.ttf", 35)
            text = font.render(minStr + ":" + secStr, True, (255, 255, 255))
            text = pygame.transform.rotate(text, 270)
      
            textrect = text.get_rect(left = 15, bottom = 410)

        self.screen.blit(text,textrect)

        #Draw the scores
		
        fontColors = [(255, 0, 0), (0,255,255)]
        if(self.environment.IsServer): 
            
            font = pygame.font.Font("data/Deutsch.ttf", 35)
            text = font.render(str(self.environment.scores[0]), True, fontColors[0])
            textrect = text.get_rect(right =735, top = 40)
            self.screen.blit(text,textrect)

            text = font.render(str(self.environment.scores[1]), True, fontColors[1])
		
            textrect = text.get_rect(right =735, top = 80)
        else:
            font = pygame.font.Font("data/Deutsch.ttf", 35)
            text = font.render(str(self.environment.scores[0]), True, fontColors[0])
            text = pygame.transform.rotate(text, 270)
            textrect = text.get_rect(right =735, bottom = 410)
            self.screen.blit(text,textrect)
            text = font.render(str(self.environment.scores[1]), True, fontColors[1])
            text = pygame.transform.rotate(text, 270)
            textrect = text.get_rect(right = 775, bottom = 410)
        
        self.screen.blit(text,textrect)

        #GAMEOVER
        if self.environment.GameOver:
            endGameMessage = ""
            if self.environment.IsServer:
                scoreDifference = self.environment.scores[0] - self.environment.scores[1]
                if scoreDifference > 0:
                    endGameMessage = "RED WINS!"
                elif scoreDifference < 0:
                    endGameMessage = "BLUE WINS!"
                else:
                    endGameMessage = "DRAW!"
                font = pygame.font.Font("data/Deutsch.ttf", 140)
                
                text = font.render(endGameMessage, True, (255,255,255))
                textrect = text.get_rect(centery =240, centerx = 400)

            else:
                scoreDifference = self.environment.scores[self.environment.team-1] > self.environment.scores[self.environment.otherTeam-1]
                if scoreDifference > 0:
                    endGameMessage = "YOU WIN!"
                elif scoreDifference < 0:
                    endGameMessage = "YOU LOSE!"
                else:
                  endGameMessage = "DRAW!"
                font = pygame.font.Font("data/Deutsch.ttf", 70)

                text = font.render(endGameMessage, True, (255,255,255))
                text = pygame.transform.rotate(text, 270)
                textrect = text.get_rect(centery =240, centerx = 400)
            self.screen.blit(text,textrect)
        
        
    def setCenter(self, position):
        self.center = position

    def worldCoord(self, p):
        width = self.screen.get_width()
        height = self.screen.get_height()
        (cx, cy) = self.screen.get_rect().center
        return Vector2D(((p.x - cx) * self.environment.width) / width,
                        ((p.y - cy) * self.environment.height) / height)

    def screenCoord(self, p):
        width = self.screen.get_width()
        height = self.screen.get_height()
        (cx, cy) = self.screen.get_rect().center
        return Vector2D((((p.x - self.center[0]) / (self.environment.width / 2)) * width) + cx,
                        (((p.y - self.center[1]) / (self.environment.height / 2)) * height) + cy)

    def start(self, title):
        self.screen = pygame.display.get_surface()
        pygame.display.set_caption(title)
    
        
        (cx, cy) = self.screen.get_rect().center

    def stop(self):
        self._renderCall.stop()
