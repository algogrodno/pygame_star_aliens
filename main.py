from os import remove
import pygame as pg
from other import set_text
from sprites import *
from config import *
from other import *
from random import randint
from time import time
pg.init()

pg.display.set_caption("My game")
mw = pg.display.set_mode(WINDOWS_SIZE)
mw.fill(BACK_COLOR)
clock = pg.time.Clock()

background = pg.transform.scale(pg.image.load('pic\\fon1.jpg'),(WINDOWS_SIZE))
ship = Ship('pic\\starship2.png', WINDOWS_SIZE[0]/2,WINDOWS_SIZE[1]/2,70,100)

s_fon = pg.mixer.Sound('snd\\fon1.mp3')
s_fire = pg.mixer.Sound('snd\\fire1.mp3')
s_fon.play(-1)

starss = pg.sprite.Group()
fiers = pg.sprite.Group()
aliens = pg.sprite.Group()
for i in range(20): starss.add(Star(True))



fl = []
stars = []

aliens = []
play = True

key_wait = 0

SCORE = 0
TICKS = 0
ticks = 0
fps = 0
t = time()
while play:    
    mw.blit(background,(0,0))
    
    if TICKS % STAR_WAIT == 0:        
        starss.add(Star())
    starss.update()
    starss.draw(mw)

    for e in pg.event.get():
        # print(e)
        if e.type == pg.QUIT or \
                (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
            play  = False
        # if e.type == pg.KEYDOWN:
        #     if e.key == pg.K_UP:
        #         ship.sety(True)
    if pg.key.get_pressed()[pg.K_DOWN]:
        ship.sety(False)
    if pg.key.get_pressed()[pg.K_UP]:
        ship.sety(True)
    if pg.key.get_pressed()[pg.K_RIGHT]:
        ship.setx(True)
    if pg.key.get_pressed()[pg.K_LEFT]:
        ship.setx(False)
    if pg.key.get_pressed()[pg.K_2]:
        ship.speed += 1
    if pg.key.get_pressed()[pg.K_1]:
        ship.speed -= 1
    if pg.key.get_pressed()[pg.K_4]:
        FIRE_WAIT += 1
    if pg.key.get_pressed()[pg.K_3]:
        if FIRE_WAIT > 2:  FIRE_WAIT -= 1 
        else: FIRE_WAIT =  1
    if pg.key.get_pressed()[pg.K_5]:
        for alien in aliens:
            alien.speed += 1        
    if pg.key.get_pressed()[pg.K_6]:
        for alien in aliens:            
            if alien.speed > 2:  alien.speed -= 1 
            else: alien.speed =  1
    if pg.key.get_pressed()[pg.K_SPACE]:
        fl.append(Fire())
        fl[len(fl)-1].fire(ship, FIRE_WAIT, s_fire)    
    if pg.key.get_pressed()[pg.K_q]:
        
        aliens = alien_add(aliens, ship)
        alien_wait = 5
        
    if pg.key.get_pressed()[pg.K_a]:
        if key_wait == 0:
            ALIEN = not ALIEN
            key_wait = KEY_WAIT
        else:
            key_wait -= 1 
    
    

        
    
    
    if TICKS % NEW_ALIEN_WAIT == 0 :
        if ALIEN: aliens = alien_add(aliens, ship)
    
    for alien in aliens:
        if alien.visible: alien.update(mw, ship)
        else: aliens.remove(alien)
        
    
    for f in fl:
        if f.visible: f.update(mw)
        else: fl.remove(f)


    


    for f in fl:        
        for alien in aliens:
            if (f.y <= alien.y + alien.h and f.y > alien.y) and \
                    (f.x > alien.x and f.x + f.w < alien.x + alien.w) and \
                    alien.visible and f.visible:
                alien.visible = False
                f.visible = False
                SCORE += 1
                NEW_ALIEN_WAIT -=5 
                if NEW_ALIEN_WAIT <= 0 : NEW_ALIEN_WAIT = 3
                ALIEN_SPEED += 1

                
                

    ship.draw(mw)
    

    set_text(mw, f"Скорость - {ship.speed}", 30, (10,10))    
    set_text(mw, f"Огонь - {int(FIRE_WAIT)}", 30, (870,10))
    set_text(mw, int(ALIEN), 30, (960,680))
    set_text(mw, f"Чужих - {len(aliens)}", 30, (10,680))
    set_text(mw,f"ОЧКИ - {SCORE}", 40, (500,10))
    set_text(mw,f"звезд-{len(starss)}", 30, (500,680))
    
    t2 = time()
    if t2-t > 1:                        
        t = t2        
        fps = TICKS-ticks
        ticks = TICKS
    set_text(mw,f"fps-{fps}", 30, (700,680))


    pg.display.update()
    clock.tick(FPS)
    pg.event.pump()
    TICKS += 1

pg.quit()