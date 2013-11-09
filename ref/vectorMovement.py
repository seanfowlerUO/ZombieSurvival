__author__ = 'Sean Fowler'
from vector import Vector
class vectorMovement(object):
    def __init__(self):
        super(vectorMovement,self).__init__()

    def addVector(self,vec):
        self.vector = vec

    def move(self):

        if self.vector==None:
            self.moving=False
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