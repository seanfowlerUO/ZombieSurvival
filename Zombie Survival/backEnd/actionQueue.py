#Sean Fowler
#11/9/2013

import heapq

class ActionQueue(object):
    '''
        Priority Queue container for Actions
            Attributes:
                self.actions = list of current actions (stored as heap)
    '''
    def __init__(self):
        super(ActionQueue,self).__init__()
        self.actions = []
    
    def push(self,action):
        heapq.heappush(self.actions,action)
        
    def pop(self):
        return heapq.heappop(self.actions)
    
    def __getitem__(self, item): #Allows proper indexing on ActionQueue
        return self.actions[item]
    
    def __len__(self): #allows len() function to be used
        return len(self.actions)
    
    def __iter__(self):
        return self.actions.__iter__()
    
    def __bool__(self):
        return self.actions.__bool__()
    
    
class Action(object):
    '''
        These are the objects which will fill ActionQueue inside the driver
        Attributes:
            self.timeToExecute = time which self.executable should execute (based on drivers clock)
            self.executable    = executable object should be function object not actual function (ex. function not function())
            self.args          = arguments for the self.executable
    '''
    def __init__(self,timeToExecute,executable,*args):
        super(Action,self).__init__()
        self.timeToExecute=timeToExecute
        self.executable=executable
        self.args = args
        
    def execute(self):
        self.executable(self.args) #run your executables with your arguments
        
    def flipFlag(self,flag):
        return not flag
    
    def __lt__(self,other): #We need a < and > method because this needs to be comparable as it will be in a heapq
        if type(other)==type(1):
            return self.timeToExecute<other
        assert(type(other)==type(self)) #should only be comparing against ints and other Actions
        return self.timeToExecute<other.timeToExecute
    
    def __gt__(self,other): 
        if type(other)==type(1):
            return self.timeToExecute>other
        assert(type(other)==type(self)) #should only be comparing against ints and other Actions
        return self.timeToExecute>other.timeToExecute
    
    def __str__(self):
        return "(" + str(self.timeToExecute)+","+str(self.executable)+","+str(self.args)+")"

    
if __name__ == "__main__":
    import time
    w = time.sleep
    
    def function(string):
        print(string)
    q = ActionQueue()
    for x in range(10):
        a = Action(x*2,function,str(x*2))
        q.push(a)
    for x in range(20):
        try:
            if q[0]<x:
                q.pop().execute()
        except:
            pass
        w(1)
    
        
    
        
    
        
        
