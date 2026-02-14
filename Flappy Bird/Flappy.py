import pygame
import random
from pygame.locals import*
pygame.init()
screen=pygame.display.set_mode((864,768))
clock=pygame.time.Clock()
framer=60
pygame.display.set_caption("Flappy Bird")
font=pygame.font.SysFont("Merlin",50)
#gaming variable
gscroll=0
scrspe=5
fly=False
gameo=False
pipegap=160
pifreq=2000
score=0
pipepass=False
lastpigen=pygame.time.get_ticks()-pifreq
#loading the images
bgload=pygame.image.load("bg.png")
groload=pygame.image.load("ground.png")
resload=pygame.image.load("restart.png")
#function for text
def text(txt,font,txtcol,x,y):
    txthold=font.render(txt,True,txtcol)
    screen.blit(txthold,(x,y))
#class for bird
class bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.birdimgs=[]
        self.index=0
        self.countingbirds=0
        #loading bird images
        for i in range(1,4):
            birdload=pygame.image.load(f"bird{i}.png")
            self.birdimgs.append(birdload)
        self.image=self.birdimgs[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vertspe=0
        self.clicked=False
    #update function
    def update(self):
        global fly,gameo
        if fly==True:
            self.vertspe+=0.1
            if self.vertspe>3:
                self.vertspe=3
            if self.rect.bottom<768:
                self.rect.y+=int(self.vertspe)
        #jumping of flappy
        if gameo==False:
            if pygame.mouse.get_pressed()[0]==1 and not self.clicked:
                self.clicked=True
                self.vertspe=-5
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False
            #bird animation
            flapcooldown=25
            self.countingbirds+=1
            if self.countingbirds>flapcooldown:
                self.countingbirds=0
                self.index+=1
                if self.index>=3:
                    self.index=0
                self.image=self.birdimgs[self.index]
            self.image=pygame.transform.rotate(self.birdimgs[self.index],self.vertspe *-2)
        else:
            self.image=pygame.transform.rotate(self.birdimgs[self.index],-90)
class pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        super().__init__()
        self.image=pygame.image.load("pipe.png")
        self.rect=self.image.get_rect()
        if pos==1:#top
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=(x,y-int(pipegap // 2))
        elif pos==2:#bottom
            self.rect.topleft=(x,y+int(pipegap // 2))
    def update(self):
            self.rect.x-=scrspe
            if self.rect.x<=0:
                self.kill()
#bird object
birdobj=bird(100,384)
birdgrp=pygame.sprite.Group()
birdgrp.add(birdobj)
#pipe group
pipegrp=pygame.sprite.Group()
#while loop
run=True
while run:
    clock.tick(framer)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==MOUSEBUTTONDOWN and not fly and not gameo:
            fly=True
    screen.blit(bgload,(0,0))
    birdgrp.draw(screen)
    birdgrp.update()
    pipegrp.draw(screen)
    screen.blit(groload,(gscroll,600))
    #scoring
    if len(pipegrp)>0:
        bird1=birdgrp.sprites()[0] 
        first_pipe=pipegrp.sprites()[0]
        if bird1.rect.left>first_pipe.rect.left and bird1.rect.right<first_pipe.rect.right and not pipepass:
            pipepass=True
        if pipepass and bird1.rect.left>first_pipe.rect.right:
            score+=1
            print(score)
            pipepass=False
    text(str(score),font,"red",20,20)

    gscroll-=scrspe
    if abs(gscroll)>37:
        gscroll=0
    #pipe collision
    if pygame.sprite.groupcollide(birdgrp,pipegrp,False,False) or birdobj.rect.top<0 or birdobj.rect.bottom>600:
        gameo=True
    #pipe generation
    if fly and not gameo:
        curtime=pygame.time.get_ticks()
        if curtime-lastpigen>pifreq:
            pipeheight=random.randint(-150,150)
            botpipe=pipe(864,384+pipeheight,2)
            topipe=pipe(864,384+pipeheight,1)
            pipegrp.add(botpipe)
            pipegrp.add(topipe)
            lastpigen=curtime
        pipegrp.update()
    pygame.display.update()
pygame.quit()
