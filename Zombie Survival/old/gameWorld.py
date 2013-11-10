import pygame,random
from classes import *
from globals import *

class CustomGroup(pygame.sprite.RenderUpdates):
    #Basically a custom shell that allows subclassing which simplifies the pygame.sprite.Group.add(*args) method
    def __init__(self):
        self.superGroups=[]
        super(CustomGroup,self).__init__()
    
    def add(self,*sprite):
        super(CustomGroup,self).add(*sprite)
        for superGroup in self.superGroups:
            superGroup.add(*sprite)
    
    def addSubGroup(self,customSubGroup):
        customSubGroup.superGroups.append(self)
    
    def addSuperGroup(self,customSuperGroup):
        self.superGroups.append(customSuperGroup)

class GameWorld(object):
    #Game world should consist of methods which monitor and progress most things in the game.
    #These methods will be called as threads in the driver function along with necessary graphics. NOTE: GameWorld should not control ANY graphics   
    def __init__(self):
        super(GameWorld,self).__init__()
        
        self.nextSpawn=True
        self.timeBetweenSpawns=1000
        
        self.allSprites = CustomGroup()
        self.animates = CustomGroup() #Super of activeHorde and activeHumans
        self.activeHorde=CustomGroup()
        self.activeHumans=CustomGroup()
        self.animates.addSubGroup(self.activeHorde)
        self.animates.addSubGroup(self.activeHumans)
        self.allSprites.addSubGroup(self.animates)
        
        self.projectiles = CustomGroup()
        self.allSprites.addSubGroup(self.projectiles)
            
        self.screenEdges = CustomGroup()
        self.screenEdges.add(ScreenEdge("left"))
        self.screenEdges.add(ScreenEdge("right"))
        self.screenEdges.add(ScreenEdge("up"))
        self.screenEdges.add(ScreenEdge("down"))
        
        ############################FIXME##########################
        #Background should not be static. Probably be in map.py
        self.backgroundGroup = CustomGroup()
        self.background = pygame.sprite.DirtySprite()
        self.background.image = pygame.image.load("images/bg.png")
        self.background.rect = self.background.image.get_rect()
        ###########################################################
        
        self.player = Player(pygame.image.load("images/humans/squad1_rifle.png"),(500,500)) #FIXME. Player shouldn't be static
        self.squad  = self.player.squad
        self.animates.add(self.player)
        self.spawnPoints = [(-20,-20),(WIDTH/2,-20),(WIDTH+20,+20)]
        
    def spawn(self):
        if self.nextSpawn <= pygame.time.get_ticks() or self.nextSpawn==True:
            target  = random.randrange(len(self.player.squad))
            picture = random.randrange(1,6) # number of different zombie pictures available
            spawn   = random.randrange(len(self.spawnPoints))
            zed     = Zombie(pygame.image.load("images/zombies/zombie"+str(picture)+".png"),self.spawnPoints[spawn])
            zed.setTarget(self.player.squad.members[target])
            self.activeHorde.add(zed)
            self.nextSpawn = pygame.time.get_ticks() + self.timeBetweenSpawns
            
    def move(self):
        for hum in self.activeHumans:
            hum.move()
        for zed in self.activeHorde:
            zed.move()
        for pro in self.projectiles:
            pro.move()
        
    def checkCollisions(self):
        projectileHits = pygame.sprite.groupcollide(self.activeHorde,self.projectiles,0,0) # Returns dict with all collisions in form {animateSprite : [*projectileSprites]} | FF=OFF
        zombieHits     = pygame.sprite.groupcollide(self.activeHumans,self.activeHorde,0,0) 
        humanScreenHits= pygame.sprite.groupcollide(self.screenEdges,self.activeHumans,0,0)
        playerScreenHits = pygame.sprite.spritecollide(self.player,self.screenEdges,0)
        
        for victim in projectileHits:
            for projectile in projectileHits[victim]: # all of the projectils which hit a victim
                damage = projectile.damage
                victim.takeDamage(damage)
                projectile.pierce-=1
                if projectile.pierce==0: #Remove projectile if has no more pierces (allows for one bullet to hit multiple tagets (assuming the guns peirce rating is high enough)
                    projectile.kill() 
        
        for victim in zombieHits:
            for zombie in zombieHits[victim]: #all of the zombies which hit a victim
                if zombie.nextAttack <= pygame.time.get_ticks() or zombie.nextAttack==True: #Only calls attack when human can attack
                    zombie.attack(victim)
        
        for screenSprite in humanScreenHits:
            #print str(screenSprite) + ":" + str(humanScreenHits[screenSprite])
            for human in humanScreenHits[screenSprite]: #all of the humans hitting the given screen
                human.stop(screenSprite.edge)
                
        for human in self.activeHumans:  #checking if zombies are in range of human and taking closest zombie
            if human.nextAttack <= pygame.time.get_ticks() or human.nextAttack==True: #check if human can attack before iterating through all of the activeHorde
                shortest = None
                for zed in self.activeHorde:
                    r = inRange(human.rect.center,zed.rect.center,human.weapon.range) 
                    if r:
                        if shortest == None:
                            shortest = zed
                        else:
                            if r<shortest:
                                shortest = zed
                human.target = shortest
        
        for hits in playerScreenHits:
            self.player.stop(hits.edge)
                            
        # NOTE: This allows further implementation to add a scrolling map! By making sprites in the areas which cause scrolling we can scroll map on impact
    
    def update(self):
        self.allSprites.update()
    
    def attack(self):
        #Used for all non-impact attacks
        for human in self.activeHumans:
            att = human.attack()
            if att!=None:
                self.projectiles.add(att) #human.attack returns a list of new projectiles to be added to gameWorld
            human.target=None
    
    
    