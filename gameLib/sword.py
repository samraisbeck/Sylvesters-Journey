###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: sword.py
# Description: The class for the character's sword
###############################
from localVariables import *
import pygame

class Sword(object):
    """ Sword object """
    def __init__(self, x, y, sizeTuple=0):
        self.image = pygame.image.load(IMG_PATH_SWORD).convert_alpha()
        if sizeTuple != 0:
            self.image = pygame.transform.scale(self.image, sizeTuple)
        self.notRotatedL = self.image
        self.rotatedL1 = pygame.transform.rotate(self.image, 20)
        self.rotatedL2 = pygame.transform.rotate(self.image, 40)
        self.rotatedL3 = pygame.transform.rotate(self.image, 60)
        self.rotatedL4 = pygame.transform.rotate(self.image, 80)
        self.rotatedL5 = pygame.transform.rotate(self.image, 100)
        self.rotatedL6 = pygame.transform.rotate(self.image, 120)
        self.imagesLeft = [self.rotatedL1, self.rotatedL2, self.rotatedL3,
                           self.rotatedL4, self.rotatedL5, self.rotatedL6, self.rotatedL5,
                           self.rotatedL4, self.rotatedL3, self.rotatedL2, self.rotatedL1]
        self.notRotatedR = pygame.transform.flip(self.image, True, False)
        self.rotatedR1 = pygame.transform.rotate(self.notRotatedR, -20)
        self.rotatedR2 = pygame.transform.rotate(self.notRotatedR, -40)
        self.rotatedR3 = pygame.transform.rotate(self.notRotatedR, -60)
        self.rotatedR4 = pygame.transform.rotate(self.notRotatedR, -80)
        self.rotatedR5 = pygame.transform.rotate(self.notRotatedR, -100)
        self.rotatedR6 = pygame.transform.rotate(self.notRotatedR, -120)
        self.imagesRight = [self.rotatedR1, self.rotatedR2, self.rotatedR3,
                           self.rotatedR4, self.rotatedR5, self.rotatedR6, self.rotatedR5,
                           self.rotatedR4, self.rotatedR3, self.rotatedR2, self.rotatedR1]
        self.imageIndex = 0
        self.imageCounter = 0
        self.swingSpeed = 2
        self.displayImage = self.image # Image for when the sword isn't swinging
        self.x = x
        self.y = y
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.visible = False
        self.swinging = False
        self.canHit = True
        self.swingCount = 0
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def getRect(self, image):
        """ Takes an image and returns the rectangular border around the image """
        return image.get_rect()

    def checkSwing(self, events):
        """ Checks to see if the character is swinging the sword """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.swinging = True

    def checkSwingCount(self):
        """ Limits the swings available to 5 """
        if self.swingCount >= 5:
            self.visible = False

    def counter(self):
        """ Runs through the images of the sword swing animation """
        self.imageCounter += 1
        if self.imageCounter >= self.swingSpeed:
            self.imageCounter = 0
            self.imageIndex += 1
            if self.imageIndex == len(self.imagesLeft):
                self.imageIndex = 0
                self.swinging = False
                self.canHit = True
                self.swingCount += 1
                self.checkSwingCount()

    def getRotated(self, character):
        """ Returns the rectangular border of the rotated image """
        if character.direction == "left":
            originalRect = pygame.Rect(self.x-character.w-self.w, self.y, self.w, self.h)
            rotatedRect = self.getRect(self.imagesLeft[self.imageIndex])
            rotatedRect.bottomright = originalRect.bottomright
        else:
            originalRect = pygame.Rect(self.x, self.y, self.w, self.h)
            rotatedRect = self.getRect(self.imagesRight[self.imageIndex])
            rotatedRect.bottomleft = originalRect.bottomleft
        return rotatedRect

    def drawArms(self, surface, character):
        """ Draws arms on the character based on the position of the sword """
        rotatedCoords = self.getRotated(character)
        if character.direction == "left":
            pygame.draw.line(surface, BLACK, character.getRect().center,
                             (rotatedCoords.centerx+10, rotatedCoords.centery+20), 4)
            pygame.draw.line(surface, BLACK, (character.getRect().centerx-10, character.getRect().centery),
                             (rotatedCoords.centerx+10, rotatedCoords.centery+10), 4)
        else:
            pygame.draw.line(surface, BLACK, character.getRect().center,
                             (rotatedCoords.centerx-10, rotatedCoords.centery+20), 4)
            pygame.draw.line(surface, BLACK, (character.getRect().centerx+10, character.getRect().centery),
                             (rotatedCoords.centerx-10, rotatedCoords.centery+10), 4)

    def draw(self, surface, character):
        """ Draws the sword with the correct coordinates and image """
        if (character.y+character.h <= (HEIGHT/6)*5 and character.speedY > 0) or\
            (character.y >= HEIGHT/6 and character.speedY < 0):
            self.y += character.speedY
        rotatedCoords = self.getRotated(character)
        if not self.swinging and character.direction == "left":
            self.displayImage = self.notRotatedL
            surface.blit(self.displayImage, (self.x-character.w-self.w, self.y))
        elif not self.swinging:
            self.displayImage = self.notRotatedR
            surface.blit(self.displayImage, (self.x, self.y))
        else:
            if character.direction == "left":
                self.displayImage = self.imagesLeft[self.imageIndex]
                surface.blit(self.displayImage, (rotatedCoords.left, rotatedCoords.top+10))
            else:
                self.displayImage = self.imagesRight[self.imageIndex]
                surface.blit(self.displayImage, (rotatedCoords.left, rotatedCoords.top+10))
            self.counter()
        self.rect = (rotatedCoords.x, rotatedCoords.y, rotatedCoords.w, rotatedCoords.h)
        self.drawArms(surface, character)

    def update(self, surface, character, events):
        """ Sword update method to be used in the main game class """
        self.checkSwing(events)
        self.draw(surface, character)
