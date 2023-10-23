import pygame as pg
from config import *
from random import randint
from math import sqrt
from time import time


class Game_sprite(pg.sprite.Sprite):    
    def __init__(self, image = None, x = 0, y = 0, w = None, h = None) -> None:
        super().__init__()        
        self.image = (pg.image.load(image)) if image else None        
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
        self.image_orig = self.image
        self.type = randint(1,3)
        self.visible = True
        self.speed = speed
        self.x = x # свой х и у т.к. rect.x - округляет до целого
        self.y = y # а для подсчета направления по вектору нужны дроби
        
        #для вращения
        #self.rotate = randint(-10, 10)        
        self.angle_rotate = randint(-15, 15) # для постоянного вращения
        self.angle_max = randint(1,20)
        self.angle_min = -self.angle_max        
        self.angle = randint(self.angle_min, self.angle_max)
        self.angle_step = 1 if self.angle >= 0 else -1
    
    def update(self, ship):
        dx, dy = ship.rect.x - self.x, ship.rect.y - self.y # вектор направдения на корабль        
        dist = sqrt( dx**2 + dy**2 ) # дистанция до корабля       
        # dx = dx / dist * self.speed 
        # dy = dy / dist * self.speed        
        self.x += dx / dist * self.speed 
        self.y += dy / dist * self.speed
        self.rect.x = self.x
        self.rect.y = self.y

        self.spr_rotate_back()
    
    def spr_rotate(self, angle):
        '''поворачивает спрайт на установленный градус'''        
        # создаем каждый раз новую каритнку из оригинала
        # т.к. если поворачивать оригинал будет сильное искажение        
        self.image = pg.transform.rotate(self.image_orig, angle)
        self.rect_r = self.image.get_rect()
        # приравниваем кординады новой картинки у позиции данного спрайта
        self.rect_r.x = self.rect.x
        self.rect_r.y = self.rect.y
        # ищем на сколько отличается центр новой картинки
        w_delta = self.rect_r.center[0] - self.rect.center[0]
        h_delta = self.rect_r.center[1] - self.rect.center[1]
        # и смещаем коринаты ровно на столько
        self.rect.x -= w_delta
        self.rect.y -= h_delta
        
        

    def spr_rotate_normal(self):
        '''        
        производит вращение всегда в одну сторону
        на за ранее установленный градус (self.angle_rotate)
        '''
        self.spr_rotate(self.angle)
        self.angle = (self.angle + self.angle_rotate)%360

    def spr_rotate_back(self):
        '''   вращение  вперед и обратно    '''
        self.spr_rotate(self.angle)
        if abs(self.angle) > self.angle_max:
            self.angle_step *= -1
        self.angle += self.angle_step
        #print(self.angle)




    



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



class Boom(pg.sprite.Sprite):
    def __init__(self, ufo_center, boom_sprites, booms) -> None:
        super().__init__() 
        #global booms, boom_sprites              
        self.frames = boom_sprites
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = boom_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = ufo_center
        self.add(booms)
    
    def update(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1
        if self.frame_num == len(self.frames)-1:
            self.kill()


class Star(pg.sprite.Sprite):
    def __init__(self, full_y = False) -> None:
        super().__init__()
        self.r = randint(1,3)
        self.image =  pg.Surface((self.r*2,self.r*2), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, WINDOWS_SIZE[0])
        self.rect.y = 0 if not full_y else randint(1,WINDOWS_SIZE[1])
        self.speed = randint(3,10)        
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



