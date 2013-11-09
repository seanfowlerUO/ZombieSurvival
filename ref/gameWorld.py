__author__ = 'Sean Fowler'
import pygame,classes,vector,globals
class GameWorld(object):
    def __init__(self,level):
        super(GameWorld,self).__init__()
        self.level=level

    def spawn(self):

        if len(self.level.waitingHorde)>0 and self.level.driver.state.spawning==True:

            if (pygame.time.get_ticks()-self.level.spawnInterval>self.level.driver.lastSpawn) and pygame.time.get_ticks()>self.level.driver.lastSpawn:
                self.level.driver.lastSpawn=pygame.time.get_ticks()
                zed=self.level.waitingHorde.sprites()[0]

                self.level.waitingHorde.remove(zed)

                self.level.activeHorde.add(zed)
                self.level.npcSprites.add(zed)
                self.level.animates.add(zed)
                self.level.allSprites.add(zed)
                self.level.layer2.add(zed)#NEED TO FIND A BETTER SYSTEM


    def move(self):
        #self.level.dirtyRect=self.level.dirtyRect.union(self.level.player.rangeHaloUnderlay.rect)
        self.level.dirtyRect=self.level.dirtyRect.union(self.level.player.rect)
        #self.level.dirtyRect=self.level.dirtyRect.union(self.level.mapRect.clip(self.level.player.rangeHaloUnderlay.rect))

        for sprite in self.level.npcSprites: # all sprites but player, since player's move is controlled in Driver.state.catchEvents
            self.level.dirtyRect=self.level.dirtyRect.union(sprite.rect)
            self.level.dirtyRect=self.level.dirtyRect.union(self.level.mapRect.clip(sprite.rect))
            #if isinstance(sprite,classes.Squad):
                #self.level.dirtyRect=self.level.dirtyRect.union(sprite.rangeHaloUnderlay.rect)
                #self.level.dirtyRect=self.level.dirtyRect.union(self.level.mapRect.clip(sprite.rangeHaloUnderlay.rect))
            sprite.move()

    def checkCollisions(self):
        #Zombie Collisions AND attacks
        for zombie in self.level.activeHorde:
            for sprite in self.level.allSprites:
                if zombie.rect.colliderect(sprite.rect):
                    zombie.visit(sprite)
                    if isinstance(sprite,classes.Human):
                        self.level.dirtyRect=self.level.dirtyRect.union(sprite.lifeBar.rect)
        for h in self.level.activeHumans:
            for i in self.level.inanimates:
                if isinstance(i,classes.BucketOfWater):
                    if h.rect.colliderect(i.rect):
                        if h.hitbox.colliderect(i.rect):
                            h.statusState=h.slowedState
                        else:
                            h.statusState=h.normalState



    def attack(self):
        for human in self.level.squad:
            for zombie in self.level.activeHorde:
                if human.aiming==False:
                    if human.inRange(zombie):
                        human.aiming=zombie

            if (pygame.time.get_ticks()-human.nextAttack>human.lastAttack) and pygame.time.get_ticks()>human.lastAttack:
                human.shoot=True

            if human.aiming!=False:
                #human.aiming will return the zombie sprite at which it is aiming
                zombie=human.aiming
                if human.inRange(zombie):
                    if zombie not in self.level.activeHorde:
                        human.aiming=False
                    if human.shoot==True:
                        #pygame.draw.line(self.level.graphicsHandeler.screen,(255,255,255),human.rect.center,zombie.rect.center)


                        # human.weapon.fire returns ROF if reload is not needed and reloadTime+ROF (and reloads) if reload is needed
                        (reloading,nextshot,projectiles) = human.attack(zombie.rect.center)
                        for proj in projectiles:
                            self.level.allSprites.add(proj)
                            self.level.npcSprites.add(proj)
                            self.level.layer2.add(proj)
                        human.nextAttack=nextshot
                        human.lastAttack=pygame.time.get_ticks()
                        if reloading==True:
                            human.reloadingTimer=nextshot+pygame.time.get_ticks()
                    else:
                        pass

                else:
                    human.aiming=False


            human.shoot=False

    def checkStatus(self):
        for sprite in self.level.allSprites:
            if sprite.health<=0:

                if sprite.critical==True:
                    self.level.driver.state=self.level.driver.gameOverState
                if isinstance(sprite,classes.Human):
                    self.level.dirtyRect=self.level.dirtyRect.union(sprite.lifeBar.rect)
                try:
                    sprite.dieSound.play()
                except:
                    pass
                sprite.kill()
            if globals.isInPlay((sprite.rect.center))!=True:


                if isinstance(sprite,classes.Squad):
                    sprite.nextMove=sprite.rect
                    sprite.vector=None
                elif isinstance(sprite,classes.Projectile):
                    sprite.vector=None
                    sprite.kill()
                elif isinstance(sprite,classes.Inanimate):
                    pass
                else:
                    sprite.evalStops(globals.isInPlay(sprite.rect.center))

            if isinstance(sprite,classes.Zombie):
                if sprite.rect.center==(self.level.map.goal):
                    self.level.driver.state=self.level.driver.gameOverState

        if len(self.level.waitingHorde)==0 and len(self.level.activeHorde)==0:
            if not self.level.driver.state==self.level.driver.testingState:

                self.level.driver.state=self.level.driver.completeState

    def update(self):
        for actor in self.level.animates:
            actor.update()
            self.level.dirtyRect=self.level.dirtyRect.union(actor.rect)
            if isinstance(actor,classes.Human):
                self.level.dirtyRect=self.level.dirtyRect.union(actor.rangeHaloUnderlay.rect)


