import driver,pygame,classes,gameWorld
d = driver.Driver()

HUMANS = 4

for i in range(HUMANS):
    img = pygame.image.load("images/humans/squad"+str(i+2)+"_rifle.png")
    loc = (60,(i*40 + 60))
    human = classes.Human(img,loc)
    d.gameWorld.player.squad.addMember(human)
    d.gameWorld.activeHumans.add(human)  
    
while 1:
    d.mainLoop()
    