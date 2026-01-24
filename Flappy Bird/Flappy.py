import pygame
import random
from pygame.locals import*
pygame.init()
screen=pygame.display.set_mode((864,768))
clock=pygame.time.Clock()
framer=60
pygame.display.set_caption("Flappy Bird")
font=pygame.font.SysFont("Merlin",30)
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
        self.img=self.birdimgs[self.index]
        self.rect=self.image.get_rect()
        self.rect.centre=[x,y]
        self.vertspe=0
        self.clicked=False
    #update function
    def update(self):
        global fly,gameo
        if fly==True:
            self.vertspe+=0.8
            if self.vertspe>6:
                self.vertspe=6
            if self.rect.bottom<768:
                self.rect.y+=int(self.vertspe)
        #jumping of flappy
        if gameo==False:
            if pygame.mouse.get_pressed()[0]==1 and not self.clicked:
                self.clicked=True
                self.vertspe=-10
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False
            #bird animation
            flapcooldown=6
            self.countingbirds+=1
            
#while loop
run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    screen.blit(bgload,(0,0))
    pygame.display.update()
pygame.quit()