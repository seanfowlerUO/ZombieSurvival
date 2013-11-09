__author__ = 'Sean Fowler'
import pygame, guns, globals,random,relVector
from helpers import *
import functions
from mapper import *
from pygame.locals import *
from vector import *
from visitor import *
import states

########################################################################################################################
#IMAGES


HALOS = dict({100:'../images/halo_100.png' ,150:'../images/halo_150.png', 200:'../images/halo_200.png',400:'../images/halo_400.png',700:'../images/halo_700.png'})
MOVE_KEY_DICT=dict({119:'up',97:'left',115:'down',100:'right','ALL':'ALL','RIGHT':'right','LEFT':'left','UP':'up','DOWN':'down'})

class Animate(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.killCount=0
        self.health=20
        self.nextAttack=0
        self.reloading=False
        pygame.font.init()
        font=pygame.font.Font('freesansbold.ttf',15)
        reloadTxt=font.render('Reloading...',1,(255,0,0))
        self.reloadingImage=reloadTxt
        self.reloadingRect=reloadTxt.get_rect(center=(self.rect.centerx,self.rect.centery+30))
        self.cursorImage=pygame.image.load('../images/moveTo.png')
        self.cursorRect=self.cursorImage.get_rect()
        self.nextMove=None
        self.critical=False


    def inRange(self,other):
        if (distance(self.rect.center,other.rect.center)<self.primaryWeapon.range):
            return True
        return False

    def swapWeapons(self):
        temp=self.primaryWeapon
        self.primaryWeapon=self.secondaryWeapon
        self.secondaryWeapon=temp
        self.image=functions.loadImage('../images/%s' %self.type + '_%s' %self.primaryWeapon.name +'.png' )
        self.rangeHaloImage = functions.loadImage(HALOS[self.primaryWeapon.range*2])
        self.rangeHaloRect  = pygame.rect.Rect(self.rect.center,(self.primaryWeapon.range*2,self.primaryWeapon.range*2))

    def attack(self,target):
        reloadBool ,fireTime, projectileTup= self.primaryWeapon.fire()
        projectiles=[]
        if reloadBool==1:
            self.reloading=True
            self.reloadingRect.center=self.rect.center
        else:
            self.reloading=False
        if self.moving==True:
            (reloadBool,fireTime) =(reloadBool,int(fireTime*(3/2)))

        for x in range(projectileTup[1]):
            diffx=random.randrange(self.primaryWeapon.accuracy)
            diffy=random.randrange(self.primaryWeapon.accuracy)
            dirx=random.randrange(2)
            diry=random.randrange(2)
            if dirx==0:
                missx=-diffx
            else:
                missx=diffx
            if diry==0:
                missy=-diffy
            else:
                missy=diffy
            dist=distance((self.rect.centerx,self.rect.centery),target)
            missx=((missx*dist)/self.primaryWeapon.range)
            missy=((missy*dist)/self.primaryWeapon.range)
            


            projectiles.append(projectileTup[0](self.rect.center,relVector.RelVector((self.rect.centerx,self.rect.centery),(target[0]+missx,target[1]+missy)),self.primaryWeapon))

        return reloadBool,fireTime, projectiles

    def reload(self):
        self.reloading=True
        temp = self.primaryWeapon.reload()
        return temp

    def takeDamage(self,amount):
        self.health-=amount
        if isinstance(self,Human):
            if self.health>=0:
                self.lifeBar.image=pygame.image.load('../images/lifebar_%s' %self.health + '.png')
            else:
                self.lifeBar.image=pygame.image.load('../images/lifebar_0.png')






    def switchWeapons(self,weapon):


        self.primaryWeapon=weapon
        self.image=functions.loadImage('../images/%s' %self.type + '_%s' %self.primaryWeapon.name +'.png' )

        self.rangeHaloImage = pygame.image.load(HALOS[self.primaryWeapon.range*2])
        self.rangeHaloRect  = self.rangeHaloImage.get_rect(center=self.rect.center)
        self.rangeHaloUnderlay = Element(self.rangeHaloImage,self.rangeHaloRect,True)

class Zombie(Animate,ZombieVisitor):
    def __init__(self,spawn=(0,0),image=('../images/zombie1.png')):

        self.normalState=states.NormalState()
        self.slowedState=states.SlowedState()
        self.state=self.normalState





        self.type=image[10:17]
        self.image = pygame.image.load(image)
        self.rect =  self.image.get_rect()
        self.rect.center=spawn
        self.biteRect=self.image.get_rect(center=spawn, width=20, height=20)
        self.stackRect=self.image.get_rect(center=spawn, width=15, height=15)

        self.path=None
        self.pathSection=0
        self.sectionProgress=0
        self.speed=2
        self.diagSpeedRaw=((self.speed/math.sqrt(2)))
        self.diagSpeed=int(round(self.diagSpeedRaw))
        self.directionSpeed=self.speed
        self.canMove=True
        self.slowed=False
        self.moved=False

        self.moniter=False


        Animate.__init__(self)


        self.movingUp=False
        self.movingDown=False
        self.movingLeft=False
        self.movingRight=False
        self.distanceRemaining=CELL_SIZE-self.sectionProgress
        self.direction=''
        self.touchingCount=0



        self.health=10
        self.dieTime=None
        self.primaryWeapon=guns.ZombieMouth()
        self.secondaryWeapon=guns.ZombieHands()
        self.rateOfFire=self.primaryWeapon.rateOfFire
        self.canAttack=False
        self.lastAttack=0

        self.hitSound=pygame.mixer.Sound('../sounds/zed_hit.wav')
        self.dieSound=pygame.mixer.Sound('../sounds/zed_die.wav')
        self.lurkSound=None


    def changeState(self,newState):
        self.state=newState

    def hit(self,damage):
        self.health-=damage
        if self.health<4:
            self.image=pygame.image.load('../images/%s'%self.type+'_shot2.png')
            self.hitSound.play()
        elif self.health<8:
            self.image=pygame.image.load('../images/%s'%self.type+'_shot1.png')
            self.hitSound.play()
        else:
            pass

    def die(self,time,weapon='pistol'):
        print 'DIE SEQUENCE NOT COMPLETE FOR ALL ZOMBIES'

        if weapon=='shotgun':

            if self.dieTime==None:
                self.image=pygame.image.load('../images/zombie1_die_shotgun1.png')
                self.dieTime=time
            elif time-self.dieTime>150:
                return True
            elif time-self.dieTime>100:

                self.image=pygame.image.load('../images/zombie1_die_shotgun3.png')
            elif time-self.dieTime>50:

                #if has been dead for more than 50 miliseconds

                self.image=pygame.image.load('../images/zombie1_die_shotgun2.png')



        else:
            self.image=pygame.image.load('../images/zombie1_die1.png')
            if self.dieTime==None:
                self.dieTime=time
            elif time-self.dieTime>150:
                return True
            elif time-self.dieTime>100:

                self.image=pygame.image.load('../images/zombie1_die3.png')
            elif time-self.dieTime>50:

                #if has been dead for more than 300 miliseconds
                self.image=pygame.image.load('../images/zombie1_die2.png')
        return False


    def switchWeapons(self,weapon):
        '''hopefully zombies are never able to use guns...'''
        pass


    def move(self):
        self.direction=self.path[self.pathSection]

        if self.direction=='GOAL':
            #zombie has reached and is on top of the goal
            self.stop('all')
            self.sectionProgress=0
            self.directionSpeed=0

        if self.direction=='N':
            self.movingUp=True
            self.movingDown=False
            self.movingLeft=False
            self.movingRight=False
        elif self.direction=='S':
            self.movingDown=True
            self.movingUp=False
            self.movingLeft=False
            self.movingRight=False
        elif self.direction=='W':
            self.movingLeft=True
            self.movingRight=False
            self.movingUp=False
            self.movingDown=False
        elif self.direction=='E':
            self.movingRight=True
            self.movingLeft=False
            self.movingUp=False
            self.movingDown=False
        elif self.direction=='NE':
            self.movingUp=True
            self.movingDown=False
            self.movingRight=True
            self.movingLeft=False
        elif self.direction=='NW':
            self.movingUp=True
            self.movingDown=False
            self.movingLeft=True
            self.movingRight=False
        elif self.direction=='SE':
            self.movingDown=True
            self.movingUp=False
            self.movingRight=True
            self.movingLeft=False
        elif self.direction=='SW':
            self.movingDown=True
            self.movingUp=False
            self.movingLeft=True
            self.movingRight=False

    def update(self):
        #NOT READY FOR DIAGONAL MOVEMENT
        if self.state==self.normalState:
            speed=self.speed
        elif self.state==self.slowedState:
            speed=self.speed/2
        progress=False
        if self.distanceRemaining<speed:
            move=self.distanceRemaining
        else:
            move=speed
        if self.movingUp==True:
            self.rect.move_ip(0,-move)
            progress=True
        elif self.movingDown==True:
            self.rect.move_ip(0,move)
            progress=True
        elif self.movingRight==True:
            self.rect.move_ip(move,0)
            progress=True
        elif self.movingLeft==True:
            self.rect.move_ip(-move,0)
            progress=True
        if progress==True:
            self.distanceRemaining-=move
            if self.distanceRemaining==0:
                self.pathSection+=1
                self.sectionProgress=0
                self.distanceRemaining=CELL_SIZE
        self.biteRect.center=self.rect.center
        self.stackRect.center=self.rect.center

    def stop(self,direction):
        if direction=='N':
            self.movingUp=False
        if direction=='S':
            self.movingDown=False
        if direction=='W':
            self.movingLeft=False
        if direction=='E':
            self.movingRight=False
        if direction=='NE':
            self.movingUp=False
            self.movingRight=False
        if direction=='NW':
            self.movingUp=False
            self.movingLeft=False
        if direction=='SE':
            self.movingDown=False
            self.movingRight=False
        if direction=='SW':
            self.movingDown=False
            self.movingLeft=False
        if direction=='ALL':
            self.movingUp=False
            self.movingDown=False
            self.movingLeft=False
            self.movingRight=False

        if direction=='all':
            self.movingUp=False
            self.movingDown=False
            self.movingLeft=False
            self.movingRight=False




class Human(Animate):
    def __init__(self):
        super(Human,self).__init__()
        self.onTheMoveState=states.OnTheMove()
        self.stationaryState=states.Stationary()
        self.uprightState=states.Upright()
        self.crouchState=states.Crouch()
        self.proneState=states.Prone()
        self.slowedState=states.SlowedState()
        self.normalState=states.NormalState()

        self.movingState=self.onTheMoveState
        self.stanceState=self.uprightState
        self.statusState=self.normalState



    def changeState(self,type,newState):
        if type=='moving':
            self.movingState=newState
        else:
            self.stanceState=newState


class Player(Human):
    def __init__(self,image="../images/player_handToHand.png"):

        self.image=  functions.loadImage(image)
        self.rect =  self.image.get_rect()
        self.hitbox= self.image.get_rect(width=30,height=30)
        self.type='player'

        self.speed=10
        self.diagSpeed=int(round((self.speed)/math.sqrt(2)))
        self.slowed=False

        self.name=self.type
        self.lifeBarImage=pygame.image.load('../images/lifebar.png')
        self.lifeBarRect=self.lifeBarImage.get_rect(left=self.rect.left)
        self.lifeBar=Element(self.lifeBarImage,self.lifeBarRect,True)




        self.critical=True
        self.movingUp=False
        self.movingDown=False
        self.movingLeft=False
        self.movingRight=False
        self.aiming=False
        self.canAttack=False
        self.lastAttack=0
        self.moving=False

        self.primaryWeapon=guns.HandToHand()
        self.secondaryWeapon=guns.HandToHand()
        super(Player,self).__init__()
        #current setup needs a halo for each range distance but I am working on stretching halo images
        #range is half the halo
        self.rangeHaloImage = pygame.image.load(HALOS[self.primaryWeapon.range*2])
        self.rangeHaloRect  = self.rangeHaloImage.get_rect(center=self.rect.center)
        self.rangeHaloUnderlay = Element(self.rangeHaloImage,self.rangeHaloRect,True)
        self.critical=True
    #MOVEMENT

    #keycode dictionary

    def move(self,key):
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

    def stop(self,key):
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

    def evalStops(self,(left,right,down,up)):
        if left:
            self.stop('LEFT')
        if right:
            self.stop('RIGHT')
        if up:
            self.stop('UP')
        if down:
            self.stop('DOWN')

    def update(self):
        if self.movingUp:
            self.moving=True
            if self.movingRight:
                self.rect.move_ip(self.diagSpeed*self.statusState.speedModifier,-self.diagSpeed*self.statusState.speedModifier)
            elif self.movingLeft:
                self.rect.move_ip(-self.diagSpeed*self.statusState.speedModifier,-self.diagSpeed*self.statusState.speedModifier)
            else:
                self.rect.move_ip(0,-self.speed*self.statusState.speedModifier)

        elif self.movingDown:
            self.moving=True
            if self.movingRight:
                self.rect.move_ip(self.diagSpeed*self.statusState.speedModifier,self.diagSpeed*self.statusState.speedModifier)
            elif self.movingLeft:
                self.rect.move_ip(-self.diagSpeed*self.statusState.speedModifier,self.diagSpeed*self.statusState.speedModifier)
            else:
                self.rect.move_ip(0,self.speed*self.statusState.speedModifier)

        elif self.movingRight:
            self.moving=True
            self.rect.move_ip(self.speed*self.statusState.speedModifier,0)

        elif self.movingLeft:
            self.moving=True
            self.rect.move_ip(-self.speed*self.statusState.speedModifier,0)

        else:
            self.moving=False
            self.rect.move_ip(0,0)

        self.rangeHaloUnderlay.rect.center=self.rect.center
        self.reloadingRect.center=self.rect.center
        self.hitbox.center=self.rect.center
        self.lifeBar.rect.left=self.rect.left
        self.lifeBar.rect.top=self.rect.top
class Squad(Human):

    def __init__(self,image='../images/squad1_handToHand.png',critical=False,spawn=(20,20) ):
        self.speed=6
        self.aiming=False
        self.moving=False
        self.shoot=False
        self.lastAttack=0
        self.critical=critical
        self.spawn=spawn
        self.primaryWeapon=guns.HandToHand()
        self.secondaryWeapon=guns.HandToHand()
        self.image = functions.loadImage(image)
        self.rect = self.image.get_rect(center=self.spawn)
        self.hitbox = self.image.get_rect(center=self.spawn, width=30, height=30)
        self.type=image[10:16]
        self.name=self.type
        super(Squad,self).__init__()

        self.lifeBarImage=pygame.image.load('../images/lifebar.png')
        self.lifeBarRect=self.lifeBarImage.get_rect(left=self.rect.left)
        self.lifeBar=Element(self.lifeBarImage,self.lifeBarRect,True)

        self.rangeHaloImage = pygame.image.load(HALOS[self.primaryWeapon.range*2])
        self.rangeHaloRect  = self.rangeHaloImage.get_rect(center=self.rect.center)
        self.rangeHaloUnderlay = Element(self.rangeHaloImage,self.rangeHaloRect,True)


        self.moving=False
        self.vectorStack=[]
        self.vector=None
        self.rawX=float(self.rect.centerx)
        self.rawY=float(self.rect.centery)

    def addVector(self,vector):

        self.vectorStack.append(vector)
        if len(self.vectorStack)==1:
            self.vector=vector

    def clearVectors(self):
        self.vectorStack=[]

    def moveTo(self,pos,waypoint=False):
        if waypoint==False:
            self.clearVectors()
            self.addVector(Vector(pos))
        else:
            self.addVector(Vector(pos))

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
            xcomp=-normalx*self.speed*self.statusState.speedModifier
            ycomp=-normaly*self.speed*self.statusState.speedModifier
            if abs(xcomp)>abs(self.vector.x-self.rect.centerx):
                xcomp=self.vector.x-self.rect.centerx
            if abs(ycomp)>abs(self.vector.y-self.rect.centery):
                ycomp=self.vector.y-self.rect.centery
            self.rawX+=xcomp
            self.rawY+=ycomp
            self.nextMove.move_ip(xcomp,ycomp)

            if (direction.x, direction.y) ==(0,0):
                self.vectorStack.remove(self.vector)
                try:
                    self.vector=self.vectorStack[0]
                except IndexError:
                    self.vector=None

    def update(self):
        self.rect=self.nextMove
        self.hitbox.center=self.rect.center
        self.rangeHaloUnderlay.rect.center=self.rect.center
        self.lifeBar.rect.left=self.rect.left
        self.lifeBar.rect.top=self.rect.top


class Civilian(Animate):
    def __init__(self,image='../images/girl_1.png',critical=False,spawnCenter=(20,20)):

        self.image=pygame.image.load(image)
        self.rect=self.image.get_rect(center=spawnCenter)
        self.critical=critical
        self.speed=5 #currently only used in title screen
        Animate.__init__(self)

#don't know if I want this yet

class Element(pygame.sprite.DirtySprite):
    def __init__(self, image, spawn,fullImageandRect=False):
        pygame.sprite.Sprite.__init__(self)
        if not fullImageandRect:
            self.image=pygame.image.load(image)
            self.rect=self.image.get_rect(center=spawn)
        else:
            self.image=image
            self.rect=spawn


class Inanimate(pygame.sprite.DirtySprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.placed=False
        self.cursorImage=self.image
        self.cursorRect=self.cursorImage.get_rect()
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

class ChainLink(Inanimate):
    def __init__(self, spawn):

        self.image=pygame.image.load('../images/chainLink_500.png')
        Inanimate.__init__(self)
        self.placedImageLoc='../images/chainLink_500.png'
        self.rect=self.image.get_rect(center=spawn)
        self.health=500
        self.snapTo=False
        self.moving=False
        self.vertical=True

    def takeDamage(self,damage):
        self.health-=damage
        if self.health<100:
            self.swapImage('../images/chainLink_100.png')
            if self.vertical==True:
                pass
            else:
                imgRot=pygame.transform.rotate(self.image,90)
                imgRotRect=imgRot.get_rect(center=self.rect.center)
                self.image=imgRot
                self.rect=imgRotRect
        elif self.health<200:
            self.swapImage('../images/chainLink_200.png')
            if self.vertical==True:
                pass
            else:
                imgRot=pygame.transform.rotate(self.image,90)
                imgRotRect=imgRot.get_rect(center=self.rect.center)
                self.image=imgRot
                self.rect=imgRotRect
        elif self.health<300:
            self.swapImage('../images/chainLink_300.png')
            if self.vertical==True:
                pass
            else:
                imgRot=pygame.transform.rotate(self.image,90)
                imgRotRect=imgRot.get_rect(center=self.rect.center)
                self.image=imgRot
                self.rect=imgRotRect
        elif self.health<400:
            self.swapImage('../images/chainLink_400.png')
            if self.vertical==True:
                pass
            else:
                imgRot=pygame.transform.rotate(self.image,90)
                imgRotRect=imgRot.get_rect(center=self.rect.center)
                self.image=imgRot
                self.rect=imgRotRect
            #if the picture image changes, need to change self.rect

class BucketOfWater(Inanimate):
    def __init__(self,spawn):
        self.image=pygame.image.load('../images/bucketOfWater_placed.png')
        Inanimate.__init__(self)
        self.moving=False
        self.rect=self.image.get_rect(center=spawn)
        self.health=1 #will never loose health, just needed for GameWorld.checkStatus (also may incorperate something with the more it gets walked on the better it gets)

class ItemSpawn(pygame.sprite.DirtySprite):
    def __init__(self,level,item,amount,spawn):
        super(ItemSpawn,self).__init__()
        tempString=str(item)
        tempString=tempString[16:-2]
        tempString=str(tempString[0].lower() + tempString[1:])
        self.item=tempString

        self.itemType=item

        self.level=level

        self.spawnPoint=spawn
        self.image=pygame.image.load('../images/%s' %self.item + '_item.png')
        self.rect=self.image.get_rect(center=spawn)
        self.amount=amount
        self.spawning=False
        pygame.font.init()
        self.font=pygame.font.Font('freesansbold.ttf',35)
        self.amountImage=self.font.render('X' + str(self.amount),1,(0,0,0))
        self.amountRect=self.amountImage.get_rect(left=self.rect.left,top=self.rect.top)
        self.amountElement=Element(self.amountImage,self.amountRect,True)
        self.outOfItemImage=pygame.image.load('../images/outOfItem.png')
        self.outOfItemRect=self.outOfItemImage.get_rect(center=self.rect.center)
        self.outOfItem=Element(self.outOfItemImage,self.outOfItemRect,True)
        self.cursorImage=pygame.image.load('../images/%s' %self.item + '_placed.png')
        self.cursorRect=self.cursorImage.get_rect()

    def spawnItem(self,spawn):
        #creates item and returns the pointer to that item
        #name is lowercase, capitalize to make name of class
        itemType=self.item.capitalize()
        object=self.itemType(spawn)
        self.amount-=1
        self.amountElement.image=self.font.render('X' + str(self.amount),1,(0,0,0))

        return object

    def addItems(self,number):
        self.amount+=number
        self.amountImage=self.font.render('X' + str(self.amount),1,(0,0,0))
        self.level.layer6.remove(self.amountElement)
        self.amountElement=Element(self.amountImage,self.amountRect,True)
        self.level.layer6.add(self.amountElement)
        self.level.dirtyRect=self.level.dirtyRect.union(self.rect)

class Vehicle(Inanimate):
    def __init__(self,spawn,color=(0,0,255)):
        super(Vehicle,self).__init__()
        self.color=color
        self.spawn=spawn
        self.health=1

    def update(self):
        self.rect=self.rect

class Truck(Vehicle):
    def __init__(self,spawn,color=(0,0,255)):
        self.color=color
        self.northImage=pygame.image.load('../images/%s' %globals.COLORS[self.color] + '_truck.png')
        self.image=self.northImage
        super(Truck,self).__init__(spawn,color)
        self.rect=self.image.get_rect(center=self.spawn)
        self.speed=15
        self.diagSpeedRaw=((self.speed/math.sqrt(2)))
        self.diagSpeed=int(round(self.diagSpeedRaw))
        self.vectorStack=[]
        self.vector=None
        self.rawX=float(self.rect.centerx)
        self.rawY=float(self.rect.centery)
        self.rotated=False

    def addVector(self,vector):

        self.vectorStack.append(vector)
        if len(self.vectorStack)==1:
            self.vector=vector

    def clearVectors(self):
        self.vectorStack=[]

    def rotateImage(self,degrees):
        #Not perfected
        if self.rotated==False:
            temp = self.image
            centered=self.rect.center
            self.image=pygame.transform.rotate(temp,degrees)
            self.rect=self.image.get_rect(center=centered)

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
            self.rect.move_ip(xcomp,ycomp)



            if (direction.x, direction.y) ==(0,0):
                self.vectorStack.remove(self.vector)

                try:
                    self.vector=self.vectorStack[0]
                except IndexError:
                    self.vector=None

    def moveTo(self,spawn):
        pass




class Projectile(Inanimate):
    def __init__(self,spawn,RelVector,gun):

        self.speed=25
        self.image=pygame.image.load('../images/projectile2.png')
        self.rect=self.image.get_rect(center=spawn)
        self.gun=gun
        self.damage=self.gun.damage

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







