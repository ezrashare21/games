from pygame.locals import *
import pygame, sys, json, os

pygame.init()

lifesize = 10
font = pygame.font.SysFont("arial",15)
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
life = {
    (20,20): None,
    (20,21): None,
    (20,19): None,
    (21,19): None,
    (19,20): None
}
newlife = {}
ro = [[-1,0],[1,0],[1,1],[-1,-1],[-1,1],[1,-1],[0,1],[0,-1]]

lsize_speed = 0

def getpop(x,y):
    p = 0
    for t in ro:
        if (x+t[0],y+t[1]) in life: p+=1
    return p

def runsim(x,y):
    population = getpop(x,y)
    if (x,y) in life:
        if population == 2 or population == 3: newlife[(x,y)] = None
        else: pass
    else:
        if population == 3: newlife[(x,y)] = None

timer = 0
edit = False

pygame.display.set_caption("Conway's Game of Life (clone by ezrashare21)")

def drawLife():
    for x in life:
            rect = pygame.Rect((x[0]*lifesize)+scrollx,(x[1]*lifesize)+scrolly,lifesize,lifesize)
            pygame.draw.rect(surface=screen,color=(0,0,0),rect=rect)

pressed = [False,False,False,False,False,False]
Rect = pygame.Rect
DRect = pygame.draw.rect
Fill = screen.fill
scrollx,ssx = 0,0
scrolly,ssy = 0,0
while True:
    timer += 1
    mpos = list(pygame.mouse.get_pos())
    mpos[0] += scrollx
    mpos[1] += scrolly
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_r:
                life = {}
                newlife = {}
            if event.key == K_SPACE:
                edit = not edit
            if event.key == K_p:
                life = {
                    (20,20): None,
                    (20,21): None,
                    (20,19): None,
                    (21,19): None,
                    (19,20): None
                }
                newlife = {}
            if event.key == K_k:
                try: open("congamelife_save.json","x")
                except:pass
                l = []
                for x in life:
                    l.append(str(x[0]))
                    l.append(str(x[1]))
                file = open("congamelife_save.json","w").write(" ".join(l))
                print("saved!")
            if event.key == K_l:
                l,b,life,x,y,d = (open("congamelife_save.json").read()).split(" "),False,{},0,0,0
                for z in l:
                    d += 1
                    b = not b
                    if b:
                        if d > 1: life[x,y] = None
                        x = int(z)
                    else: y = int(z)
                newlife = {}
                print("loaded!")
            if event.key == K_a: pressed[0] = True
            if event.key == K_d: pressed[1] = True
            if event.key == K_w: pressed[2] = True
            if event.key == K_s: pressed[3] = True
            if event.key == K_q: pressed[4] = True
            if event.key == K_e: pressed[5] = True
        if event.type == KEYUP:
            if event.key == K_a: pressed[0] = False
            if event.key == K_d: pressed[1] = False
            if event.key == K_w: pressed[2] = False
            if event.key == K_s: pressed[3] = False
            if event.key == K_q: pressed[4] = False
            if event.key == K_e: pressed[5] = False
        if event.type == MOUSEBUTTONDOWN:
            mx = round((mpos[0]-(scrollx*2))/lifesize)
            my = round((mpos[1]-(scrolly*2))/lifesize)
            coord = (mx,my)
            if coord in life:
                del life[coord]
            else:
                life[coord] = None
    if pressed[0]: ssx += 2
    if pressed[1]: ssx -= 2
    if pressed[2]: ssy += 2
    if pressed[3]: ssy -= 2
    if pressed[4]: lsize_speed += 0.1
    if pressed[5]: lsize_speed -= 0.1
    scrollx += ssx
    scrolly += ssy
    
    #lsize mangagment
    lifesize += lsize_speed
    
    ssx *= 0.8
    ssy *= 0.8
    lsize_speed *= 0.8
    if edit:
        screen.fill((200,200,200))
        timer = 0
        drawLife()
    if not edit:
        Fill((255,255,255))
        
        runs = timer > 3
        
        stack = []
        if runs: newlife = {}
        for x in life:
            rect = Rect((x[0]*lifesize)+scrollx,(x[1]*lifesize)+scrolly,lifesize,lifesize)
            DRect(surface=screen,color=(0,0,0),rect=rect)
            if runs:
                timer = 0
                runsim(x[0],x[1])
                for ad in ro:
                    nx = x[0] + ad[0]
                    ny = x[1] + ad[1]
                    if not (nx,ny) in stack:
                        stack.append((nx,ny))
                        runsim(nx,ny)
        if runs: life = dict(newlife)
    fps = round(clock.get_fps())
    fps_texture = font.render(str(fps),False,(0,0,0))
    screen.blit(fps_texture,(0,0))
    
    pygame.display.update()
    clock.tick(60)