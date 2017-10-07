import pygame, sys, random
from pygame.locals import *
pygame.init()
pygame.display.init()
# Intialize global variable
window_height = 600
window_width = 1200
level = 0
fps = 25
black = (0,0,0)
white = (255,255,255)
canvas = pygame.display.set_mode((window_width,window_height))
addnewflamerate = 12
######
class dragon:
    global firerect, imagerect, canvas
    up = False
    down = True
    velocity = 15
    def __init__(self):
        self.image = pygame.image.load("dragon.png")
        self.imagerect = self.image.get_rect()
        self.imagerect.bottom = firerect.top
        self.imagerect.right = 1200
        canvas.blit(self.image,self.imagerect)
##
    def update(self):
        if(self.imagerect.top < cactusrect.bottom):
            self.down = True
            self.up = False
        if(self.imagerect.bottom > firerect.top):
            self.up = True
            self.down = False
        if(self.down):
            self.imagerect.bottom += self.velocity
        if(self.up):
            self.imagerect.top -= self.velocity
        canvas.blit(self.image,self.imagerect)
#
    def return_height(self):
       return self.imagerect.top;
## FLAMES
class flames:
    flamespeed = 20
    def __init__(self, height):
        self.image = pygame.image.load("fireball.png")
        self.imagerect = self.image.get_rect()
        self.imagerect.top = height
        self.imagerect.right = 1200
    def update(self):
        self.imagerect.left -= self.flamespeed
        #canvas.blit(self.image, self.imagerect)
    def collision(self):
        if self.imagerect.left <= 0:
            return True
        return False

## MARYO
class maryo:
    global moveup,movedown,gravity,cactusrect,firerect
    speed = 10
    downspeed = 20
    def __init__(self):
        self.image = pygame.image.load("maryo.png")
        self.imagerect = self.image.get_rect()
        self.imagerect.topleft = (50, 300)
        self.score = 0
        gravity = True
    def update(self):
        if(moveup and (self.imagerect.top > cactusrect.bottom )):
            self.imagerect.top -= self.speed
            self.score += 1
        elif(movedown and (self.imagerect.bottom <firerect.top)):
            self.score += 1
            self.imagerect.bottom += self.downspeed
        elif(gravity and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.speed
def terminate():
    pygame.quit()
    sys.exit()
#
def waitforkey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

def flamehitsmariyo(playrect, flames):
     for f in flames:
        if f.imagerect.bottom >= playrect.top and f.imagerect.top <= playrect.bottom:
            if f.imagerect.right >= playrect.left and f.imagerect.left <= playrect.right:
                return True
            return False
        return False
def drawtext(text, font, surface,x,y):
    textobj = font.render(text,1,white)
    textrect = textobj.get_rect()
    textrect.left = x
    textrect.top = y
    surface.blit(textobj, textrect)

def check_level(score):
    global window_height, level, cactusrect, firerect
    if score in range(0,250):
        level = 1
        cactusrect.centerx = 600
        cactusrect.centery = -48
        firerect.centerx = 600
        firerect.centery = 650
    elif score in range(250,500):
        level = 2
        cactusrect.centerx = 600
        cactusrect.centery = 0
        firerect.centerx = 600
        firerect.centery = 600
    elif score in range(500,750):
        level = 3
        cactusrect.centerx = 600
        cactusrect.centery = 50
        firerect.centerx = 600
        firerect.centery = 550
    elif score in range(750,1000):
        level = 4
        cactusrect.centerx = 600
        cactusrect.centery = 90
        firerect.centerx = 600
        firerect.centery = 510
        

def load_image(imagename):
    image = pygame.image.load(imagename)
    return image

#resource handling
font = pygame.font.SysFont(None, 40, False, True)
scorefont = pygame.font.SysFont(None, 40, False, True)

fireimage = load_image("fire_bricks.png")
firerect = fireimage.get_rect()
cactusimage = load_image("cactus_bricks.png")
cactusrect = cactusimage.get_rect()

startimage = load_image("start.png")
startimagerect = startimage.get_rect()
startimagerect.centerx = 600
startimagerect.centery = 300

endimage = load_image("end.png")
endimagerect = endimage.get_rect()
endimagerect.centerx = 600
endimagerect.centery = 300

#playback music
playback = pygame.mixer.music.load('mario_theme.wav')
gameover = pygame.mixer.Sound('mario_dies.wav')
#game over music
#Start screen..
#pygame.display.set_caption('MARYO')
drawtext('Mario',font,canvas,(window_width/3),(window_height/3))
canvas.blit(startimage,startimagerect)
pygame.display.update()

#initialize

waitforkey()
topscore = 0
Dragon = dragon()

while True:
    flame_list = []
    player = maryo()
    moveup = movedown = gravity = False
    flameaddcounter = 0
    gameover.stop()
    pygame.mixer.music.play(-1,0.0) #play the music
    pygame.display.update()

#Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    moveup = True
                    movedown = False
                    gravity = False
                    player.update()
                if event.key == K_DOWN:
                    moveup = False
                    movedown = True
                    gravity = False
                    player.update()

            if event.type == KEYUP:
                if event.key == K_UP:
                    moveup = False
                    gravity = True
                    player.update()
                if event.key == K_DOWN:
                    movedown = False
                    gravity = True
                    player.update()
                if event.key == K_ESCAPE:
                    terminate()
        flameaddcounter += 1
        check_level (player.score)

        if flameaddcounter == addnewflamerate: #to create flame
            flameaddcounter = 0
            newflame = flames(Dragon.return_height())
            flame_list.append(newflame)

        for f in flame_list:
            flames.update(f)## f.update()
        
        for f in flame_list:
            if(f.collision() == True):
                flame_list.remove(f)

        player.update()
        Dragon.update()

        canvas.fill(black)
        canvas.blit(fireimage, firerect)
        canvas.blit(cactusimage, cactusrect)
        canvas.blit(player.image, player.imagerect)
        canvas.blit(Dragon.image, Dragon.imagerect)

        drawtext('Score : %s | Top Score : %s | Level : %s' %(player.score, topscore, level
             ),scorefont,canvas,350,cactusrect.bottom+10)
        for f in flame_list:
            f.surface = pygame.transform.scale(f.image, (25,25))
            canvas.blit(f.surface, f.imagerect)
        if flamehitsmariyo(player.imagerect, flame_list): # collision with flame
            if player.score > topscore:
                topscore = player.score
                break
            break
        if player.imagerect.bottom >= firerect.top or player.imagerect.top <= cactusrect.bottom:
            if player.score > topscore:
                topscore = player.score
                break
            break
        pygame.display.update()
        mainClock = pygame.time.Clock()
        mainClock.tick(fps)

    #play game over
    canvas.blit(endimage,endimagerect)
    pygame.mixer.music.stop()
    gameover.play()
    pygame.display.update() #end image
    waitforkey()
