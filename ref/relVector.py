__author__ = 'Sean Fowler'
import math

class RelVector(object):
    #Very similar to Vector however it uses relative points
    def __init__(self,(sx,sy),(fx,fy)):
        super(RelVector,self).__init__()
        self.fx=fx
        self.fy=fy
        self.sx=sx
        self.sy=sy
        self.x=self.fx-self.sx
        self.y=self.fy-self.sy

    def __sub__(self,other):
        return RelVector((0,0),(self.x-other.x,self.y-other.y))

    def __add__(self,other):
        return RelVector((0,0),(self.x+other.x,self.x+other.y))

    def __getitem__(self,item):
        #Allows indexing on the vector
        if item==1:
            return self.y
        if item==0:
            return self.x
        else:
            raise "RelVector has no item " + str(item)

    def __str__(self):
        return str(self.x)+','+str(self.y)

    def getLength(self):
        # assumes origin is 0,0 and gets length of vector
        return math.sqrt((self.x)**2 + (self.y)**2)

    def scale(self,scalar):
        (xNorm,yNorm) = self.getNormal()
        self.x=scalar*xNorm
        self.y=scalar*yNorm

    def getNormal(self):
        length = self.getLength()
        if length==0:
            return (0,0)
        else:
            return ((self.x)/length,(self.y)/length)






if __name__=="__main__":
    v=RelVector((0,0),(10,10))
    v2=RelVector((15,20),(0,25))
    print v.getNormal()
    print v2.getNormal()

    v3=v+v2
    v3.scale(5)
    print v3
