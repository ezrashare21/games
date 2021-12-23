#mindsweeper

from pygame.locals import *
import pygame, sys, random

pygame.init()

size = 10
screen = pygame.display.set_mode((size*20,size*20))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial",16)
pygame.display.set_caption("Minesweeper")

ro = [[-1,0],[1,0],[1,1],[-1,-1],[-1,1],[1,-1],[0,1],[0,-1]]
colors = [(125, 125, 125),(159, 159, 159),(23, 45, 191),(125,125,125)]
colormap = {
    "tile": 0,
    "mined": 1,
    "flag": 2,
    "mine": 3
}
grid,mgrid = [],{}
for x in range(size*size): grid.append(0)
for x in range(size-1): grid.append(0)

def index(x,y):
    return (x + (y * size))
x,y = -1,0
for t in grid:
    x += 1
    if x > size:
        x = 0
        y += 1
    mgrid[(x,y)] = index(x,y)







def rpos():
    return (random.randint(0,size-1),random.randint(0,size-1))

stack = []
for x in range(10):
    pos = rpos()
    while pos in stack:
        pos = rpos()
    stack.append(pos)
    grid[mgrid[pos]] = colormap["mine"]

def amount_of_mines(x,y):
    a = 0
    for v in ro:
        p = (x+v[0],y+v[1])
        if p in mgrid:
            if grid[mgrid[p]] == colormap["mine"]:
                a += 1
    return a

while True:
    mpos = pygame.mouse.get_pos()
    mpos = (mpos[0]-10,mpos[1]-10)
    mpos = (round(mpos[0]/20),round(mpos[1]/20))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if colormap["mine"] == grid[mgrid[mpos]]:
                print("your city exploded. :(")
                pygame.quit()
                sys.exit()
            elif colormap["tile"] == grid[mgrid[mpos]]:
                grid[mgrid[mpos]] = colormap["mined"]
        if event.type == KEYDOWN:
            if event.key == K_LSHIFT:
                if grid[mgrid[mpos]] == colormap["mine"]:
                    grid[mgrid[mpos]] = colormap["flag"]
                else:
                    print("your city was too scared to pick the untouched square of land.")
                    pygame.quit()
                    sys.exit()
    screen.fill((93, 143, 101))
    
    for e in mgrid:
        text = font.render(str(amount_of_mines(e[0],e[1])),False,(255,0,0))
        rect = pygame.Rect((e[0]*20,e[1]*20),(19,19))
        pygame.draw.rect(screen,colors[grid[mgrid[e]]],rect)
        if grid[mgrid[e]] == colormap["mined"]:
            screen.blit(text,(rect.x+2,rect.y+2))
    
    if not 0 in grid:
        print("YOU WIN!!!!!!! (nothing is a undug tile)")
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    clock.tick(60)