import pygame
from pygame.locals import *
from globals import *

class GraphicsHandler(object):
    def __init__(self,gameWorld):
        super(GraphicsHandler,self).__init__()
        self.gameWorld = gameWorld
        
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT), 1 | FULLSCREEN)        
    
    def draw(self):
        self.screen.blit(self.gameWorld.background.image,self.gameWorld.background.rect)
        rectList = self.gameWorld.allSprites.draw(self.screen)
        rectList +=self.gameWorld.screenEdges.draw(self.screen)
        #pygame.display.update(rectList) 
        pygame.display.flip()