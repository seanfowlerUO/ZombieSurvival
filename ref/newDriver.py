__author__ = 'Sean Fowler'
import pygame, guns, mapper, random, globals,levelClass,driverState

from pygame.locals import *
from classes import *

from functions import *


#I am not sure if I want to use groups or not yet
'''
self.level.waitingHorde=pygame.sprite.RenderUpdates()
self.level.activeHorde=pygame.sprite.RenderUpdates()
'''



class Driver:

    def __init__(self,level):

        #level should be an instance of Level()
        self.level=level

        self.preWaveState=driverState.PreWaveState(self)
        self.waveState=driverState.WaveState(self)
        self.clickToFire=driverState.ClickToFire(self)
        self.gameOverState=driverState.GameOverState(self)
        self.completeState=driverState.CompleteState(self)
        self.testingState=driverState.TestingState(self)
        self.demoMode=driverState.DemoState(self)

        self.demo=False

        self.state=self.preWaveState

        self.gameWorld=self.level.gameWorld
        self.graphicsHandeler=self.level.graphicsHandeler

        self.hud=[Element('../images/items_menu.png',(100,globals.DISPLAY_HEIGHT/2))]


        self.lastSpawn=0
        self.killAll=False

    def nextLevel(self):
        ''' not sure if this is the best way to do it...'''
        self.running=False

    def mainLoop(self):
        pygame.init()
        self.initialized=pygame.time.get_ticks()
        self.graphicsHandeler.initialDraw()
        self.running=True
        while self.running==1:
            #print globals.FPS_CLOCK.get_fps()
            globals.FPS_CLOCK.tick(globals.FPS)
            if self.killAll==True:
                for zed in self.level.activeHorde:
                    zed.kill()
                for zed in self.level.waitingHorde:
                    zed.kill()
            if self.state!=self.gameOverState:
                self.state.catchEvents()
                self.gameWorld.spawn()
                self.gameWorld.move()
                self.gameWorld.checkCollisions()
                self.gameWorld.attack()
                self.gameWorld.checkStatus()
                self.gameWorld.update()
                self.graphicsHandeler.draw()
                if self.state==self.testingState:
                    self.level.layer6.add(self.graphicsHandeler.testingElement)
                else:

                    self.graphicsHandeler.testingElement.kill()
            else:
                self.state.catchEvents()
                self.graphicsHandeler.gameOver()





if __name__== "__main__":

#for now levels will just be here
    loadingImage=pygame.image.load('../images/loading.png')
    loadingRect=loadingImage.get_rect()

    SQUAD=[classes.Squad('../images/squad1_handToHand.png'),classes.Squad('../images/squad3_handToHand.png'),classes.Squad('../images/squad4_handToHand.png')]
    CIVILIANS=[classes.Civilian('../images/girl_3.png'),classes.Civilian('../images/girl_1.png'),classes.Civilian('../images/girl_2.png')]
    SQUAD[0].switchWeapons(guns.Shotgun())
    SQUAD[1].switchWeapons(guns.Pistol())
    SQUAD[2].switchWeapons(guns.Sniper())
    SQUAD[0].critical=True
    SQUAD[1].critical=True
    SQUAD[2].critical=True
    OVERLAYS=[classes.Element('../images/level1_roof.png',(920,480))]

    LEVEL_1x1=levelClass.Level(1.1,'../images/level1.png','maps/1x1_schematic.txt',0,50,500,3,SQUAD,CIVILIANS,OVERLAYS)
    LEVEL_1x1.addInanimate(classes.BucketOfWater)
    LEVEL_1x1.player.switchWeapons(guns.Glock())
    LEVEL_1x1.player.secondaryWeapon=guns.Shotgun()
    program=Driver(LEVEL_1x1)
    program.mainLoop()