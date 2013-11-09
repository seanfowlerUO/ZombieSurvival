__author__ = 'Sean Fowler'
import pygame, sys, classes,vector,guns
from pygame.locals import *

class DriverState(object):
    def __init__(self):
        super(DriverState,self).__init__()
        self.movables=None
        self.movingMovable=False

    def catchEvents(self):
        pass

class PreWaveState(DriverState):
    def __init__(self,driver):
        super(PreWaveState,self).__init__()

        self.spawning=False
        self.driver=driver
        self.movables=[]
        for movable in self.driver.level.squad:
            self.movables.append(movable)
        for movable in self.driver.level.inanimates:
            self.movables.append(movable)

    def catchEvents(self):
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if (event.key==K_w)\
                    or (event.key==K_a)\
                    or (event.key==K_s)\
                    or (event.key==K_d):
                    self.driver.level.player.move(event.key)

                if (event.key==K_q):
                    self.driver.level.player.swapWeapons()

                elif event.key==K_ESCAPE:
                    sys.exit()

                elif event.key==K_RETURN:
                    #NEEDS A SAFETY SO CAN'T START ON ACCIDENT
                    if not self.driver.demo==True:
                        self.driver.state=self.driver.clickToFire
                    else:
                        self.driver.state=self.driver.demoMode

            elif event.type==KEYUP:
                if (event.key==K_w)\
                    or (event.key==K_a)\
                    or (event.key==K_s)\
                    or (event.key==K_d):
                    self.driver.level.player.stop(event.key)

            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1:
                    (mx,my) = pygame.mouse.get_pos()
                    if self.movingMovable!=False:
                        for actor in self.movables:
                            if self.movingMovable==actor:
                                if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                    if not pygame.key.get_mods() & KMOD_SHIFT:
                                        actor.moveTo(pygame.mouse.get_pos())
                                        self.movingMovable=False
                                    else:
                                        actor.moveTo(pygame.mouse.get_pos(),True)


                                elif actor.rect.collidepoint(pygame.mouse.get_pos()):

                                    self.movingMovable=False

                        for spawnPoint in self.driver.level.itemSpawns:
                            if spawnPoint.spawning==True and self.movingMovable==spawnPoint:

                                if not spawnPoint.item=='bucketOfWater':
                                    self.driver.level.addInanimate(spawnPoint.spawnItem((((mx//40)*40)+20,((my//40)*40)+20)))
                                    #self.driver.level.dirtyRect=self.driver.level.dirtyRect.union(spawnPoint.rect)

                                    spawnPoint.spawning=False
                                    self.movingMovable=False
                                else:
                                    #if you are spawning a bucket of water
                                    color=self.driver.level.graphicsHandeler.screen.get_at((mx,my))
                                    if color==(0,127,0):
                                        self.driver.level.addInanimate(spawnPoint.spawnItem((((mx//40)*40)+20,((my//40)*40)+20)))
                                        self.driver.level.dirtyRect=self.driver.level.dirtyRect.union(spawnPoint.rect)
                                        self.driver.level.dirtyRect=self.driver.level.dirtyRect.union(spawnPoint.amountRect)
                                        self.driver.level.dirtyRect=self.driver.level.dirtyRect.union(spawnPoint.rect)
                                        self.movingMovable=False
                                        spawnPoint.spawning=False
                                    else:
                                        #give invalid placement warning
                                        pass
                        for item in self.driver.level.inanimates:
                            if self.movingMovable==item:
                                if item.rect.collidepoint((mx,my)):
                                    self.movingMovable=False
                                else:
                                    if not isinstance(item,classes.BucketOfWater):
                                        item.moveTo((mx,my))
                                        self.movingMovable=False
                                    else:
                                        color=self.driver.level.graphicsHandeler.screen.get_at((mx,my))
                                        if color==(0,127,0):
                                            item.moveTo((mx,my))
                                            self.movingMovable=False
                                        else:
                                            #Cannot place item here
                                            pass


                    else:
                        for actor in self.movables:
                            if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                pass
                            else:
                                if not pygame.key.get_mods() & KMOD_CTRL:
                                    self.movingMovable=actor
                                else:
                                    if isinstance(actor,classes.Squad):
                                        actor.swapWeapons()

                        for spawnPoint in self.driver.level.itemSpawns:
                            if spawnPoint.rect.collidepoint(pygame.mouse.get_pos()):
                                if spawnPoint.amount!=0:
                                    spawnPoint.spawning=True
                                    self.movingMovable=spawnPoint

                        for item in self.driver.level.inanimates:
                            if not item.rect.collidepoint(pygame.mouse.get_pos()):
                                pass
                            else:
                                self.movingMovable=item

                elif event.button==3:
                    for item in self.driver.level.inanimates:
                        if item.rect.collidepoint(pygame.mouse.get_pos()):
                            if isinstance(item,classes.Inanimate):
                                item.rotate()
                        else:
                            self.movingMovable=False

            elif event.type==pygame.QUIT:
                sys.exit()

class WaveState(DriverState):
    def __init__(self,driver):
        super(WaveState,self).__init__()
        self.driver=driver
        self.movables=[]
        for movable in self.driver.level.squad:
            self.movables.append(movable)

        self.spawning=True
    def catchEvents(self):
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                or (event.key==K_d):
                    self.driver.level.player.move(event.key)

                if (event.key==K_q):
                    self.driver.level.player.swapWeapons()

                elif event.key==K_ESCAPE:
                    sys.exit()

                elif event.key==K_RETURN:
                    #NEEDS A SAFETY SO CAN'T START ON ACCIDENT
                    pass

            elif event.type==KEYUP:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                or (event.key==K_d):
                    self.driver.level.player.stop(event.key)

            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1:
                    if self.movingMovable!=False:
                        for actor in self.movables:
                            if self.movingMovable==actor:
                                if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                    if not pygame.key.get_mods() & KMOD_SHIFT:
                                        actor.moveTo(pygame.mouse.get_pos())
                                        self.movingMovable=False
                                    else:
                                        actor.moveTo(pygame.mouse.get_pos(),True)


                                elif actor.rect.collidepoint(pygame.mouse.get_pos()):

                                    self.movingMovable=False
                    else:
                        for actor in self.movables:
                            if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                pass
                            else:
                                self.movingMovable=actor
                elif event.button==3:
                    self.movingMovable=False
            elif event.type==pygame.QUIT:
                sys.exit()

class ClickToFire(DriverState):
    def __init__(self,driver):
        super(ClickToFire,self).__init__()
        self.driver=driver
        self.movables=[]
        for movable in self.driver.level.squad:
            self.movables.append(movable)

        self.spawning=True

    def catchEvents(self):
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                or (event.key==K_d):
                    self.driver.level.player.move(event.key)
                if event.key==K_t:
                    self.driver.state=self.driver.testingState

                if (event.key==K_q):
                    self.driver.level.player.swapWeapons()

                elif event.key==K_ESCAPE:
                    sys.exit()

                elif event.key==K_k:
                    if pygame.key.get_mods() & KMOD_SHIFT and KMOD_CTRL:
                        self.driver.killAll=True
                elif event.key==K_RETURN:
                    #NEEDS A SAFETY SO CAN'T START ON ACCIDENT
                    pass

            elif event.type==KEYUP:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                or (event.key==K_d):
                    self.driver.level.player.stop(event.key)

            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1:
                    if self.movingMovable!=False:
                        for actor in self.movables:
                            if self.movingMovable==actor:
                                if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                    if not pygame.key.get_mods() & KMOD_SHIFT:
                                        actor.moveTo(pygame.mouse.get_pos())
                                        self.movingMovable=False
                                    else:
                                        actor.moveTo(pygame.mouse.get_pos(),True)


                                elif actor.rect.collidepoint(pygame.mouse.get_pos()):

                                    self.movingMovable=False
                    else:
                        for actor in self.movables:
                            if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                pass
                            else:
                                if not pygame.key.get_mods() & KMOD_CTRL:
                                    self.movingMovable=actor
                                else:
                                    if isinstance(actor,classes.Squad):
                                        actor.swapWeapons()
            elif event.type==pygame.QUIT:
                sys.exit()

        if pygame.mouse.get_pressed()==(0,0,1):
            self.movingMovable=False
            if (pygame.time.get_ticks()-self.driver.level.player.nextAttack>self.driver.level.player.lastAttack) and pygame.time.get_ticks()>self.driver.level.player.lastAttack:
                self.driver.level.player.shoot=True
                if self.driver.level.player.shoot==True:
                    (reloading,nextshot,projectiles) = self.driver.level.player.attack(pygame.mouse.get_pos())
                    for proj in projectiles:
                        self.driver.level.allSprites.add(proj)
                        self.driver.level.npcSprites.add(proj)
                        self.driver.level.layer2.add(proj)
                    self.driver.level.player.nextAttack=nextshot
                    self.driver.level.player.lastAttack=pygame.time.get_ticks()
                    if reloading==True:
                        self.driver.level.player.reloadingTimer=nextshot+pygame.time.get_ticks()
            self.driver.level.player.shoot=False





class GameOverState(DriverState):
    def __init__(self,driver):
        super(GameOverState,self).__init__()
        self.driver=driver
        self.spawning=False
        self.movables=[]

    def catchEvents(self):
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_RETURN or K_ESCAPE:
                    sys.exit()
            elif event.type==pygame.QUIT:
                sys.exit()

class CompleteState(DriverState):
    def __init__(self,driver):
        super(CompleteState,self).__init__()
        self.driver=driver
        self.movables=[]
        for movable in self.driver.level.squad:
            self.movables.append(movable)

        self.spawning=True

    def catchEvents(self):
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                or (event.key==K_d):
                    self.driver.level.player.move(event.key)

                if (event.key==K_q):
                    self.driver.level.player.swapWeapons()

                elif event.key==K_t:
                    self.driver.state=self.driver.testingState

                elif event.key==K_ESCAPE:
                    sys.exit()

                elif event.key==K_RETURN:
                    self.driver.nextLevel()

            elif event.type==KEYUP:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                or (event.key==K_d):
                    self.driver.level.player.stop(event.key)

            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1:
                    if self.movingMovable!=False:
                        for actor in self.movables:
                            if self.movingMovable==actor:
                                if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                    if not pygame.key.get_mods() & KMOD_SHIFT:
                                        actor.moveTo(pygame.mouse.get_pos())
                                        self.movingMovable=False
                                    else:
                                        actor.moveTo(pygame.mouse.get_pos(),True)


                                elif actor.rect.collidepoint(pygame.mouse.get_pos()):

                                    self.movingMovable=False
                    else:
                        for actor in self.movables:
                            if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                pass
                            else:
                                self.movingMovable=actor
            elif event.type==pygame.QUIT:
                sys.exit()
        if pygame.mouse.get_pressed()==(0,0,1):
            self.movingMovable=False
            if (pygame.time.get_ticks()-self.driver.level.player.nextAttack>self.driver.level.player.lastAttack) and pygame.time.get_ticks()>self.driver.level.player.lastAttack:
                self.driver.level.player.shoot=True
                if self.driver.level.player.shoot==True:
                    (reloading,nextshot,projectiles) = self.driver.level.player.attack(pygame.mouse.get_pos())
                    for proj in projectiles:
                        self.driver.level.allSprites.add(proj)
                        self.driver.level.npcSprites.add(proj)
                        self.driver.level.layer2.add(proj)
                    self.driver.level.player.nextAttack=nextshot
                    self.driver.level.player.lastAttack=pygame.time.get_ticks()
                    if reloading==True:
                        self.driver.level.player.reloadingTimer=nextshot+pygame.time.get_ticks()
            self.driver.level.player.shoot=False

class TestingState(DriverState):
    def __init__(self,driver):
        super(TestingState,self).__init__()
        self.driver=driver
        self.movables=[]
        for movable in self.driver.level.squad:
            self.movables.append(movable)

        self.spawning=True

    def catchEvents(self):

        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                or (event.key==K_d):
                    self.driver.level.player.move(event.key)
                if event.key==K_t:
                    self.driver.state=self.driver.clickToFire
                elif event.key==K_1:
                    self.driver.level.player.switchWeapons(guns.Pistol())
                elif event.key==K_2:
                    self.driver.level.player.switchWeapons(guns.Glock())
                elif event.key==K_3:
                    self.driver.level.player.switchWeapons(guns.Shotgun())
                elif event.key==K_4:
                    self.driver.level.player.switchWeapons(guns.AR15())
                elif event.key==K_5:
                    self.driver.level.player.switchWeapons(guns.Sniper())
                elif (event.key==K_q):
                    self.driver.level.player.swapWeapons()

                elif (event.key==K_k):
                    if pygame.key.get_mods() & KMOD_SHIFT and KMOD_CTRL:
                        for z in self.driver.level.activeHorde:
                            z.kill()
                        for z in self.driver.level.waitingHorde:
                            z.kill()

                elif event.key==K_ESCAPE:
                    sys.exit()

                elif event.key==K_RETURN:
                    #NEEDS A SAFETY SO CAN'T START ON ACCIDENT
                    pass

            elif event.type==KEYUP:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                or (event.key==K_d):
                    self.driver.level.player.stop(event.key)

            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1:
                    if self.movingMovable!=False:
                        for actor in self.movables:
                            if self.movingMovable==actor:
                                if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                    if not pygame.key.get_mods() & KMOD_SHIFT:
                                        actor.moveTo(pygame.mouse.get_pos())
                                        self.movingMovable=False
                                    else:
                                        actor.moveTo(pygame.mouse.get_pos(),True)


                                elif actor.rect.collidepoint(pygame.mouse.get_pos()):

                                    self.movingMovable=False
                    else:
                        for actor in self.movables:
                            if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                pass
                            else:
                                if not pygame.key.get_mods() & KMOD_CTRL:
                                    self.movingMovable=actor
                                else:
                                    if isinstance(actor,classes.Squad):
                                        actor.swapWeapons()
            elif event.type==pygame.QUIT:
                sys.exit()
        if pygame.mouse.get_pressed()==(0,0,1):
            self.movingMovable=False
            if (pygame.time.get_ticks()-self.driver.level.player.nextAttack>self.driver.level.player.lastAttack) and pygame.time.get_ticks()>self.driver.level.player.lastAttack:
                self.driver.level.player.shoot=True
                if self.driver.level.player.shoot==True:
                    (reloading,nextshot,projectiles) = self.driver.level.player.attack(pygame.mouse.get_pos())
                    for proj in projectiles:
                        self.driver.level.allSprites.add(proj)
                        self.driver.level.npcSprites.add(proj)
                        self.driver.level.layer2.add(proj)
                    self.driver.level.player.nextAttack=nextshot
                    self.driver.level.player.lastAttack=pygame.time.get_ticks()
                    if reloading==True:
                        self.driver.level.player.reloadingTimer=nextshot+pygame.time.get_ticks()
            self.driver.level.player.shoot=False

class DemoState(DriverState):
    def __init__(self,driver):
        super(DemoState,self).__init__()
        self.driver=driver
        self.movables=[]
        for movable in self.driver.level.squad:
            self.movables.append(movable)
        for movable in self.driver.level.inanimates:
            self.movables.append(movable)
        self.spawning=True

    def catchEvents(self):

        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                or (event.key==K_d):
                    self.driver.level.player.move(event.key)
                if event.key==K_t:
                    self.driver.state=self.driver.clickToFire
                elif event.key==K_1:
                    self.driver.level.player.switchWeapons(guns.Pistol())
                elif event.key==K_2:
                    self.driver.level.player.switchWeapons(guns.Glock())
                elif event.key==K_3:
                    self.driver.level.player.switchWeapons(guns.Shotgun())
                elif event.key==K_4:
                    self.driver.level.player.switchWeapons(guns.AR15())
                elif event.key==K_5:
                    self.driver.level.player.switchWeapons(guns.Sniper())
                elif (event.key==K_q):
                    self.driver.level.player.swapWeapons()

                elif event.key==K_ESCAPE:
                    sys.exit()

                elif event.key==K_RETURN:
                    #NEEDS A SAFETY SO CAN'T START ON ACCIDENT
                    pass

            elif event.type==KEYUP:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                or (event.key==K_d):
                    self.driver.level.player.stop(event.key)

            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1:
                    (mx,my) = pygame.mouse.get_pos()
                    if self.movingMovable!=False:
                        for actor in self.movables:
                            if self.movingMovable==actor:
                                if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                    if not pygame.key.get_mods() & KMOD_SHIFT:
                                        actor.moveTo(pygame.mouse.get_pos())
                                        self.movingMovable=False
                                    else:
                                        actor.moveTo(pygame.mouse.get_pos(),True)


                                elif actor.rect.collidepoint(pygame.mouse.get_pos()):

                                    self.movingMovable=False

                        for spawnPoint in self.driver.level.itemSpawns:
                            if spawnPoint.spawning==True and self.movingMovable==spawnPoint:

                                if not spawnPoint.item=='bucketOfWater':
                                    self.driver.level.addInanimate(spawnPoint.spawnItem((((mx//40)*40)+20,((my//40)*40)+20)))
                                    #self.driver.level.dirtyRect=self.driver.level.dirtyRect.union(spawnPoint.rect)

                                    spawnPoint.spawning=False
                                    self.movingMovable=False
                                else:
                                    #if you are spawning a bucket of water
                                    color=self.driver.level.graphicsHandeler.screen.get_at((mx,my))
                                    if color==(0,127,0):
                                        self.driver.level.addInanimate(spawnPoint.spawnItem((((mx//40)*40)+20,((my//40)*40)+20)))
                                        self.driver.level.dirtyRect=self.driver.level.dirtyRect.union(spawnPoint.rect)
                                        self.driver.level.dirtyRect=self.driver.level.dirtyRect.union(spawnPoint.amountRect)
                                        self.driver.level.dirtyRect=self.driver.level.dirtyRect.union(spawnPoint.rect)
                                        self.movingMovable=False
                                        spawnPoint.spawning=False
                                    else:
                                        #give invalid placement warning
                                        pass
                        for item in self.driver.level.inanimates:
                            if self.movingMovable==item:
                                if item.rect.collidepoint((mx,my)):
                                    self.movingMovable=False
                                else:
                                    if not isinstance(item,classes.BucketOfWater):
                                        item.moveTo((mx,my))
                                        self.movingMovable=False
                                    else:
                                        color=self.driver.level.graphicsHandeler.screen.get_at((mx,my))
                                        if color==(0,127,0):
                                            item.moveTo((mx,my))
                                            self.movingMovable=False
                                        else:
                                            #Cannot place item here
                                            pass


                    else:
                        for actor in self.movables:
                            if not actor.rect.collidepoint(pygame.mouse.get_pos()):
                                pass
                            else:
                                if not pygame.key.get_mods() & KMOD_CTRL:
                                    self.movingMovable=actor
                                else:
                                    if isinstance(actor,classes.Squad):
                                        actor.swapWeapons()

                        for spawnPoint in self.driver.level.itemSpawns:
                            if spawnPoint.rect.collidepoint(pygame.mouse.get_pos()):
                                if spawnPoint.amount!=0:
                                    spawnPoint.spawning=True
                                    self.movingMovable=spawnPoint

                        for item in self.driver.level.inanimates:
                            if not item.rect.collidepoint(pygame.mouse.get_pos()):
                                pass
                            else:
                                self.movingMovable=item

                elif event.button==3:
                    for item in self.driver.level.inanimates:
                        if item.rect.collidepoint(pygame.mouse.get_pos()):
                            if isinstance(item,classes.Inanimate):
                                item.rotate()
                        else:
                            self.movingMovable=False

            elif event.type==pygame.QUIT:
                sys.exit()
        if pygame.mouse.get_pressed()==(0,0,1):
            self.movingMovable=False
            if (pygame.time.get_ticks()-self.driver.level.player.nextAttack>self.driver.level.player.lastAttack) and pygame.time.get_ticks()>self.driver.level.player.lastAttack:
                self.driver.level.player.shoot=True
                if self.driver.level.player.shoot==True:
                    (reloading,nextshot,projectiles) = self.driver.level.player.attack(pygame.mouse.get_pos())
                    for proj in projectiles:
                        self.driver.level.allSprites.add(proj)
                        self.driver.level.npcSprites.add(proj)
                        self.driver.level.layer2.add(proj)
                    self.driver.level.player.nextAttack=nextshot
                    self.driver.level.player.lastAttack=pygame.time.get_ticks()
                    if reloading==True:
                        self.driver.level.player.reloadingTimer=nextshot+pygame.time.get_ticks()
            self.driver.level.player.shoot=False