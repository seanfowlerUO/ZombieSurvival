#Sean Fowler
#11/11/2013

class FlagBlock(object):
    """
        This is a generic flagblock with all needed methods built in for easy use
        ATTRIBUTES:
            self.flagToIndexDict: dictionary containing str(flag):index in self.flags
            self.flags: a list containing the status of all flags in the block. ORDER MATTERS
        
        METHODS:
            flipFlag: flips the given flag
            addFlag : adds a new flag to the FlagBlock
            getFlag : gets a flags status
    """
    def __init__(self, *flagDefaultTuples):
        super(FlagBlock,self).__init__()
        self.flagToIndexDict = dict()
        self.flags = []
        for flagTuple in flagDefaultTuples:
            self.flags.append(flagTuple[1])
            self.flagToIndexDict[flagTuple[0]] = flagDefaultTuples.index(flagTuple)
            
    def flipFlag(self,flag):
        self.flags[self.flagToIndexDict[flag]] = not self.flags[self.flagToIndexDict[flag]]
            
    def addFlag(self,flagDefaultTuple):
        self.flags.append(flagDefaultTuple[1])
        self.flagToIndexDict[flagDefaultTuple[0]] = len(self.flags) - 1
    
    def getFlag(self,flag):
        return self.flags[self.flagToIndexDict[flag]]
    
    def __add__(self,other):
        if type(other)!=type(self):
            raise TypeError("Cannot a add FlagBlock to anything but another FlagBlock")
        else:
            flagBlockOut =  FlagBlock()
            for flag in self.flagToIndexDict:
                flagBlockOut.addFlag((flag,self.flags[self.flagToIndexDict[flag]]))
            for flag in other.flagToIndexDict:
                flagBlockOut.addFlag((flag,other.flags[other.flagToIndexDict[flag]]))
            return flagBlockOut
        
    
if __name__=="__main__":
    fb = FlagBlock(("flag1",False),("flag2",False),("flag3",True),("flag4",False))
    if fb.getFlag("flag1")==False:
        print "PASSED"
    else:
        print "FAILED" + " flag1 check"
    fb.flipFlag("flag1")
    
    if fb.getFlag("flag1")==True:
        print "PASSED"
    else:
        print "FAILED" + " flag1 check"    
    fb2 = FlagBlock(("flag5",False),("flag6",True))
    fb  = fb + fb2
    print fb.flagToIndexDict
    for flag in fb.flagToIndexDict:
        print flag + " = " + str(fb.flags[fb.flagToIndexDict[flag]])
    if fb.getFlag("flag6")==True:
        print "PASSED"
    else:
        print "FAILED" + " flag6 check"
        
    if fb.getFlag("flag1")==True:
        print "PASSED"
    else:
        print "FAILED second flag1 check"
    try:
        fb = fb+1
    except TypeError:
        print "PASSED"
        print "TYPE ERROR CATCH: "
        TypeError.message
    
    
    
    
    