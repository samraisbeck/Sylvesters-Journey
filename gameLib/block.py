###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: block.py
# Description: Class for blocks that can be picked up and placed
###############################
from movableObject import MovableObject
from localVariables import *
import pygame

class Block(MovableObject):
    """ Small class for the blocks that can be picked up and placed as
        platforms """
    def __init__(self, imagePath, x, y, sizeTuple = 0):
        MovableObject.__init__(self, imagePath, x, y)
        if sizeTuple != 0:
            self.image = pygame.transform.scale(self.image, sizeTuple)
            self.w, self.h = sizeTuple
        self.placed = False
        


    

    
        
    
