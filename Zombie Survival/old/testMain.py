import pygame,sys
from pygame.locals import *
from classes import *
from squad import *

HUMANS = 4

pimage = pygame.image.load("images/humans/squad1_rifle.png")

bgimage = pygame.image.load("images/bg.png")
bgrect  = bgimage.get_rect()

player = Player(pimage,(100,100))
spectators = []
members    = []
activeProjectiles = []

for i in range(HUMANS):
    img = pygame.image.load("images/humans/squad"+str(i+2)+"_rifle.png")
    loc = (20,(i*40 + 20))
    spectators.append(Human(img,loc))  
    
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((1080,720), 1 | FULLSCREEN)

CLOCK = pygame.time.Clock()
FPS = 60

while 1:
    CLOCK.tick(FPS)
    pygame.display.flip()
    screen.blit(bgimage,bgrect)
    screen.blit(player.image,player.rect.center)
    
    #Event Catcher
    for event in pygame.event.get():
        if event.type==KEYDOWN:
                if (event.key==K_w)\
                   or (event.key==K_a)\
                   or (event.key==K_s)\
                   or (event.key==K_d):
                    player.move(event.key)

                elif event.key==K_ESCAPE:
                    sys.exit()
                    
                elif event.key==K_RETURN:
                    if len(spectators)>0:
                        member = (spectators.pop())
                        members.append(member)
                        player.squad.addMember(member)
                
                elif event.key==K_p:
                    print player.leadership
                    if len(player.squad.members)!=0:
                        print player.squad.members[0].tactics
                
                elif event.key==K_1:
                    player.squad.setFormation(SingleFile)
                elif event.key==K_2:
                    player.squad.setFormation(DoubleStaggered)
                elif event.key==K_3:
                    player.squad.setFormation(Wedge)
                elif event.key==K_4:
                    player.squad.setFormation(FiveStar)
                    
                elif event.key==K_RIGHTBRACKET:
                    if player.leadership<10:
                        player.leadership+=1
                elif event.key==K_LEFTBRACKET:
                    if player.leadership>1:
                        player.leadership-=1
                elif event.key==K_EQUALS:
                    if len(player.squad.members)!=0:
                        if player.squad.members[0].tactics<10:
                            for m in player.squad.members:
                                m.tactics+=1
                elif event.key==K_MINUS:
                    if len(player.squad.members)!=0:
                        if player.squad.members[0].tactics>1:
                            for m in player.squad.members:
                                m.tactics-=1
                    

        elif event.type==KEYUP:
            if (event.key==K_w)\
               or (event.key==K_a)\
               or (event.key==K_s)\
               or (event.key==K_d):
                player.stop(event.key)
                
        elif event.type==MOUSEBUTTONDOWN:
            if (pygame.time.get_ticks()-player.nextAttack>player.lastAttack) and pygame.time.get_ticks()>player.lastAttack:
                    player.shoot=True
                    if player.shoot==True:
                        (reloading,nextshot,projectiles) = player.attack(pygame.mouse.get_pos())
                        for proj in projectiles:
                            activeProjectiles.add(proj)
                        player.nextAttack=nextshot
                        player.lastAttack=pygame.time.get_ticks()
                        if reloading==True:
                            player.reloadingTimer=nextshot+pygame.time.get_ticks()
                    player.shoot=False
                        
    for s in spectators:
        screen.blit(s.image,s.rect.center)
        s.move()
        s.update()
        
    for m in members:
        screen.blit(m.image,m.rect.center)
        m.move()
        m.update()
        
    player.update()
                    
                    
                    
                    
                    
                    
                    
                    
                    