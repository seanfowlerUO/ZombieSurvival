__author__ = 'Sean Fowler'

import vector,classes,globals,relVector,random
from functions import *

class Observer(object):
    def __init__(self):
        super(Observer,self).__init__()
        self.observing=[]

    def move(self):
        pass

    def observe(self,o):
        self.observing.append(o)

    def __del__(self):
        for o in self.observers:
            if self in o.observing:
                o.observing.remove(self)
            if o.target==self:
                o.target=None
                o.vector=None

        for o in self.observing:
            if self in o.observers:
                o.observers.remove(self)

class Observable(object):
    def __init__(self):
        super(Observable,self).__init__()
        self.observers=[]

    def addObservers(self,olist):
        for o in olist:
            if o in self.observers:
                pass

            else:
                self.observers.append(o)
                o.observe(self)



    def notifyObservers(self):
        #print self.observers
        for o in self.observers:
            o.considerVector(self.vector)


class ZombieObserver(Observer,Observable,classes.Zombie):
    def __init__(self):
        super(ZombieObserver,self).__init__()
        self.vectorStack=[]
        self.vector=None
        self.rawX=self.rect.centerx
        self.rawY=self.rect.centery
        self.target=None
        self.speed=self.speed+random.randrange(3)

    def addVector(self,relVec):
        self.vector=relVec
        self.vector.scale(self.speed)

    def move(self):
        if self.vector!=None:
            (xComp,yComp)=(self.vector.x,self.vector.y)
            self.rawX+=xComp
            self.rawY+=yComp
            self.rect.move_ip(xComp,yComp)
            self.stackRect.center=self.rect.center
            self.notifyObservers()
        else: pass

    def chooseTarget(self):
        if len(self.observing)==0:
            return None
        elif len(self.observing)==1:
            return self.observing[0]
        else:
            target=self.observing[0]
            shortest=distance(self.observing[0].rect.center,self.rect.center)
            for brain in self.observing:
                if distance(brain.rect.center,self.rect.center)<shortest:
                    target=brain
                    shortest=distance(brain.rect.center,self.rect.center)
            return target
        
    def findTarget(self,list):
        if len(list)==0:
            return None
        elif len(list)==1:
            return list[0]
        else:
            target=list[0]
            shortest=distance(list[0].rect.center,self.rect.center)
            for brain in list:
                if distance(brain.rect.center,self.rect.center)<shortest:
                    target=brain
                    shortest=distance(brain.rect.center,self.rect.center)
            return target



class HumanObserver(Observer,Observable,classes.Civilian):
    def __init__(self):
        super(HumanObserver,self).__init__()
        self.type='girl_%s'%random.randrange(1,4)
        self.image=pygame.image.load('../images/%s'%self.type+'.png')
        self.rect=self.image.get_rect()
        self.vector=None
        self.rawX=self.rect.centerx
        self.rawY=self.rect.centery
        self.speed=3+random.randrange(3)
        self.target=None

    def considerVector(self,vect):

        if vect==None:
            pass
        else:
            vect.scale(self.speed)
            if self.vector==None:
                self.vector=vect
            else:
                self.vector+=vect
                self.vector.scale(self.speed)

    def move(self):
        if self.vector!=None:
            self.rect.move_ip(self.vector.x,self.vector.y)
            self.vector=None
        else:
            pass





