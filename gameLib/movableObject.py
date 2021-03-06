###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: movableObject.py
# Description: Basic template for all movable objects
###############################

from localVariables import *
import pygame

class MovableObject(object):
    """ The standard class for movable objects """
    def __init__(self, imagePath, x, y):
        self.image = pygame.image.load(imagePath).convert_alpha()
        self.x = x
        self.y = y
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.centerSpeed = 5
        self.visible = False

    def checkVisible(self):
        """ Checks to see if object is on the screen """
        if self.x <= WIDTH and self.x+self.w >= 0 and self.y <= HEIGHT and \
           self.y+self.h >= 0:
            self.visible = True
        else:
            self.visible = False

    def getRect(self):
        """ Returns a rectangular shape around the object """
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, surface):
        """ Draws object if it is on the screen """
        if self.visible:
            surface.blit(self.image, (self.x, self.y))

    def centerLevel(self, characterObj):
        if not ((characterObj.y+characterObj.h <= (HEIGHT/6)*5 and characterObj.speedY > 0) or\
            (characterObj.y >= HEIGHT/6 and characterObj.speedY < 0)):
            self.y -= characterObj.speedY
        if not characterObj.centered and characterObj.y - HEIGHT/2 > 0:
            self.y -= self.centerSpeed
        elif not characterObj.centered:
            self.y += self.centerSpeed


    def update(self, surface, characterObj):
        """ Movable objects update method to be used in the game class """
        self.checkVisible()
        self.x -= characterObj.speedX
        self.centerLevel(characterObj)
        self.draw(surface)
