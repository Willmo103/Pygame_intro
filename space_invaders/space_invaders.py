import math
import pygame, random

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

#events are anything happening inside your window including the closing x button pressed
# x button is pygame.QUIT

# title and Icon
pygame.display.set_caption("Space Invaders")
# icon = "icon.png"
# pygame.display.set_icon(icon)

# background
background = pygame.image.load("bg.webp")

# player
playerImg = pygame.image.load('player_retro_blue64px.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(.5)
    enemyY_change.append(40)

# laser
laserImg = []
laserX = []
laserY = []
laserY_change = []
laser_state = []
max_lasers = 7
for i in range(max_lasers):
    laserY.append(480)
    laserImg.append(pygame.image.load('laser.png'))
    laserX.append(0)
    laserY_change.append(1.2)
    laser_state.append("ready")

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over font
over_font = pygame.font.Font('freesansbold.ttf', 72)

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (182, 250))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def fire_laser(x, y, i):
    global laser_state
    laser_state[i] = "fire"
    screen.blit(laserImg[i], (x + 16 , y + 10))

def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX, 2)) + (math.pow(enemyY - laserY, 2)))
    if distance < 34:
        return True
    return False

# game loop
running = True
while running:
    # RGB - Red Green Blue
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                for i in range(max_lasers):
                    if laser_state[i] == "ready":
                        laserX[i] = playerX
                        fire_laser(laserX[i], laserY[i], i)
                    elif laser_state[i] == "fire":
                        continue
                    break
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i]+= enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 784:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

            # collision
        for j in range(max_lasers):
            collision = isCollision(enemyX[i], enemyY[i], laserX[j], laserY[j])
            if collision:
                laserY[j] = 480
                laser_state[j] = "ready"
                score_value += 1
                # print(score_value)
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # laser movement


    for j in range(max_lasers):
        if laser_state[j] == "fire":
            fire_laser(laserX[j], laserY[j], j)
            laserY[j] -= laserY_change[j]
        if laserY[j] <= 0:
            laser_state[j] = "ready"
            laserY[j] = 480


    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()

# 124 175 176 - greenGray
