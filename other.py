import pygame as pg
#from sprites import Star
from random import randint
from config import *
#from math import sqrt
from sprites import Alien

def set_text(scr, text, size = 10, pos = (0,0), color = (255,255,55)):
    font = pg.font.Font(None, size)
    text_pic = font.render(str(text), True, color)
    scr.blit(text_pic,pos)




def alien_add(aliens, speed):      
    x = randint(-200, WINDOWS_SIZE[0]+200) 
    y = -100
    aliens.add(Alien('pic\\starship4.png', x, y, 100,90, speed))
    return aliens

def game_over(scr):
    background = pg.transform.scale(pg.image.load('pic\\game_over.jpg'),(WINDOWS_SIZE))
    scr.blit(background,(0,0))