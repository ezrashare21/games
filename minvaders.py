"""
controls:
left - a
right - d
up - w
down - s
A - .
B - ,
"""

import thumby, random

games = 0
lives = 3
lost = False

def gamel():
    # BITMAP: width: 7, height: 7
    bitmap4 = [56,69,86,68,86,69,56]
    
    # BITMAP: width: 8, height: 6
    player = [48,56,56,63,63,56,56,48]
    
    hurtb = []
    timer = 0
    k = 0
    bulletreg = []
    bullet = None
    states = []
    invspeed = 0.005
    invoffsetf = 1
    def cpoint(box,point):
        px = point[0]
        py = point[1]
        return box[0] < px and box[1] < py and box[2] > px and box[3] > py
    playerx = round(thumby.DISPLAY_W/2)
    for x in range(7*3): states.append(games)
    
    def ndex(x,y,width):
        return x+(y*width)
    def invader(x,y,key):
        thumby.display.blit(bitmap4, x, y, 7, 7, key)
    while(1):
        timer += 1
        thumby.display.fill(0)
        invoffsetf += invspeed
        invoffset = round(invoffsetf)
        thumby.display.blit(player,round(playerx),30,8,6,-1)
        
        if playerx > thumby.DISPLAY_W: playerx = -8
        if playerx < -8: playerx = thumby.DISPLAY_W
        if thumby.buttonL.pressed(): playerx -= 1.2
        if thumby.buttonR.pressed(): playerx += 1.2
        if thumby.buttonA.pressed() and bullet == None: bullet = [round(playerx)+4,26]
        if timer > 50-(games+(k/8)):
            timer = 0
            bulletreg.append((random.randint(0,6),random.randint(0,2)))
        
        while len(bulletreg)!=0:
            newbull = bulletreg.pop()
            if states[ndex(newbull[0],newbull[1],7)] != 0:
                hurtb.append([(newbull[0]*8)+invoffset,newbull[1]*8])
        
        for x in range(len(hurtb)):
            hurtb[x][1] += 1
        
        playerbox = (round(playerx),30,round(playerx)+8,30+6)
        
        for x in hurtb:
            thumby.display.setPixel(x[0],x[1],1)
            if cpoint(playerbox,x):
                return "lost"
        
        statesn = -1
        for x in range(7):
            for y in range(3):
                statesn += 1
                if states[statesn] != 0:
                    invader((x*8)+invoffset,y*8,-1)
                    if bullet != None:
                        box = ((x*8)+invoffset,y*8,8+((x*8)+invoffset),8+(y*8))
                        if cpoint(box,bullet):
                            states[statesn] -= 1
                            bullet = None
                            d = invspeed < 0
                            if d: invspeed = -invspeed
                            invspeed += 0.04
                            if d: invspeed = -invspeed
                            if states[statesn] == 0:
                                k += 1
        if k == len(states):
            return 0
        if ((x*9)+invoffset)+2 > thumby.DISPLAY_W:
            invspeed = -invspeed
        if invoffset < 1:
            invspeed = -invspeed
        
        if bullet != None:
            bullet[1] -= 1
            thumby.display.setPixel(bullet[0],bullet[1], 1)
            if bullet[1] < 0: bullet = None
        
        thumby.display.update()

while True:
    thumby.display.fill(0)
    thumby.display.drawText("minvaders",1 , 4, 1)
    thumby.display.drawText("press A",1 , 30, 1)
    thumby.display.blit([56,69,86,68,86,69,56],10,20,7,7)
    thumby.display.blit([56,69,86,68,86,69,56],10+(1*10),20,7,7)
    thumby.display.blit([56,69,86,68,86,69,56],10+(2*10),20,7,7)
    thumby.display.blit([56,69,86,68,86,69,56],10+(3*10),20,7,7)
    thumby.display.blit([56,69,86,68,86,69,56],10+(4*10),20,7,7)
    thumby.display.blit([56,69,86,68,86,69,56],10+(5*10),20,7,7)
    if thumby.buttonA.justPressed(): break
    thumby.display.update()
while True:
    games += 1
    if gamel() == "lost":
        lives -= 1
        games -= 1
    if lives == 0:
        break
while True:
    thumby.display.fill(0)
    thumby.display.update()