import pygame as pg
from config import *
from random import randint
from math import sqrt
from time import time


class Game_sprite(pg.sprite.Sprite):
    
    def __init__(self, image, x, y, w = None, h = None) -> None:
        super().__init__()
        self.image = (pg.image.load(image))
        if w and h:
            self.image = pg.transform.scale(self.image, (w,h))        
        self.rect  = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.h = self.rect.height
        self.w = self.rect.width
        self.c = (self.rect.x + self.w/2, self.rect.y + self.h/2 )

    def draw(self, scr):
        scr.blit(self.image, (self.rect.x, self.rect.y))
        

    

class Ship(Game_sprite):
    def __init__(self, image, x, y, w=None, h=None) -> None:
        super().__init__(image, x, y, w, h)
        self.speed = 10
        self.fire_wait = 0
        self.movex = ''
        self.movey = ''
        self.fire_wait = 0
    
    
    def update(self):
        if self.movey == 'down':
            self.rect.y += self.speed
            if self.rect.y +  self.h > WINDOWS_SIZE[1]: 
                self.rect.y = WINDOWS_SIZE[1] - self.h            
        elif self.movey == 'up':
            self.rect.y -= self.speed
            if self.rect.y < 0: self.rect.y = 0 
        if self.movex == 'right':
            self.rect.x += self.speed
            if self.rect.x + self.w > WINDOWS_SIZE[0]: 
                self.rect.x = WINDOWS_SIZE[0]-self.w
        elif self.movex == 'left':
            self.rect.x -= self.speed
            if self.rect.x < 0: 
                self.rect.x = 0   
        self.movex = ''
        self.movey = ''
        if self.fire_wait>0: self.fire_wait -= 1

    def fire(self,  fiers, sound, fire_wait):        
        if self.fire_wait == 0:
            fiers.add(Fire(self.rect.centerx, self.rect.top))                       
            self.fire_wait = fire_wait
            sound.play() # звук выстрела
            
        
        
        

class Alien(Game_sprite):
    def __init__(self, image, x, y, w=None, h=None, speed=1) -> None:
        super().__init__(image, x, y, w, h)        
        self.visible = True
        self.speed = speed
        self.x = x # свой х и у т.к. rect.x - округляет до целого
        self.y = y
    def update(self, ship):
        dx = ship.rect.x - self.x # вектор направдения на корабль
        dy = ship.rect.y - self.y
        dist = sqrt( dx**2 + dy**2 ) # дистанция до корабля       
        # dx = dx / dist * self.speed 
        # dy = dy / dist * self.speed        
        self.x += dx / dist * self.speed 
        self.y += dy / dist * self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        #self.draw(scr)
        
        
    def draw(self, scr):
        scr.blit(self.image, (self.x, self.y))

    



class Fire(Game_sprite):
    def __init__(self, x = 0, y = 0, w=None, h=None) -> None:
        super().__init__('pic\\fire2.png', x, y, w = None, h = None)
        self.rect.x -= self.w/2 # отступ на пол спрайта чтобы было посередине
        self.visible = False
        self.speed = 20
            
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
        


class Star(pg.sprite.Sprite):
    def __init__(self, full_y = False) -> None:
        super().__init__()
        self.r = randint(1,2)
        self.image =  pg.Surface((self.r*2,self.r*2), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, WINDOWS_SIZE[0])
        self.rect.y = 0 if not full_y else randint(1,WINDOWS_SIZE[1])
        self.speed = randint(1,5)        
        self.color = (255, 255, 255, 255)
        self.shine_speed = randint(10,100)
        self.shine_deep = randint(150,250)
        self.shine_revers = False
        self.shine_ok = randint(0,1)
    
    def update(self):
        pg.draw.circle(self.image, self.color, (self.r, self.r), self.r)
        self.rect.y += self.speed
        if self.rect.y > WINDOWS_SIZE[1]: self.kill()
        if self.shine_ok == 1: self.color = self.__shine()


    def __shine(self):
        # моргание звезд - зависит от shine_speed и shine_deep
        # которые создаются случайно для каждой звезды
        color = self.color[3]
        if self.shine_revers:
            color += self.shine_speed
            if color >= 255:
                color = 255
                self.shine_revers = False 
        else:
            color -= self.shine_speed
            if color <= 255 - self.shine_deep:
                color = 255 - self.shine_deep
                self.shine_revers = True
        return tuple(list(self.color)[0:3] + [color])



    