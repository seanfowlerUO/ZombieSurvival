#author
#date

import pygame

class Area(object):
    """
        This is one single area of a map grid
        Attributes:
            self.sprite: an AreaSprite which hold the picture and rect for this Area
            self.areaSchematic: AreaSchematic this is the source for the area information and should probably not
                                ever be directly referenced
            self.areaObjects: CustomGroup which holds all inanimates and walls on the map
    """
    def __init__(self):
        super(Area,self).__init__()
        
class AreaSchematic(object):
    """
        This is an object which is used to get the important information from for the Area. It is basically a "preCompiled"
        form of the Area
        Attributes:
            self.source: a .area file which holds all the necesary information to make a Area
        
        Methods:
            compile(self):
                turns the info from self.source into Sprites
                returns:
                    A CustomGroup filled with the all needed Sprites
    """
    def __init__(self):
        super(AreaSchematic,self).__init__()
        
class AreaSprite(pygame.sprite.DirtySprite):
    """
        This is the SpriteObject for Area
        Attributes:
            self.image: a pygame.Surface corresponding to what the map looks like to the user
            self.rect : a pygame.Rect which is derived from self.image
    """
    def __init__(self):
        super(AreaSprite,self).__init__()