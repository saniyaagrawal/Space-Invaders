import pygame
import random
from pygame import mixer

# game initialization
pygame.init()

# screen size
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# set caption and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerIcon = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerChange = 0


def player(x, y):
    screen.blit(playerIcon, (x, y))


# Enemy
enemyIcon=[]
enemyX=[]
enemyY=[]
enemyYchange=[]
enemyXchange=[]
noOfEnemies=5
for i in range(noOfEnemies):
    enemyIcon.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 100))
    enemyXchange.append(3)
    enemyYchange.append(100)


def enemy(x, y, i):
    screen.blit(enemyIcon[i], (x, y))


# Bullet
bulletIcon = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletXchange = 0
bulletYchange = -10
bulletState = "ready"


def bullet(x, y):
    global bulletState
    bulletState = 'fire'
    screen.blit(bulletIcon, (x + 16, y - 10))

#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

def showScore():
    score=font.render('Score: '+str(score_value),True,(255,255,255))
    screen.blit(score,(10,10))

#GameOver
def gameOver():
    game_over=pygame.font.Font('freesansbold.ttf',64)
    text=game_over.render('GAME OVER',True,(255,255,255))
    screen.blit(text,(200,250))

running = True

# game loop
while running:
    # background RBG
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerChange += 4
            if event.key == pygame.K_LEFT:
                playerChange -= 4
            if event.key == pygame.K_SPACE and bulletState == 'ready':
                # bullet_Sound = mixer.Sound('laser.wav')
                # bullet_Sound.play()
                bulletX = playerX
                bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerChange = 0
    playerX += playerChange
    if bulletState is 'fire':
        bulletY += bulletYchange
        bullet(bulletX, bulletY)

    if bulletY <= 0:
        bulletState = 'ready'
        bulletY = 480
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(noOfEnemies):
        enemyX[i] += enemyXchange[i]

        #gameover
        if enemyY[i] >420:
            for j in range(noOfEnemies):
                enemyY[j]=2000
            gameOver()

        if enemyX[i] <= 0:
            enemyXchange[i] = 3
            enemyY[i] += enemyYchange[i]
        elif enemyX[i] >= 736:
            enemyXchange[i] = -3
            enemyY[i] += enemyYchange[i]
        if bulletX + 32 >= enemyX[i] and bulletX + 1 <= enemyX[i] + 64 and bulletY < enemyY[i] + 64 and bulletY >= enemyY[i]:
            score_value+=1
            #explosion sound
            # explosion_Sound= mixer.Sound('explosion.wav')
            # explosion_Sound.play()
            bulletY = 480
            bulletState = 'ready'
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 200)
        enemy(enemyX[i], enemyY[i], i)
    showScore()
    player(playerX, playerY)
    pygame.display.update()
