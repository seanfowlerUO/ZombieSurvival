import pygame,gameWorld,classes,graphicsHandler,sys
from squad import *
from pygame.locals import *
from globals import *
class Driver(object):
    def __init__(self):
        super(Driver,self).__init__()
        self.gameWorld = gameWorld.GameWorld()
        self.graphicsHandler = graphicsHandler.GraphicsHandler(self.gameWorld)
    
    def mainLoop(self):
        CLOCK.tick(FPS)
        self.catchEvents() #Probably end up having driverStates
        self.gameWorld.spawn()
        self.gameWorld.move()
        self.gameWorld.checkCollisions()
        self.gameWorld.update()
        self.gameWorld.attack()
        self.graphicsHandler.draw()
        
    def catchEvents(self):
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                    if (event.key==K_w)\
                       or (event.key==K_a)\
                       or (event.key==K_s)\
                       or (event.key==K_d):
                        self.gameWorld.player.move(event.key)
    
                    elif event.key==K_ESCAPE:
                        sys.exit()

                    elif event.key==K_p:
                        print self.gameWorld.player.leadership
                        if len(self.gameWorld.player.squad.members)!=0:
                            print self.gameWorld.player.squad.members[0].tactics
                    
                    elif event.key==K_1:
                        self.gameWorld.player.squad.setFormation(SingleFile)
                    elif event.key==K_2:
                        self.gameWorld.player.squad.setFormation(DoubleStaggered)
                    elif event.key==K_3:
                        self.gameWorld.player.squad.setFormation(Wedge)
                    elif event.key==K_4:
                        self.gameWorld.player.squad.setFormation(FiveStar)
                    
                    # Tactic Modifiers
                    elif event.key==K_RIGHTBRACKET:
                        if self.gameWorld.player.leadership<10:
                            self.gameWorld.player.leadership+=1
                    elif event.key==K_LEFTBRACKET:
                        if self.gameWorld.player.leadership>1:
                            self.gameWorld.player.leadership-=1
                    elif event.key==K_EQUALS:
                        if len(self.gameWorld.player.squad.members)!=0:
                            if self.gameWorld.player.squad.members[0].tactics<10:
                                for m in self.gameWorld.player.squad.members:
                                    m.tactics+=1
                    elif event.key==K_MINUS:
                        if len(self.gameWorld.player.squad.members)!=0:
                            if self.gameWorld.player.squad.members[0].tactics>1:
                                for m in self.gameWorld.player.squad.members:
                                    m.tactics-=1
                                     
            elif event.type==KEYUP:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                   or (event.key==K_d):
                    self.gameWorld.player.stop(event.key)
                    
        if pygame.mouse.get_pressed()==(0,0,1):
            if self.gameWorld.player.nextAttack<=pygame.time.get_ticks() or self.gameWorld.player.nextAttack==True:
                projs = self.gameWorld.player.attack(pygame.mouse.get_pos())
                if type(projs)==type([]):
                    for projectile in projs:
                        self.gameWorld.projectiles.add(projectile)

                