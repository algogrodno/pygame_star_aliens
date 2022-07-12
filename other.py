import pygame as pg
from sprites import Star
from random import randint
from config import *
from math import sqrt
from sprites import Alien

def set_text(scr, text, size = 10, pos = (0,0), color = (255,255,55)):
    font = pg.font.Font(None, size)
    text_pic = font.render(str(text), True, color)
    scr.blit(text_pic,pos)




def alien_add(aliens, ship):
    dist = 0
    # while dist<200:
    x = randint(-300, WINDOWS_SIZE[0]+300)                         
    y = randint(1, WINDOWS_SIZE[1])
        # dx = ship.x - x
        # dy = ship.y - y
        # dist = sqrt( dx**2 + dy**2 )
        
    # l = randint(1,4) 
    # if l == 1: y = -90
    # elif l == 2: x = WINDOWS_SIZE[0] + 100
    # elif l == 3: y = WINDOWS_SIZE[1] + 90
    # else: x = -100
    y = -100
    aliens.append(Alien('pic\\starship4.png', x, y, 100,90))
    return aliens
