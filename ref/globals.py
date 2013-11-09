__author__ = 'Sean Fowler'
import pygame, math

COLORS = dict({(255,0,0):'red',(0,255,0):'green',(0,0,255):'blue',(0,0,0):'black',(255,255,255):'white',(0,64,0):'darkGreen'})
HALO_HEIGHT=dict({'1':62,'2':137,'3':212,'4':287,'5':362})
FPS=40
FPS_CLOCK=pygame.time.Clock()
DISPLAY_WIDTH=1200
DISPLAY_HEIGHT=760
LEFT_EDGE=200
RIGHT_EDGE=DISPLAY_WIDTH
TOP_EDGE=0
BOTTOM_EDGE=DISPLAY_HEIGHT

LIVES = 5
ZOMBIE_IMAGES = ['../images/zombie1.png','../images/zombie2.png','../images/zombie3.png','../images/zombie4.png','../images/zombie5.png']

def isInPlay((x,y),left=LEFT_EDGE,right=RIGHT_EDGE,top=TOP_EDGE,bottom=BOTTOM_EDGE):
    #Takes an xy tuple and returns x if x is out of play, y if y is out of play and False if both are out of play (true else)
    xIn=False
    xLeft=False
    xRight=False
    if x<=left:
        xLeft=True
    elif x>=right:
        xRight=True
    else:
        xIn=True

    yIn=False
    yLow=False
    yHigh=False
    if y>=bottom:
        yLow=True
    elif y<=top:
        yHigh=True
    else:
        yIn=True

    if yIn and xIn:
        return True
    else:
        return [xLeft,xRight,yLow,yHigh]

def inRange((x1,y1),(x2,y2),range):
    return distance((x1,y1),(x2,y2)) < range #returns True if center1 is inrange center2
    
def distance((x1,y1),(x2,y2)):
    return math.sqrt(((y2-y1)**2)+((x2-x1)**2))
    
    
    
    
    