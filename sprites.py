import pygame as pg
from config import *
from random import randint
from math import sqrt

class Game_sprite(pg.sprite.Sprite):
    
    def __init__(self, image, x, y, w = None, h = None) -> None:
        super().__init__()
        self.image = (pg.image.load(image))
        if w and h:
            self.image = pg.transform.scale(self.image, (w,h))
        # self.image = self.image.subsurface((30,30,30,30))
        self.rect  = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.h = self.image.get_rect().height
        self.w = self.image.get_rect().width
        self.c = (self.rect.x + self.w/2, self.rect.y + self.h/2 )

    def draw(self, scr):
        scr.blit(self.image, (self.rect.x, self.rect.y))
        

    

class Ship(Game_sprite):
    def __init__(self, image, x, y, w=None, h=None) -> None:
        super().__init__(image, x, y, w, h)
        self.speed = 10
        self.fire_wait = 0
    def sety(self, up = None):
        if not up:
            self.rect.y += self.speed
            if self.rect.y +  self.h > WINDOWS_SIZE[1]: 
                self.rect.y = WINDOWS_SIZE[1] - self.h
            
        else:
            self.rect.y -= self.speed
            if self.rect.y < 0: self.rect.y = 0 

    def setx(self, right: bool): 
        if right:
            self.rect.x += self.speed
            if self.rect.x + self.w > WINDOWS_SIZE[0]: 
                self.rect.x = WINDOWS_SIZE[0]-self.w
        else:
            self.rect.x -= self.speed
            if self.rect.x < 0: 
                self.rect.x = 0   
                
    def draw(self, scr):
        super().draw(scr)
        if self.fire_wait>0: self.fire_wait -= 1

class Alien(Game_sprite):
    
    
    
    def __init__(self, image, x, y, w=None, h=None) -> None:
        super().__init__(image, x, y, w, h)
        #self.cours = self.get_cours()        
        self.visible = True
        self.speed = 1

    def update(self, scr, ship):        
        #dx = self.cours[0] - self.c[0]
        #dy = self.cours[1] - self.c[1]
        dx = ship.rect.x - self.rect.x
        dy = ship.rect.y - self.rect.y
        dist = sqrt( dx**2 + dy**2 )        
        dx /= dist
        dy /= dist
        dx *= self.speed
        dy *= self.speed
        self.rect.x += dx
        self.rect.y += dy
        self.draw(scr)
        
        #if dist<10: self.cours = self.get_cours()

        

    # def check_cours(self):
    #     dist = sqrt( (self.cours[0] - self.c[0])**2 + (self.cours[1] - self.c[1])**2 )
    #     if dist<5: self.cours = self.get_cours()

    # def get_cours(self):
    #     return (randint(0, WINDOWS_SIZE[0]), randint(0, WINDOWS_SIZE[1]))
    
    



class Fire(Game_sprite):
    def __init__(self, x = 0, y = 0, w=None, h=None) -> None:
        super().__init__('pic\\fire2.png', x, y, w = None, h = None)
        self.visible = False
        self.speed = 20
        
    
    def fire(self, ship, fw, s_fire):
        if ship.fire_wait == 0:
            self.x = ship.x + ship.w / 2 - self.w / 2
            self.y = ship.y
            self.visible = True
            ship.fire_wait = fw
            s_fire.play()
        
            
    
    def update(self, scr):
        self.y -= self.speed
        if self.y + self.h < 0:
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



    