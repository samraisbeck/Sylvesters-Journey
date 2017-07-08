###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: plats.py
# Description: The classes for platforms and walls
###############################

from localVariables import *
from movableObject import MovableObject
import pygame

class Plats(MovableObject):
    """ Platform objects """
    def __init__(self, imagePath, x, y, sizeTuple=0):
        MovableObject.__init__(self, imagePath, x, y)
        if sizeTuple != 0:
            self.image = pygame.transform.scale(self.image, sizeTuple).convert_alpha()
            self.w = self.image.get_width()
            self.h = self.image.get_height()

class Wall(Plats):
    """ Wall objects. Only created so that isinstance() can easily tell it
        is in fact a wall """
    def __init__(self, imagePath, x, y, sizeTuple=0):
        Plats.__init__(self, imagePath, x, y, sizeTuple)


			
        
        
        
        

