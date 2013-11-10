#SeanFowler
#11/9/2013

import pygame

class CustomGroup(pygame.sprite.RenderUpdates):
    """
        Basically a custom shell that allows subclassing which simplifies the pygame.sprite.Group.add(*args) method
        Attributes:
            self.superGroups = contains a list of all super groups
        Methods:
            add
            addSubGroup
            addSuperGroup
    """
    def __init__(self):
        self.superGroups=[]
        super(CustomGroup,self).__init__()
    
    def add(self,*sprite):
        """
            runs the overwritten RenderUpdates.add and runs add to all superGroups
            args *sprite:
                all sprites to add in the form of sprite1,sprite2,sprite3...
        """
        super(CustomGroup,self).add(*sprite)
        for superGroup in self.superGroups:
            superGroup.add(*sprite)
    
    def addSubGroup(self,customSubGroup):
        """
            makes subGroup a sub group of self
            args:
                customSubGroup = CustomGroup
        """
        customSubGroup.superGroups.append(self)
    
    def addSuperGroup(self,customSuperGroup):
        """
            makes customSuperGroup a super group of self
            args:
                customSuperGroup = CustomGroup
        """
        self.superGroups.append(customSuperGroup)