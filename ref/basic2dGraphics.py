__author__ = 'Sean Fowler'
import pygame,globals,classes
pygame.font.init()
font2=pygame.font.Font('freesansbold.ttf',60)
font1=pygame.font.Font('freesansbold.ttf',20)
gameOverImage=font2.render('GAME OVER',1,(255,0,0))
gameOverRect = gameOverImage.get_rect(center=(globals.DISPLAY_WIDTH/2,globals.DISPLAY_HEIGHT/2))

testingImage=font1.render('TESTING MODE',1,(255,0,0))
testingRect=testingImage.get_rect(left=0,bottom=globals.DISPLAY_HEIGHT)




class GraphicsHandeler(object):
    def __init__(self):
        super(GraphicsHandeler,self).__init__()


    def draw(self):
        pass

class Basic2dGraphics(GraphicsHandeler):
    def __init__(self,level):
        super(Basic2dGraphics,self).__init__()
        self.testingElement=classes.Element(testingImage,testingRect,1)
        #level should be an instance of Level()
        self.level=level
        self.levelNumber=level.number
        self.map=level.map
        self.size= self.width, self.height =globals.DISPLAY_WIDTH, globals.DISPLAY_HEIGHT
        self.screen=pygame.display.set_mode(self.size,1 | pygame.FULLSCREEN)

        self.gameWorld=self.level.gameWorld




    def initialDraw(self):
        self.screen.blit(self.level.mapImage,self.level.mapRect)
        #self.level.underlays.draw(self.screen)
        self.level.allSprites.draw(self.screen)
        self.level.hud.draw(self.screen)
        self.level.overlays.draw(self.screen)
        pygame.display.flip()

    def drawOld(self):
        self.screen.blit(self.level.mapImage,self.level.mapRect)
        #self.level.underlays.draw(self.screen)
        self.level.allSprites.draw(self.screen)
        self.level.hud.draw(self.screen)
        self.level.overlays.draw(self.screen)
        pygame.display.update(self.level.dirtyRect)
        self.level.dirtyRect=pygame.sprite.Rect(0,0,0,0)

    def draw(self):
        rect=[]
        rect=rect+self.level.layer1.draw(self.screen)
        rect=rect+self.level.layer2.draw(self.screen)
        rect=rect+self.level.layer3.draw(self.screen)
        rect=rect+self.level.layer4.draw(self.screen)
        rect=rect+self.level.layer5.draw(self.screen)
        rect=rect+self.level.layer6.draw(self.screen)
        pygame.display.update(rect)

    def gameOver(self):
        pygame.display.flip()
        self.screen.blit(gameOverImage,gameOverRect)






