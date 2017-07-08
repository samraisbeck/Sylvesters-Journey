###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: door.py
# Description: Class for the door between worlds
###############################
import pygame
from localVariables import *
from movableObject import MovableObject

class Door(MovableObject):
    """ Small class that operates the doors between levels """
    def __init__(self, imagePath, x, y, sizeTuple=0):
        MovableObject.__init__(self, imagePath, x, y)
        self.imageClosed = self.image.convert_alpha()
        self.imageOpened = pygame.image.load(IMG_PATH_DOOR_OPENED).convert_alpha()
        self.opened = False

    def draw(self, surface):
        """ Draws the door opened or closed, depending on the boolean """
        if not self.opened:
            surface.blit(self.imageClosed, (self.x, self.y))
        else:
            surface.blit(self.imageOpened, (self.x, self.y))
        
