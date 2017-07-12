###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: items.py
# Description: Every item's class
###############################

from movableObject import MovableObject
from localVariables import *
import pygame

class GeneralItem(MovableObject):
    """ The general item class structure """
    def __init__(self, imagePath, x, y, sizeTuple=0):
        MovableObject.__init__(self, imagePath, x, y)
        if sizeTuple != 0:
            self.image = pygame.transform.scale(self.image, sizeTuple)

class GravityBoost(GeneralItem):
    """ Gravity booster object """
    def __init__(self, x, y, sizeTuple = 0):
        self.image = IMG_PATH_GRAVITY
        GeneralItem.__init__(self, self.image, x, y, sizeTuple)

class Invincibility(GeneralItem):
    """ Invincibility object """
    def __init__(self, x, y, sizeTuple = 0):
        self.image = IMG_PATH_INVINCIBLE
        GeneralItem.__init__(self, self.image, x, y, sizeTuple)

class Superjump(GeneralItem):
    """ Superjump object """
    def __init__(self, x, y, sizeTuple = 0):
        self.image = IMG_PATH_SUPERJUMP
        GeneralItem.__init__(self, self.image, x, y, sizeTuple)
        self.canBeUsed = False # Only turns true when the boss is killed

    def draw(self, surface):
        """ Draws superjump if it can be used """
        if self.visible and self.canBeUsed:
            surface.blit(self.image, (self.x, self.y))

class Coin(GeneralItem):
    """ Coin object """
    def __init__(self, x, y, sizeTuple = 0):
        self.image = IMG_PATH_COIN
        GeneralItem.__init__(self, self.image, x, y, sizeTuple)

class Health(GeneralItem):
    """ Health (heart) object """
    def __init__(self, x, y, sizeTuple = 0):
        self.image = IMG_PATH_HEALTH
        GeneralItem.__init__(self, self.image, x, y, sizeTuple)

class SwordIcon(GeneralItem):
    """ Sword icon object. Used for collision to add a usable sword
        to the character's item bank """
    def __init__(self, x, y, sizeTuple = 0):
        self.image = IMG_PATH_SWORD
        GeneralItem.__init__(self, self.image, x, y, sizeTuple)
