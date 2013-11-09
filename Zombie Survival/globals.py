import math,pygame

WIDTH  = 1080
HEIGHT = 720

CLOCK = pygame.time.Clock()
FPS = 60

def inRange((x1,y1),(x2,y2),range):
    #Returns False if object1 is not in range object2 and the distance if it is in range
    d = distance((x1,y1),(x2,y2)) 
    if d > range:
        return False
    else:
        return d
        
def distance((x1,y1),(x2,y2)):
    return math.sqrt(((y2-y1)**2)+((x2-x1)**2))