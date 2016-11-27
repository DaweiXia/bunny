# 1 - Import Library
import pygame, math, random, os
from pygame.locals import *

# 2 - Initialize the game
pygame.init()
pygame.mixer.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [100, 100]
acc = [0, 0]
arrows = []
badguyspos = [[640, 100]]
badtimer = 100
healthvalue = 194

# 3.1 - Load images
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguy = pygame.image.load("resources/images/badguy.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# 3.2 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load("resources/audio/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 4 - Keep looping through
running, exitcode = 1, 0
while running:
    # 5 - clear the screen before drawing it again
    screen.fill((255,0,255))

    # 6.0 - Draw grass
    for i in range(0, width/grass.get_width()+1):
        for j in range(0, height/grass.get_height()+1):
            screen.blit(grass, (i*grass.get_width(), j*grass.get_height()))

    # 6.2 - Draw castle
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))
        
    # 6.3 - Set player position and rotation then draw player
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32),
                       position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2,
                  playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)
    
    # 6.4 - Move arrows
    removed_arrows = []
    for bullet in arrows:
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1] += velx
        bullet[2] += vely
        if (bullet[1] < -64 or bullet[1] > 640 or
            bullet[2] < -64 or bullet[2] > 480):
            if bullet not in removed_arrows:
                removed_arrows.append(bullet)

    # 6.5 - Generate badguys at suitable positiona with suitable frequency
    if badtimer == 0:
        badguyspos.append([640, random.randint(50, 430)])
        badtimer = random.randint(10, 100)   # Why 10: Avoid one bullet kill two badguys, which will cause an error.

    # 6.6 - Move badguys
    removed_badguyspos = []
    for badguypos in badguyspos:
        badguypos[0] -= 7
        badrect = pygame.Rect(badguy.get_rect())
        badrect.left = badguypos[0]
        badrect.top = badguypos[1]
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                acc[0] += 1
                if badguypos not in removed_badguyspos:
                    removed_badguyspos.append(badguypos)
                if bullet not in removed_arrows:
                    removed_arrows.append(bullet)
                break
        if badguypos[0] < 64:
            healthvalue -= random.randint(5,20)
            removed_badguyspos.append(badguypos)
            continue

    # 6.7 - Draw arrows
    for bullet in removed_arrows:
        arrows.remove(bullet)

    for bullet in arrows:
        bulletrot = pygame.transform.rotate(arrow, 360-bullet[0]*57.29)
        screen.blit(bulletrot, (bullet[1], bullet[2]))

    # 6.8 - Draw badguys
    for badguypos in removed_badguyspos:
        badguyspos.remove(badguypos)
        
    for badguypos in badguyspos:
        screen.blit(badguy, badguypos)

    # 6.9 - Draw healthbar
    screen.blit(healthbar, (5,5))
    for index in range(healthvalue):
        screen.blit(health, (index+8,8))

    # 6.10 - Draw clock
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(str(pygame.time.get_ticks()/60000)+":"+
                               str(pygame.time.get_ticks()/1000%60).zfill(2),
                               True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedtext, textRect)

    # 7 - Update the screen
    pygame.display.flip()

    # 8 - Loop through the events
    for event in pygame.event.get():

        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            dy = position[1] - (playerpos1[1] + playerrot.get_rect().height/2)
            dx = position[0] - (playerpos1[0] + playerrot.get_rect().width/2)
            acc[1] += 1
            arrows.append([math.atan2(dy, dx),
                           playerpos1[0]+playerrot.get_rect().width/2,
                           playerpos1[1]+playerrot.get_rect().height/2])
    # 9 - Move player
    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    if keys[1]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5

    # 10 - Update badtimer
    badtimer -= 1

    # 11 - Win/Lose check
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 0
    if healthvalue <= 0:
        running = 0
        exitcode = 1
    if acc[1] != 0:
        accuracy = acc[0] * 1.0 / acc[1] * 100
    else:
        accuracy = 0

# 12 - Win/Lose display
if exitcode == 1:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(accuracy) + "%", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(text, textRect)
    screen.blit(gameover, (0,0))
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(accuracy) + "%", True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(text, textRect)
    screen.blit(youwin, (0,0))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
