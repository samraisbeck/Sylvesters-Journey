###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: powerBlock.py
# Description: Classes for the power blocks and item blocks
###############################
from localVariables import *
from movableObject import MovableObject
import pygame

class PowerBlock(MovableObject):
    """ Power blocks object """
    def __init__(self, x, y, sizeTuple = 0):
        self.imageNotHit = pygame.image.load(IMG_PATH_POWERBLOCK)
        self.imageHit = pygame.image.load(IMG_PATH_POWERBLOCK_HIT)
        if sizeTuple != 0:
            self.imageNotHit = pygame.transform.scale(self.imageNotHit, sizeTuple)
            self.imageHit = pygame.transform.scale(self.imageHit, sizeTuple)
        self.images = [self.imageNotHit, self.imageHit]
        self.imageIndex = 0
        self.x = x
        self.y = y
        self.w = self.imageNotHit.get_width()
        self.h = self.imageNotHit.get_height()
        self.hit = False
        self.visible = False
        self.centerSpeed = 5

    def draw(self, surface):
        """ Draws the correct image """
        if self.visible:
            surface.blit(self.images[self.imageIndex], (self.x, self.y))

    def update(self, surface, characterObj):
        """ Updates the power block, including its image """
        self.checkVisible()
        self.x -= characterObj.speedX
        self.centerLevel(characterObj)
        if self.hit:
            self.imageIndex = 1
        self.draw(surface)

class ItemBlock(PowerBlock):
    """ Item block object """
    def __init__(self, x, y, sizeTuple = 0):
        """ Basically the same as powerBlock, but the images are different
            which changes a lot of things in the __init__() """
        self.imageNotHit = pygame.image.load(IMG_PATH_ITEMBLOCK)
        self.imageHit = pygame.image.load(IMG_PATH_ITEMBLOCK_HIT)
        if sizeTuple != 0:
            self.imageNotHit = pygame.transform.scale(self.imageNotHit, sizeTuple)
            self.imageHit = pygame.transform.scale(self.imageHit, sizeTuple)
        self.images = [self.imageNotHit, self.imageHit]
        self.imageIndex = 0
        self.x = x
        self.y = y
        self.w = self.imageNotHit.get_width()
        self.h = self.imageNotHit.get_height()
        self.hit = False
        self.visible = False
        self.centerSpeed = 5
