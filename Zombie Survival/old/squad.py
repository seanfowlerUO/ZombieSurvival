import math, random
class Squad(object):
    def __init__(self,player):
        super(Squad,self).__init__()
        self.formation = SingleFile
        self.positions = self.formation(0).locations
        self.members = []
        self.player = player
    
    def addMember(self,member):
        #member should be an instance of class Human
        self.members.append(member)
        member.observe(self.player)
        self.player.addObservers([member])
        self.positions =self.formation(len(self.members)).locations
        for i in range(len(self.members)):
            self.members[i].setPlace(self.positions[i])
            
                  
    def setFormation(self,newFormation):
        #newFormation should be a uninstantiated class
        self.formation = newFormation
        self.positions = newFormation(len(self.members)).locations
        for i in range(len(self.members)):
            xoff = random.randrange(-20,20)/self.player.leadership
            yoff = random.randrange(-20,20)/self.player.leadership
            self.members[i].setPlace((self.positions[i][0]+xoff,self.positions[i][1]+yoff))
            
    def __len__(self):
        #Allows a len() call on Squad and returns length of members
        return len(self.members)
        
        
class Formation(object):
    #Abstract class should never be instantiated
    def __init__(self,number):
        super(Formation,self).__init__()
        self.locations=self.getLocations(number)
    
    def getLocations(self,number):
        #Overwritten in each subclass. Returns list of each location relative to the point man.
        #If however the desired number of squadmembers is not compatible with the desired formation,
        #it will kick the call back to its super class Formation
        #NOTE: this is SingleFile formation
        out=[]
        for i in range(number):
            out.append((0,i*60 +60))
        return out       
        
class SingleFile(Formation):
    def __init__(self,number):
        super(SingleFile,self).__init__(number)
        
    def getLocations(self,number):
        #Returns list of each location relative to the point man.
        #Kicks back to super since default is SingleFile
        return super(SingleFile,self).getLocations(number)
    
class DoubleStaggered(Formation):
    def __init__(self,number):
        super(DoubleStaggered,self).__init__(number)
    
    def getLocations(self,number):
        #Returns list of each location relative to the point man.
        out=[]
        for i in range(number):
            y = i*60 + 60
            if i%2 == 0:
                x = 60
            else:
                x = 0
            out.append((x,y))
        return out

class Wedge(Formation):
    def __init__(self,number):
        super(Wedge,self).__init__(number)
    
    def getLocations(self,number):
        #Returns list of each location relative to the point man.
        x=0
        y=0
        out=[]
        for i in range(number):
            #Add 75 every other iteration
            if i%2==0:
                x= math.fabs(x)+75
                y+=75
            else:
            #Make x negative every other iteration
                x*=-1
            out.append((x,y))
        return out

class FiveStar(Formation):
    def __init__(self,number):
        super(FiveStar,self).__init__(number)
        
    def getLocations(self,number):
        #Allowed to have a max of 4 members (plus pointman makes 5) if more than 4 members return default formation
        if number>4:
            return super(FiveStar,self).getLocations(number)
        #Returns list of each location relative to the point man.
        #This is a shifting formation, that means the pointman's position depends on how many people are in the formation
        out=[]
        if number==1:
            out+=[(200,0)]
        elif number==2:
            out+=[(100,100),(-100,100)]
        elif number==3:
            out+=[(200,0),(50,100),(150,100)]
        elif number==4:
            out+=[(100,100),(-100,100),(-50,200),(50,200)]
        #If number is 0, this will return an empty list which is good
        return out


            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
                
        
    
        