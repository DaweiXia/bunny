# 1 - Import Library
import pygame, math, random, os
from pygame.locals import *

# 2 - Initialize the game
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [100, 100]
acc = [0, 0]
arrows = []
badguyspos = [[640, 100]]
badtimer = 100

# 3 - Load images
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguy = pygame.image.load("resources/images/badguy.png")

# 4 - Keep looping through
while 1:
    # 5 - clear the screen before drawing it again
    screen.fill((255,0,255))

    # 6 - Draw the screen elements
    for i in range(0, width/grass.get_width()+1):
        for j in range(0, height/grass.get_height()+1):
            screen.blit(grass, (i*grass.get_width(), j*grass.get_height()))
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))
    
    # 6.1 - Set player position and rotation
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32),
                       position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2,
                  playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)
    
    # 6.2 - Move arrows
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

    # 6.3 - Generate badguys
    if badtimer == 0:
        badguyspos.append([640, random.randint(50, 430)])
        badtimer = random.randint(10, 100)   # Why 10: Avoid one bullet kill two badguys, which will cause an error.

    # 6.4 - Move badguys
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
                if badguypos not in removed_badguyspos:
                    removed_badguyspos.append(badguypos)
                if bullet not in removed_arrows:
                    removed_arrows.append(bullet)
                break
        if badguypos[0] < -64:
            removed_badguyspos.append(badguypos)
            continue

    # 6.5 - Draw arrows
    for bullet in removed_arrows:
        arrows.remove(bullet)

    for bullet in arrows:
        bulletrot = pygame.transform.rotate(arrow, 360-bullet[0]*57.29)
        screen.blit(bulletrot, (bullet[1], bullet[2]))

    # 6.6 - Draw badguys
    for badguypos in removed_badguyspos:
        badguyspos.remove(badguypos)
        
    for badguypos in badguyspos:
        screen.blit(badguy, badguypos)

    # 6.7 - Draw clock
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

    badtimer -= 1
