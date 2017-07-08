###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: localVariables.py
# Description: Includes images and one function, used all throughout the classes
#              of the game.
###############################
import pygame, os

def getFilepath(filename):
    """ Takes the filename and based on the last 3 characters,
        it decides what folder to look in for it """
    rootPath = os.path.dirname(os.path.dirname(__file__))
    if filename[-3:] == "png" or filename[-3:] == "jpg":  
        return rootPath+"\\data\\pictures\\"+filename
    elif filename[-3:] == "txt":
        return rootPath+"\\data\\levels\\"+filename
    elif filename[-3:] == "mp3" or filename[-3:] == "wav":
        return rootPath+"\\data\\music and sounds\\"+filename
    return rootPath+"\\data\\"+filename

WIDTH = 900
HEIGHT = 700
ORIGIN = 0, 0
OFF_SCREEN = -999

BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
YELLOW = 255,255,0

BASIC_FONT = "C:\\Windows\\Fonts\\impact.ttf"
COOL_FONT = getFilepath("coolFont.ttf")

IMG_PATH_MAINMENU = getFilepath("menuBackground.png")
IMG_PATH_INSTRUCTIONS = getFilepath("menuInstructions.png")
IMG_PATH_STORY = getFilepath("storyBackground.png")
IMG_PATH_MECHANICS = getFilepath("mechanicsBackground.png")
IMG_PATH_LVLSELECT = getFilepath("levelSelection.jpg")
IMG_PATH_TRANSITION = getFilepath("transition.png")
IMG_PATH_WIN = getFilepath("winScreen.png")
IMG_PATH_CREDITS = getFilepath("credits.png")
IMG_PATH_CHECK = getFilepath("check.png")

IMG_PATH_CHARACTER = getFilepath("charStanding.png")
IMG_PATH_CHARACTER1 = getFilepath("charRunning1.png")
IMG_PATH_CHARACTER2 = getFilepath("charRunning2.png")
IMG_PATH_CHARACTER3 = getFilepath("charRunning3.png")
IMG_PATH_CHARACTER4 = getFilepath("charRunning4.png")
IMG_PATH_CHARACTER5 = getFilepath("charRunning5.png")
IMG_PATH_CHARACTERJ = getFilepath("charJumping.png")

IMG_PATH_PLATFORM = getFilepath("platform.png")
IMG_PATH_BLOCK = getFilepath("block.png")
IMG_PATH_WALL = getFilepath("wall.png")
IMG_PATH_POWERBLOCK = getFilepath("powerBlock.png")
IMG_PATH_POWERBLOCK_HIT = getFilepath("powerBlockHit.png")
IMG_PATH_ITEMBLOCK = getFilepath("itemBlock.png")
IMG_PATH_ITEMBLOCK_HIT = getFilepath("itemBlockHit.png")

IMG_PATH_GRAVITY = getFilepath("gravityBoost.png")
IMG_PATH_SUPERJUMP = getFilepath("superjump.png")
IMG_PATH_INVINCIBLE = getFilepath("invincibility.png")
IMG_PATH_BUBBLE = getFilepath("invinBubble.png")
IMG_PATH_COIN = getFilepath("coin.png")
IMG_PATH_HEALTH = getFilepath("heart.png")
IMG_PATH_SWORD = getFilepath("sword.png")
IMG_PATH_ARROW = getFilepath("arrow.png")

IMG_PATH_ENEMY1 = getFilepath("enemy1.png")
IMG_PATH_ENEMY2 = getFilepath("enemy2.png")
IMG_PATH_BOSS1 = getFilepath("boss1.png")

IMG_PATH_DOOR_CLOSED = getFilepath("doorClosed.png")
IMG_PATH_DOOR_OPENED = getFilepath("doorOpened.png")
