__author__ = 'Sean Fowler'
import math

class Vector(object):
    #Vector logic used for vector movement
    def __init__(self,(x,y)):
        super(Vector,self).__init__()
        self.x=x
        self.y=y

    def __sub__(self,other):
        return Vector((self.x-other.x,self.y-other.y))

    def __add__(self,other):
        return Vector((self.x+other.x,self.y+other.y))

    def __getitem__(self,item):
        #Allows indexing on the vector
        if item==1:
            return self.y
        if item==0:
            return self.x
        else:
            raise "Vector has no item " + str(item)

    def __str__(self):
        return str(self.x)+','+str(self.y)
    
    def getLength(self):
        # assumes origin is 0,0 and gets length of vector
        return math.sqrt(self.x**2 + self.y**2)

    def scale(self,scalar):
        (xNorm,yNorm) = self.getNormal()
        self.x=scalar*xNorm
        self.y=scalar*yNorm
        
    def getNormal(self):
        length = self.getLength()
        if length==0:
            return (0,0)
        else:
            return (self.x/length,self.y/length)

if __name__=="__main__":
    pass

