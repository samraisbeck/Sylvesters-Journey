###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: main.py
# Description: Class for buttons to be pressed
###############################
from localVariables import *
import pygame, sys

class Button(object):
    """a class for buttons"""
    def __init__(self, text, x, y, w=140, h=70, colorMouseOff=GREEN, colorMouseOn=BLUE):
        self.text = text
        self.colorMouseOff = colorMouseOff
        self.colorMouseOn = colorMouseOn
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.shape = pygame.Rect(x, y, w, h)
        self.mouseOver = None
        self.pressed = None
        self.font = pygame.font.Font('C:\\Windows\\Fonts\\impact.ttf', 40)
        self.buttonFont = None
        self.rectButtonFont = None
        self.updateText()


    def updateText(self):
        """ Renders the font and sets its coordinates to the middle of
            the button """
        self.buttonFont = self.font.render(self.text, True, self.colorMouseOff)
        self.rectButtonFont = self.buttonFont.get_rect(center=((self.shape.left+self.shape.right)/2,
                                                               (self.shape.top + self.shape.bottom)/2))

    def checkState(self, events):
        """ Takes pygame.event.get() and checks mouse events """
        self.mouseOver = self.shape.collidepoint(pygame.mouse.get_pos())
        self.pressed = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.mouseOver:
                self.pressed = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

    def draw(self, surface):
        """ Draws the button and font with the right colors """
        if self.mouseOver:
            pygame.draw.rect(surface, self.colorMouseOn, self.shape)
            self.buttonFont = self.font.render(self.text, True, self.colorMouseOff)
        else:
            pygame.draw.rect(surface, self.colorMouseOff, self.shape)
            self.buttonFont = self.font.render(self.text, True, self.colorMouseOn)
        surface.blit(self.buttonFont, self.rectButtonFont)
