__author__ = 'Sean Fowler'
import classes,pygame.mixer,random,relVector
from globals import *
class Guns(object):
    #interface
    def __init__(self):
        pygame.mixer.init()
        self.ammo=None
        self.magazine=None
        self.pierce = 1 #How many sprites the bullet can hit
        #reload needs to be an int
        self.reloadTime=0
        self.rateOfFire=0
        self.accuracy=0 #accuracy is how many pixels are in the +- target range so 0 is perfect accuracy. NOTE: Accuracy is also dependent on range so a shotgun could have the same accuracy as a pistol, but the different range changes the projectiles behavior
        self.sound=None
        
    def reload(self):
        pass

    def fire(self,shooterTup,targetTup): # the rects of the trigger puller and target
        projectiles = []
        for projectile in range(self.projectileTup[1]):
            diffx = random.randrange(-self.accuracy,self.accuracy)
            diffy = random.randrange(-self.accuracy,self.accuracy)
            dist  = distance(shooterTup,targetTup)
            
            missx=((diffx*dist)/self.range)
            missy=((diffy*dist)/self.range)
            projectiles.append(self.projectileTup[0](shooterTup,relVector.RelVector(shooterTup,(targetTup[0]+missx,targetTup[1]+missy)),self))            
        return (self.rateOfFire, projectiles)


class HandToHand(Guns):
    def __init__(self):
        Guns.__init__(self)
        self.damage=1
        self.range=50
        self.rateOfFire=500
        self.name='handToHand'
        self.image='../images/'+self.name+'.png'
        self.magazine=1
        self.reloadTime=10
        self.ammo=self.magazine
        self.loadType='single'
        self.projectileTup=(classes.Projectile,1) # MAY need to be fixed

class ZombieHands(Guns):
    def __init__(self):
        Guns.__init__(self)
        self.damage=1
        #FOR ZOMBIES RANGE IS ONLY USED IN ITEM DESTRUCTION
        self.range=42
        self.rateOfFire=500
        self.name='zombieHands'
        self.image=''

class ZombieMouth(Guns):
    def __init__(self):
        Guns.__init__(self)
        self.damage=2
        #FOR ZOMBIES RANGE IS ONLY USED IN ITEM DESTRUCTION
        self.range=42
        self.rateOfFire=500
        self.name='zombieMouth'
        self.image=''

class AR15(Guns):
    def __init__(self):
        Guns.__init__(self)
        self.damage=3
        self.range=200
        self.rateOfFire=200
        #name is used for image purposes mostly
        self.name='rifle'
        self.image='../images/'+self.name+'.png'
        self.magazine=10
        self.reloadTime=2000
        self.ammo=self.magazine
        self.loadType='mag'
        self.projectileTup=(classes.Projectile,1)
        self.accuracy=12
        self.sound=pygame.mixer.Sound('../sounds/AR15.wav')

class Pistol(Guns):
    def __init__(self):
        Guns.__init__(self)
        self.damage=2
        self.range=100
        self.rateOfFire=400
        self.name='pistol'
        self.image='../images/'+self.name+'.png'
        self.magazine=6
        self.reloadTime=600
        self.ammo=self.magazine
        self.loadType='single'
        self.projectileTup=(classes.Projectile,1)
        self.accuracy=15
        self.sound=pygame.mixer.Sound('../sounds/pistol.wav')

class Glock(Guns):
    def __init__(self):
        Guns.__init__(self)
        self.damage=1
        self.range=100
        self.rateOfFire=300
        self.name='glock'
        self.image='../images/'+self.name+'.png'
        self.magazine=17
        self.reloadTime=700
        self.ammo=self.magazine
        self.loadType='mag'
        self.projectileTup=(classes.Projectile,1)
        self.accuracy=10
        self.sound=pygame.mixer.Sound('../sounds/glock.wav')

class Shotgun(Guns):
    def __init__(self):
        Guns.__init__(self)
        self.damage=2 #*7 Projectiles
        self.range=75
        self.rateOfFire=800
        self.name='shotgun'
        self.image='../images/'+self.name+'.png'
        self.magazine=6
        self.reloadTime=850
        self.ammo=self.magazine
        self.loadType='single'
        self.projectileTup=(classes.Projectile,7)
        self.accuracy=15
        self.sound=pygame.mixer.Sound('../sounds/shotgun.wav')


class Sniper(Guns):
    def __init__(self):
        Guns.__init__(self)
        self.damage=8
        self.range=350
        self.rateOfFire=1500
        self.name='sniper'
        self.image='../images/'+self.name+'.png'
        self.magazine=5
        self.reloadTime=2000
        self.ammo=self.magazine
        self.loadType='mag'
        self.projectileTup=(classes.Projectile,1)
        self.accuracy=2
        self.sound=pygame.mixer.Sound('../sounds/sniper.wav')