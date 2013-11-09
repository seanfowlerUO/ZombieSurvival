'''
Created on Oct 19, 2013
@author: Sean Fowler
'''
import pygame,math,random,guns
from vector import Vector
from squad import Squad
from globals import *

MOVE_KEY_DICT=dict({119:'up',97:'left',115:'down',100:'right','ALL':'ALL','RIGHT':'right','LEFT':'left','UP':'up','DOWN':'down','left':'left','right':'right','up':'up','down':'down'})

class Observer(pygame.sprite.DirtySprite):
    '''
    Observer and Observable class in one. This is specifically an abstract class and should never be instantiated.
    ''' 
    def __init__(self,img,loc):
        super(Observer,self).__init__()
        self.observing=[]
        self.observers=[]

    def observe(self,o):
        self.observing.append(o)

    def __del__(self):
        #Special deletion function which makes sure no other objects are referencing the deleted object
        for o in self.observers:
            if self in o.observing:
                o.observing.remove(self)
            if o.target==self:
                o.target=None
                o.vector=None

        for o in self.observing:
            if self in o.observers:
                o.observers.remove(self)

    def addObservers(self,olist):
        if type(olist)!=type([]):
            olist=[olist]  #allows addition of a single observer
        for o in olist:
            if o in self.observers:
                pass
            else:
                self.observers.append(o)
                o.observe(self)

    def notifyObservers(self):
        #Reroutes all observers to the observed object. By telling the observer to .considerVector(self.vector) you tell them to move along
        #A vector relative to the observable
        for o in self.observers:
            o.considerVector(Vector((self.rect.centerx,self.rect.centery)))
            
    def considerVector(self,vec):
        pass
            
class Animate(Observer):
    def __init__(self,img,loc):
        super(Animate,self).__init__(img,loc)
        self.image = img
        self.rect = img.get_rect(center=loc)
        self.rawX = loc[0]
        self.rawY = loc[1]
        self.target = None
        
        #Movement
        self.speed = 5
        self.diagSpeed=int(math.floor((self.speed)/math.sqrt(2)))
        self.movingUp   =  False
        self.movingDown =  False
        self.movingRight=  False
        self.movingLeft =  False
        self.moving     =  False
        
        #Attack
        self.nextAttack = True
    
    def takeDamage(self,damage):
        pass
    
    def move(self):
        pass
    
    def stop(self,dir):
        pass
    
    def update(self):
        pass
    
    def attack(self, target = None):
        if target == None:
            target = self.target
        if target != None: #Make sure human has a target
            shooter = self.rect.center
            if type(target)!=type(tuple()): #if target is not a tuple, it's a sprite
                target = target.rect.center
            (nextShot , projectiles) = self.weapon.fire(shooter,target) # returns (rateOfFire , [projectiles]) all projectiles should be appended to the gameWorld's groups
            self.nextAttack = pygame.time.get_ticks() + nextShot
            return projectiles
        return
        

class Player(Animate):   
    def __init__(self,img,loc):
        super(Player,self).__init__(img,loc)
        self.squad = Squad(self)
        
        #Attacking
        self.weapon = guns.AR15()
        
        #Attributes
        self.leadership = 1
    
    def notifyObservers(self):
        #Sends a vector modified by your leadership to observers
        for o in self.observers:
            o.considerVector(Vector((self.rect.centerx,self.rect.centery)))      
    
    def move(self,key):
        #Standard key movement allowing diagonal movement
        global MOVE_KEY_DICT
        direction =MOVE_KEY_DICT[key]

        if direction=='up':
            self.movingUp=True
            self.movingDown=False
        if direction=='down':
            self.movingDown=True
            self.movingUp=False
        if direction=='left':
            self.movingLeft=True
            self.movingRight=False
        if direction=='right':
            self.movingRight=True
            self.movingLeft=False
        self.notifyObservers()

    def stop(self,key):
        #Called when user lets go of key
        direction=MOVE_KEY_DICT[key]

        if direction=='up':
            self.movingUp=False
        if direction=='down':
            self.movingDown=False
        if direction=='left':
            self.movingLeft=False
        if direction=='right':
            self.movingRight=False
        if direction=='ALL':
            self.movingUp=False
            self.movingDown=False
            self.movingLeft=False
            self.movingRight=False

    def update(self):
        if self.movingUp:
            self.moving=True
            if self.movingRight:
                self.rect.move_ip(self.diagSpeed,-self.diagSpeed)
            elif self.movingLeft:
                self.rect.move_ip(-self.diagSpeed,-self.diagSpeed)
            else:
                self.rect.move_ip(0,-self.speed)

        elif self.movingDown:
            self.moving=True
            if self.movingRight:
                self.rect.move_ip(self.diagSpeed,self.diagSpeed)
            elif self.movingLeft:
                self.rect.move_ip(-self.diagSpeed,self.diagSpeed)
            else:
                self.rect.move_ip(0,self.speed)

        elif self.movingRight:
            self.moving=True
            self.rect.move_ip(self.speed,0)

        elif self.movingLeft:
            self.moving=True
            self.rect.move_ip(-self.speed,0)
        else:
            self.moving=False
            self.rect.move_ip(0,0)
        self.notifyObservers()

        ''' def evalStops(self,(left,right,down,up)):
        #Checks whether or not player is being stopped by outside source (not player)
        if left:
            self.stop('LEFT')
        if right:
            self.stop('RIGHT')
        if up:
            self.stop('UP')
        if down:
            self.stop('DOWN')'''

     
class NPC(Animate):   
    def __init__(self,img,loc):
        super(NPC,self).__init__(img,loc)
        self.vector=None
        self.nextMove=self.rect.copy()
    
    def addVector(self,vec):
        self.vector = vec

    def move(self):

        if self.vector==None:
            self.moving=False
            pass
        else:
            self.moving=True
            currLoc=Vector(self.rect.center)
            desiredLoc=self.vector
            direction=currLoc-desiredLoc
            (normalx,normaly) = direction.getNormal()
            xcomp=-normalx*self.speed
            ycomp=-normaly*self.speed
            if abs(xcomp)>abs(self.vector.x-self.rect.centerx):
                xcomp=self.vector.x-self.rect.centerx
            if abs(ycomp)>abs(self.vector.y-self.rect.centery):
                ycomp=self.vector.y-self.rect.centery
            self.rawX+=xcomp
            self.rawY+=ycomp
            self.nextMove.move_ip(xcomp,ycomp)
            if (direction.x, direction.y) ==(0,0):
                self.vector=None
        self.notifyObservers()
        
    def stop(self,direction):
        if direction=="left":
            if self.nextMove.centerx < self.rect.centerx:
                self.nextMove.centerx = self.rect.centerx
        elif direction=="right":
            if self.nextMove.centerx > self.rect.centerx:
                self.nextMove.centerx = self.rect.centerx
        elif direction=="up":
            if self.nextMove.centery < self.rect.centery:
                self.nextMove.centery = self.rect.centery
        elif direction=="down":
            if self.nextMove.centery > self.rect.centery:
                self.nextMove.centery = self.rect.centery                

    def update(self):
        self.rect.center=self.nextMove.center
   
class Human(NPC):
    def __init__(self,img,loc):
        super(Human,self).__init__(img,loc)
        self.placeInFormation = Vector((0,0))
        
        #Attacking
        self.weapon=guns.AR15()
        self.radius=self.weapon.range
        self.aiming=False
                
        #Attributes
        self.tactics = 1

    
    def considerVector(self,vec):
        self.vector = vec + self.placeInFormation
        
    def setPlace(self, place):
        xoff = random.randrange(-20,20)/self.tactics
        yoff = random.randrange(-20,20)/self.tactics        
        self.placeInFormation = Vector(place) + Vector((xoff,yoff))
        
    def reload(self):
        self.weapon.reload()
            
            
        
class Zombie(NPC):   
    def __init__(self,img,loc):
        super(Zombie,self).__init__(img,loc)
        
        #Attacking
        self.weapon=guns.ZombieHands()
        self.damage=self.weapon.damage
        self.target=None
                    
        #Stats
        self.health =10
        self.speed  =4
        
    def takeDamage(self,damage):
        self.health-=damage
        if self.health<=0:
            self.kill()
    def considerVector(self,vec):
        self.vector = vec
        
    def setTarget(self,targ):
        self.observe(targ)
        targ.addObservers(self)
        self.target = targ
        
    def attack(self,target):
        #only called when zombie can attack something
        target.takeDamage(self.damage)
              
#NEEDS TO BE REWRITTEN/CLEANED UP
class Inanimate(pygame.sprite.DirtySprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.placed=False
        self.critical=False
        self.vertical=True

    def swapImage(self,image):
        spawn=self.rect.center
        self.image=pygame.image.load(image)
        self.rect=self.image.get_rect(center=spawn)

    def rotate(self):
        imgRot=pygame.transform.rotate(self.image,90)
        imgRotRect=imgRot.get_rect(center=self.rect.center)
        self.image=imgRot
        self.rect=imgRotRect
        self.vertical=not self.vertical

    def moveTo(self,(x,y)):
        self.rect.center=(((x//40)*40)+20,((y//40)*40)+20)
        
class ScreenEdge(Inanimate):
    def __init__(self,side):
        super(ScreenEdge,self).__init__()
        self.edge = side
        if side==("left"):
            self.image=pygame.image.load("images/verticalEdge.png")
            self.rect =self.image.get_rect()
            self.rect.left , self.rect.top = 0 , 0
        elif side==("right"):
            self.image=pygame.image.load("images/verticalEdge.png")
            self.rect =self.image.get_rect()
            self.rect.right , self.rect.top = WIDTH , 0
        elif side==("up"):
            self.image=pygame.image.load("images/horizontalEdge.png")
            self.rect =self.image.get_rect()
            self.rect.left , self.rect.top = 0 , 0
        elif side==("down"):
            self.image=pygame.image.load("images/horizontalEdge.png")
            self.rect =self.image.get_rect()
            self.rect.left , self.rect.bottom = 0 , HEIGHT           
        
class Projectile(Inanimate):
    def __init__(self,spawn,RelVector,gun):

        self.speed=25
        self.image=pygame.image.load('images/projectile2.png')
        self.rect=self.image.get_rect(center=spawn)
        self.gun=gun
        self.damage=self.gun.damage
        self.pierce=self.gun.pierce

        self.vector=RelVector
        self.vector.scale(self.speed)

        self.origx=self.vector.x-spawn[0]
        self.origy=self.vector.y-spawn[1]
        #self.image=pygame.transform.rotate(self.image,math.degrees(math.atan2(self.vector.getNormal()[0],self.vector.getNormal()[1])))
        self.rawX=self.rect.centerx
        self.rawY=self.rect.centery
        self.nextMove=self.rect
        self.health=1
        super(Projectile,self).__init__()

    def move(self):
        #vector is scaled on initialization
        xcomp=self.vector.x
        ycomp=self.vector.y
        self.rawX+=xcomp
        self.rawY+=ycomp
        self.nextMove.move_ip(xcomp,ycomp)

    def update(self):
        self.rect=self.nextMove
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        