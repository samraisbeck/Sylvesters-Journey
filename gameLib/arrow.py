###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: arrow.py
# Description: Class for an arrow that points at an angle
###############################
from movableObject import MovableObject
from localVariables import *
import pygame

class Arrow(MovableObject):
    """ Small class that creates an arrow pointing on an angle """
    def __init__(self, x, y, angle = 0):
        MovableObject.__init__(self, IMG_PATH_ARROW, x, y)
        if angle != 0:
            self.image = pygame.transform.rotate(self.image, angle).convert_alpha()
