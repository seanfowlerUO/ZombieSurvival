#Author
#Date

class Driver(object):
    '''
        This is the main driver class for the program
        Attributes:
            currentState    : corresponds to the drivers current state
            runningState    : an instantiated instance of RunningState
            pausedState     : an instantiated instance of PausedState
            gameWorld       : the drivers GameWorld
            graphicsHandler : the drivers GraphicsHandler
            actionQueue     : the drivers ActionQueue
            
        Methods:
            popAction(self)
    '''
    def __init__(self):
        super(Driver,self).__init__()
    
    def popAction(self):
        """
            Pops runs all stored actions who's timeToExecute is < than current time
        """
        pass
    
class DriverState(object):
    """
        Abstract class. Should never be instantiated except within subclasses
    """
    def __init__(self):
        super(DriverState,self).__init__()
    
    def catchEvents(self):
        """
            uses pygame.event.get() to catch and handle all events
            
            Should be overwritten in each Subclass
        """

class DriverRunningState(DriverState):
    """
        State when the game is active (not paused)
        Methods:
            catchEvents(self)
    """
    def __init__(self):
        super(DriverRunningState,self).__init__()
        
    def catchEvents(self):
        """
        users pygame.event.get() to catch and handle all events
        """
        pass
    
class DriverPausedState(DriverState):
    """
        State when the game is paused
        Methods:
            catchEvents(self)
    """
    def __init(self):
        pass
    
    def catchEvents(self):
        pass
    