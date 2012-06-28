# Python
from collections import deque

# pyGame
import pygame

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



class Window(object):
    def __init__(self, environment):
        self.environment = environment
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


    def drawEnvironment(self):
		'''Draw the state of the environment. This is called by view after drawing the background. 
		   This function draws the timer and calls the drawing functions of the players/buildings/resource pool'''
		if(self.environment.ResourcePool<>None):
		    self.environment.ResourcePool.draw(self,self.screenCoord(Vector2D(0,0)))

		for b in self.environment.buildings.itervalues():
		# draw all buildings. TODO : should i restrict to viewport for speed?
			b.draw(self,self.screenCoord(b.position))

		for p in self.environment.players.itervalues(): 
		# draw all players. TODO : should i restrict to viewport for speed?
			p.draw(self,self.screenCoord(p.position))

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
