from tweener import *
from asyncio import wait
from turtle import delay
import pygame
import random
import math
from pygame import mixer  
from tkinter import messagebox 


pygame.init()  
# 
screen =  pygame.display.set_mode((1000, 653)) 

background = pygame.image.load('resources/images/back1.jpg')



mixer.music.load('resources/sounds/bac_music.mp3')
mixer.music.play(-1)

  
pygame.display.set_caption("THE BATTLE FOR CAPITALIST WORLD")
dark_lord_health = 10
win_num = 0
icon = pygame.image.load('resources/images/elvenemblem.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('resources/images/goc2.png')
playerX = 500
playerY = 580 
playerX_change = 0


# enemy
winnum = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10
for i in range(num_of_enemies):

    enemyImg.append(pygame.image.load('resources/images/star1.png'))
    enemyX.append(random.randint(160, 500))
    enemyY.append(random.randint(270, 300))
    enemyX_change.append(1)
    enemyY_change.append(40)
 
fallingImg = []
fallingX = []
fallingY = []
fallingX_change = []
fallingY_change = []
num_of_fallings = 4
for i in range(num_of_fallings):

    fallingImg.append(pygame.image.load('resources/images/starf.png'))
    fallingX.append(random.randint(160, 500))
    fallingY.append(random.randint(270, 300))
    fallingY_change.append(0.2)
 



# arrow
arrowImg = pygame.image.load('resources/images/dollarw.png')
arrowX = 0
arrowY = 950
arrowX_change = 0  
arrowY_change = 3
arrow_state = 'ready'


#  fireball 
# fireballImg = pygame.image.load('resources/images/flames.png')
# fireballX = 0
# fireballY = 480
# fireballX_change = 0
# fireballY_change = 2
# fireball_state = 'ready'



game_over_num = 0  
game_win_num = 0 

score_value = 0

font = pygame.font.Font('freesansbold.ttf', 32)
player_font = pygame.font.Font('freesansbold.ttf', 17)

textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)
 



def game_over_text():
    game_over = over_font.render("Game over!", True, (0, 0, 0))
    screen.blit(game_over, (200, 250))

def show_boss_name():
    game_over = font.render("Mao Zedong, The Red Sun In The Sky", True, (0, 0, 0))
    screen.blit(game_over, (200, 20))

def show_player_name():
    game_over = player_font.render("Brave Capitalist", True, (0, 0, 0))
    screen.blit(game_over, (5, 520))





def show_score(x, y):
    score = font.render(str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def falling(x, y, i):
    screen.blit(fallingImg[i], (x, y))


def shoot(x, y):
    global arrow_state
    arrow_state ='fire'
    screen.blit(arrowImg, (x + 16, y + 10))





def isCollision(enemyX, enemyY, arrowX, arrowY):
    distance = math.sqrt((math.pow(enemyX - arrowX, 2)) + (math.pow(enemyY - arrowY, 2)))
    if distance < 27:
        return True
    else:
        return False

def isCollision2(fallingX, fallingY, arrowX, arrowY):
    distance = math.sqrt((math.pow(fallingX - arrowX, 2)) + (math.pow(fallingY - arrowY, 2)))
    if distance < 27:
        return True
    else:
        return False

def isCollision3(playerX, playerY, fireballX, fireballY):
    distance = math.sqrt((math.pow(playerX - fireballX, 2)) + (math.pow(playerY - fireballY, 2)))
    if distance < 27:
        return True
    else:
        return False

class HealthBar():
  def __init__(self, x, y, w, h, max_hp):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.x2 = x
    self.y2 = y
    self.w2 = w
    self.h2 = h
    
    self.hp = max_hp
    self.max_hp = max_hp
    self.ratio2 = self.hp / self.max_hp
    self.anim_y = None  # Store the animation object
  def draw(self, surface):
    #calculate health ratio
    ratio = self.hp / self.max_hp
    
    pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h))
    pygame.draw.rect(surface, "yellow", (self.x2, self.y2, self.w2, self.h2))
    pygame.draw.rect(surface, "red", (self.x, self.y, self.w * ratio, self.h))
    if self.anim_y is not None:
        self.anim_y.update()
        self.w2 = self.anim_y.value  # Update the width with the animated value
    

health_bar = HealthBar(150, 60, 700, 20, 50 )
health_bar.hp = health_bar.max_hp


def dmg_health():
    
    current_health = health_bar.hp
    health_bar.hp -= 1
    if health_bar.w2 == health_bar.w * health_bar.hp / health_bar.max_hp:
        health_bar.anim_y = Tween(begin=health_bar.w * current_health / health_bar.max_hp,
            end=health_bar.w * health_bar.hp / health_bar.max_hp,
            duration=1000,
            easing=Easing.SINE,
            easing_mode=EasingMode.OUT,
            boomerang=False, 
            loop=False)
    else:
        health_bar.anim_y = Tween(begin=health_bar.w2,
            end=health_bar.w * health_bar.hp / health_bar.max_hp,
            duration=1000,
            easing=Easing.SINE,
            easing_mode=EasingMode.OUT,
            boomerang=False, 
            loop=False)
        
    
    health_bar.anim_y.start()

class PHealthBar():
  def __init__(self, x, y, w, h, max_hp):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.hp = max_hp
    self.max_hp = max_hp

  def draw(self, surface):
    #calculate health ratio
    ratio = self.hp / self.max_hp
    pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h))
    pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

phealth_bar = PHealthBar(5, 500, 100, 10, 3) #5
phealth_bar.hp = phealth_bar.max_hp


enemy_X_c = 0.7
falling_start = False

running = True
while running:
    

    
    screen.fill((0, 0, 0))

    screen.blit(background,(0, 0))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 250, 700, 400))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7

            if event.key == pygame.K_SPACE:
                if arrow_state == "ready":
                    arrow_sound = mixer.Sound('resources/sounds/arr.wav')
                    arrow_sound.play()
                    arrowX = playerX
                    shoot(arrowX, arrowY)
                
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0



    playerX += playerX_change

    if playerX <= 150:
        playerX = 150

    elif playerX >= 850:
        playerX = 850  

    for i in range(num_of_enemies):
        if enemyY[i] > 650:
            enemyX[i] = random.randint(160, 830)
            enemyY[i] = random.randint(270, 300)

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 160:
            enemyX_change[i] = enemy_X_c
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 810:
            enemyX_change[i] = -enemy_X_c
            enemyY[i] += enemyY_change[i]

        player_attacked = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if player_attacked:
            phealth_bar.hp -= 1
            enemyX[i] = random.randint(160, 830)
            enemyY[i] = random.randint(270, 300)
            
        enemy(enemyX[i], enemyY[i], i)

        collision = isCollision(enemyX[i], enemyY[i], arrowX, arrowY)
        if collision:
            orc_sound = mixer.Sound('resources/sounds/orco.wav')
            orc_sound.play()
            arrowY = 580
            arrow_state = 'ready'
            dmg_health()
            
            enemyX[i] = random.randint(160, 830)
            enemyY[i] = random.randint(270, 300)
        enemy(enemyX[i], enemyY[i], i)

    if falling_start:
        for i in range(num_of_fallings):
            if fallingY[i] > 650:
                phealth_bar.hp -= 1
                fallingX[i] = random.randint(160, 830)
                fallingY[i] = random.randint(270, 300)

            fallingY[i] += fallingY_change[i]

            player_attacked = isCollision(fallingX[i], fallingY[i], playerX, playerY)
            if player_attacked:
                phealth_bar.hp -= 1
                fallingX[i] = random.randint(160, 830)
                fallingY[i] = random.randint(270, 300)

            falling(fallingX[i], fallingY[i], i)

            collision = isCollision(fallingX[i], fallingY[i], arrowX, arrowY)
            if collision:
                orc_sound = mixer.Sound('resources/sounds/orco.wav')
                orc_sound.play()
                arrowY = 580
                arrow_state = 'ready'
                dmg_health()
                fallingX[i] = random.randint(160, 830)
                fallingY[i] = random.randint(270, 300)
            falling(fallingX[i], fallingY[i], i)

        

    if arrowY <= 250:
        arrowY = 580
        arrow_state = 'ready'

    

    
 
    if arrow_state == "fire":
        shoot(arrowX, arrowY)
        arrowY -= arrowY_change

    

    if phealth_bar.hp <= 0:
        game_over_num = 1
        running = False

    if health_bar.hp <= 30:
        falling_start = True

    if health_bar.hp <= 20:
        falling_start = False
        enemy_X_c = 1.2            
    if health_bar.hp == 34 and phealth_bar.hp == 2:
        messagebox.showinfo("John Piss", "Eht ofni er'uoy gnikees si ton ereh.")
        winnum = 44384
        running = False



    if health_bar.hp <= 0:
        messagebox.showinfo("...", "...")
        messagebox.showinfo("...", "...")
        messagebox.showinfo("...", "...")
        messagebox.showinfo("...", "...")
        messagebox.showinfo("...", "...")
        messagebox.showinfo("...", "...")
        
        messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "ugh...")
        messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "you hurt me")
        messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "but...")
        messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "do you really think...")
        messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "you could defeat me?")
        messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "you can't kill communism incarnated")
        messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "and now...")
        messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "you will meet...")
        messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "YOUR DOOM!!!")
        
        game_win_num = 1
        running = False


    
    health_bar.draw(screen)
    phealth_bar.draw(screen)

    player(playerX, playerY)


    show_boss_name()
    show_player_name()
    
    

 
    pygame.display.update()































 





# game_win_num = 1







 
if game_win_num == 1:

    


    pygame.init()
    screen = pygame.display.set_mode((1000, 653))

    background = pygame.image.load('resources/images/back2.jpg')
    



    mixer.music.load('resources/sounds/moreepic.mp3')
    mixer.music.play(-1)

    pygame.display.set_caption("THE BATTLE FOR CAPITALIST WORLD")
    dark_lord_health = 10
    win_num = 0
    icon = pygame.image.load('resources/images/elvenemblem.png')
    pygame.display.set_icon(icon)

    playerImg = pygame.image.load('resources/images/goc2.png')
    playerX = 500
    playerY = 580
    playerX_change = 0
    playerX_des_c = 0.7

    winnum = 0

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 20
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('resources/images/star1.png'))
        enemyX.append(random.randint(160, 500))
        enemyY.append(random.randint(270, 300))
        enemyX_change.append(4)
        enemyY_change.append(40)

    fallingImg = []
    fallingX = []
    fallingY = []
    fallingX_change = []
    fallingY_change = []
    num_of_fallings = 10
    for i in range(num_of_fallings):
        fallingImg.append(pygame.image.load('resources/images/star1.png'))
        fallingX.append(random.randint(160, 500))
        fallingY.append(random.randint(270, 300))
        fallingX_change.append(0)
        fallingY_change.append(0.15)

    falling2Img = []
    falling2X = []
    falling2Y = []
    falling2X_change = []
    falling2Y_change = []
    num_of_fallings2 = 4
    for i in range(num_of_fallings2):
        falling2Img.append(pygame.image.load('resources/images/communist.png'))
        falling2X.append(random.randint(160, 500))
        falling2Y.append(random.randint(270, 300))
        falling2X_change.append(0)
        falling2Y_change.append(0.2)

    falling3Img = []
    falling3X = []
    falling3Y = []
    falling3X_change = []
    falling3Y_change = []
    num_of_fallings3 = 2
    for i in range(num_of_fallings3):
        falling3Img.append(pygame.image.load('resources/images/deathar.png'))
        falling3X.append(random.randint(160, 500))
        falling3Y.append(random.randint(270, 300))
        falling3X_change.append(0)
        falling3Y_change.append(0.1)

    darkImg = pygame.image.load('resources/images/lor.png')
    darkX = 500
    darkY = 250
    darkX_change = 0.3
    darkY_change = 40

    fireballImg = pygame.image.load('resources/images/flames.png')
    fireballX = 500
    fireballY = 400
    fX_change = 0
    fY_change = 1
    f_state = 'ready'

    arrowImg = pygame.image.load('resources/images/dollarw.png')
    arrowX = 0
    arrowY = 580
    arrowX_change = 0
    arrowY_change = 3
    arrow_state = 'ready'

    game_over_num = 0
    game_win_num = 0

    score_value = 0

    font = pygame.font.Font('freesansbold.ttf', 32)
    player_font = pygame.font.Font('freesansbold.ttf', 17)

    textX = 10
    textY = 10

    over_font = pygame.font.Font('freesansbold.ttf', 64)
 


    def game_over_text():
        game_over = over_font.render("Game over!", True, (0, 0, 0))
        screen.blit(game_over, (200, 250))

    def show_boss_name():
        game_over = font.render("GREAT MAO, THE GOD OF COMMUNISM", True, (0, 0, 0))
        screen.blit(game_over, (200, 20))

    def show_player_name():
        game_over = player_font.render("Brave Capitalist", True, (0, 0, 0))
        screen.blit(game_over, (5, 520))

    def dark(x, y):
        screen.blit(darkImg, (x, y))

    def cast(x, y):
        global f_state
        f_state = 'fire'
        screen.blit(fireballImg, (x + 16, y + 10))

    def show_score(x, y):
        score = font.render(str(score_value), True, (0, 0, 0))
        screen.blit(score, (x, y))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def falling(x, y, i):
        screen.blit(fallingImg[i], (x, y))

    def falling2(x, y, i):
        screen.blit(falling2Img[i], (x, y))

    def falling3(x, y, i):
        screen.blit(falling3Img[i], (x, y))

    def shoot(x, y):
        global arrow_state
        arrow_state = 'fire'
        screen.blit(arrowImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, arrowX, arrowY):
        distance = math.sqrt((math.pow(enemyX - arrowX, 2)) + (math.pow(enemyY - arrowY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def isCollision2(dX, dY, arrowX, arrowY):
        distance = math.sqrt((math.pow(dX - arrowX, 2)) + (math.pow(dY - arrowY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def isCollision3(playerX, playerY, fireballX, fireballY):
        distance = math.sqrt((math.pow(playerX - fireballX, 2)) + (math.pow(playerY - fireballY, 2)))
        if distance < 27:
            return True
        else:
            return False

    class HealthBar():
      def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = x
        self.y2 = y
        self.w2 = w
        self.h2 = h

        self.hp = max_hp
        self.max_hp = max_hp
        self.ratio2 = self.hp / self.max_hp
        self.anim_y = None  # Store the animation object
      def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp

        pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "yellow", (self.x2, self.y2, self.w2, self.h2))
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w * ratio, self.h))
        if self.anim_y is not None:
            self.anim_y.update()
            self.w2 = self.anim_y.value  # Update the width with the animated value


    health_bar = HealthBar(150, 60, 700, 20, 70)
    health_bar.hp = health_bar.max_hp


    def dmg_health():

        current_health = health_bar.hp
        health_bar.hp -= 1
        if health_bar.w2 == health_bar.w * health_bar.hp / health_bar.max_hp:
            health_bar.anim_y = Tween(begin=health_bar.w * current_health / health_bar.max_hp,
                end=health_bar.w * health_bar.hp / health_bar.max_hp,
                duration=1000,
                easing=Easing.SINE,
                easing_mode=EasingMode.OUT,
                boomerang=False, 
                loop=False)
        else:
            health_bar.anim_y = Tween(begin=health_bar.w2,
                end=health_bar.w * health_bar.hp / health_bar.max_hp,
                duration=1000,
                easing=Easing.SINE,
                easing_mode=EasingMode.OUT,
                boomerang=False, 
                loop=False)


        health_bar.anim_y.start()

    def dmg_health2():

        current_health = health_bar.hp
        health_bar.hp -= 5
        if health_bar.w2 == health_bar.w * health_bar.hp / health_bar.max_hp:
            health_bar.anim_y = Tween(begin=health_bar.w * current_health / health_bar.max_hp,
                end=health_bar.w * health_bar.hp / health_bar.max_hp,
                duration=1000,
                easing=Easing.SINE,
                easing_mode=EasingMode.OUT,
                boomerang=False, 
                loop=False)
        else:
            health_bar.anim_y = Tween(begin=health_bar.w2,
                end=health_bar.w * health_bar.hp / health_bar.max_hp,
                duration=1000,
                easing=Easing.SINE,
                easing_mode=EasingMode.OUT,
                boomerang=False, 
                loop=False)


        health_bar.anim_y.start()


    class PHealthBar():
        def __init__(self, x, y, w, h, max_hp):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.hp = max_hp
            self.max_hp = max_hp

        def draw(self, surface):
            ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h))
            pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

    phealth_bar = PHealthBar(5, 500, 100, 10, 5 ) #5
    phealth_bar.hp = phealth_bar.max_hp

    enemy_X_c = 4
    falling_start = False
    enemy_start = False
    dark_start = True
    falling2_start = False
    falling3_start = False

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 250, 700, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -playerX_des_c

                if event.key == pygame.K_RIGHT:
                    playerX_change = playerX_des_c

                if event.key == pygame.K_SPACE:
                    if arrow_state == "ready":
                        arrow_sound = mixer.Sound('resources/sounds/arr.wav')
                        arrow_sound.play()
                        arrowX = playerX
                        shoot(arrowX, arrowY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX <= 150:
            playerX = 150

        elif playerX >= 800:
            playerX = 800

        if dark_start:
            darkX += darkX_change

            if darkX <= 160:
                darkX_change = 0.4

            elif darkX >= 810:
                darkX_change = -0.4

            collision = isCollision(darkX, darkY, arrowX, arrowY)
            if collision:
                orc_sound = mixer.Sound('resources/sounds/orco.wav')
                orc_sound.play()
                arrowY = 580
                arrow_state = 'ready'
                dmg_health()
 
            collision2 = isCollision2(playerX, playerY, fireballX, fireballY)
            if collision2:
                phealth_bar.hp -= 1
                fireballY = darkY
                f_state = "ready"

            dark(darkX, darkY)

        if enemy_start:
            for i in range(num_of_enemies):
                if enemyY[i] > 650:
                    enemyX[i] = random.randint(160, 830)
                    enemyY[i] = random.randint(270, 500)

                enemyX[i] += enemyX_change[i]

                if enemyX[i] <= 150:
                    enemyX_change[i] = enemy_X_c
                    enemyY[i] += enemyY_change[i]

                elif enemyX[i] >= 850:
                    enemyX_change[i] = -enemy_X_c
                    enemyY[i] += enemyY_change[i]

                # player_attacked = isCollision(enemyX[i], enemyY[i], playerX, playerY)
                # if player_attacked:
                #     # phealth_bar.hp -= 1
                #     enemyX[i] = random.randint(160, 830)
                #     enemyY[i] = random.randint(270, 300)

                # enemy(enemyX[i], enemyY[i], i)

                # collision = isCollision(enemyX[i], enemyY[i], arrowX, arrowY)
                # if collision:
                #     enemyX[i] = random.randint(160, 830)
                #     enemyY[i] = random.randint(270, 300)
                enemy(enemyX[i], enemyY[i], i)

        if falling_start:
            for i in range(num_of_fallings):
                if fallingY[i] > 650:
                    fallingX[i] = random.randint(160, 830)
                    fallingY[i] = random.randint(270, 300)

                fallingY[i] += fallingY_change[i]

                player_attacked2 = isCollision(fallingX[i], fallingY[i], playerX, playerY)
                if player_attacked2:
                    phealth_bar.hp -= 1
                    fallingX[i] = random.randint(160, 830)
                    fallingY[i] = random.randint(270, 300)

                collisionf = isCollision(fallingX[i], fallingY[i], arrowX, arrowY)
                if collisionf:
                    orc_sound = mixer.Sound('resources/sounds/orco.wav')
                    orc_sound.play()
                    arrowY = 580
                    arrow_state = 'ready'
                    dmg_health()
                    fallingX[i] = random.randint(160, 830)
                    fallingY[i] = random.randint(270, 300)
                falling(fallingX[i], fallingY[i], i)

        if falling2_start:
            for i in range(num_of_fallings2):
                if falling2Y[i] > 650:
                    falling2X[i] = random.randint(160, 830)
                    falling2Y[i] = random.randint(270, 300)

                falling2Y[i] += falling2Y_change[i]

                player_attacked2 = isCollision(falling2X[i], falling2Y[i], playerX, playerY)
                if player_attacked2:
                    phealth_bar.hp -= 10
                    falling2X[i] = random.randint(160, 830)
                    falling2Y[i] = random.randint(270, 300)

                falling2(falling2X[i], falling2Y[i], i)

        if falling3_start:
            for i in range(num_of_fallings3):
                if falling3Y[i] > 650:
                    phealth_bar.hp -= 1
                    falling3X[i] = random.randint(160, 830)
                    falling3Y[i] = random.randint(270, 300)

                falling3Y[i] += falling3Y_change[i]

                player_attacked2 = isCollision(falling3X[i], falling3Y[i], playerX, playerY)
                if player_attacked2:
                    phealth_bar.hp -= 1
                    falling3X[i] = random.randint(160, 830)
                    falling3Y[i] = random.randint(270, 300)

                collisionf = isCollision(falling3X[i], falling3Y[i], arrowX, arrowY)
                if collisionf:
                    orc_sound = mixer.Sound('resources/sounds/orco.wav')
                    orc_sound.play()
                    arrowY = 580
                    arrow_state = 'ready'
                    dmg_health2()
                    falling3X[i] = random.randint(160, 830)
                    falling3Y[i] = random.randint(270, 300)
                falling3(falling3X[i], falling3Y[i], i)

        if arrowY <= 250:
            arrowY = 580
            arrow_state = 'ready'

        if arrow_state == "fire":
            shoot(arrowX, arrowY)
            arrowY -= arrowY_change

        if f_state == "ready": 
            f_sound = mixer.Sound('resources/sounds/fire.wav')
            f_sound.play()
            fireballX = darkX
            cast(fireballX, fireballY)

        if f_state == "fire":
            cast(fireballX, fireballY)
            fireballY += fY_change

        if fireballY >= 650:
            fireballY = darkY
            f_state = "ready"

        if phealth_bar.hp <= 0:
            game_over_num = 1
            messagebox.showerror("Game", "You are dead")
            running = False

        if health_bar.hp <= 60:
            enemy_start = True

        if health_bar.hp <= 53:
            falling_start = True
            playerX_des_c = 1.4

        if health_bar.hp <= 40:
            falling2_start = True

        if health_bar.hp <= 30:
            falling3_start = True

        if health_bar.hp <= 0:
            game_win_num = 2
            running = False

        if health_bar.hp == 34 and phealth_bar.hp == 2:
            game_win_num = 8
            running = False



        health_bar.draw(screen)
        phealth_bar.draw(screen)

        player(playerX, playerY)

        show_boss_name()
        show_player_name()

        pygame.display.update()














































if game_win_num == 2:
    
    import rotatescreen
    screenm = rotatescreen.get_primary_display()
    start_pos = screenm.current_orientation

    pygame.init()
    screen = pygame.display.set_mode((1000, 653))

    background = pygame.image.load('resources/images/back3.png')
    
    messagebox.showinfo("...", "...")
    messagebox.showinfo("...", "...")
    messagebox.showinfo("...", "...")
    messagebox.showinfo("...", "...")
    messagebox.showinfo("...", "...")
    messagebox.showinfo("...", "...")

    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "...")
    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "You are powerful")
    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "It's time")
    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "For my FINAL ATTACK")

    tck = 0

    pygame.display.set_caption("THE BATTLE FOR CAPITALIST WORLD")
    dark_lord_health = 10
    win_num = 0
    icon = pygame.image.load('resources/images/elvenemblem.png')
    pygame.display.set_icon(icon)

    playerImg = pygame.image.load('resources/images/goc2.png')
    playerX = 500
    playerY = 580
    playerX_change = 0
    playerX_des_c = 0.7

    winnum = 0

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 10
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('resources/images/communist.png'))
        enemyX.append(random.randint(0, 1000))
        enemyY.append(random.randint(0, 570))
        enemyX_change.append(1)
        enemyY_change.append(40)

    fallingImg = []
    fallingX = []
    fallingY = []
    fallingX_change = []
    fallingY_change = []
    num_of_fallings = 4
    for i in range(num_of_fallings):
        fallingImg.append(pygame.image.load('resources/images/communist.png'))
        fallingX.append(random.randint(0, 1000))
        fallingY.append(random.randint(0, 570))
        fallingX_change.append(0)
        fallingY_change.append(2)

    falling2Img = []
    falling2X = []
    falling2Y = []
    falling2X_change = []
    falling2Y_change = []
    num_of_fallings2 = 4
    for i in range(num_of_fallings2):
        falling2Img.append(pygame.image.load('resources/images/communist.png'))
        falling2X.append(random.randint(0, 1000))
        falling2Y.append(random.randint(0, 570))
        falling2X_change.append(0)
        falling2Y_change.append(2)

    falling3Img = []
    falling3X = []
    falling3Y = []
    falling3X_change = []
    falling3Y_change = []
    num_of_fallings3 = 2
    for i in range(num_of_fallings3):
        falling3Img.append(pygame.image.load('resources/images/deathar.png'))
        falling3X.append(random.randint(0, 1000))
        falling3Y.append(random.randint(0, 570))
        falling3X_change.append(0)
        falling3Y_change.append(15)

    darkImg = pygame.image.load('resources/images/lor.png')
    darkX = 500
    darkY = 400
    darkX_change = 0.7
    darkY_change = 40

    fireballImg = pygame.image.load('resources/images/flames.png')
    fireballX = 500
    fireballY = 400
    fX_change = 0
    fY_change = 2
    f_state = 'ready'

    arrowImg = pygame.image.load('resources/images/dollarw.png')
    arrowX = 0
    arrowY = 580
    arrowX_change = 0
    arrowY_change = 3
    arrow_state = 'ready'

    game_over_num = 0
    game_win_num = 0

    score_value = 0

    font = pygame.font.Font('freesansbold.ttf', 32)
    player_font = pygame.font.Font('freesansbold.ttf', 17)

    textX = 10
    textY = 10

    over_font = pygame.font.Font('freesansbold.ttf', 64)



    def game_over_text():
        game_over = over_font.render("Game over!", True, (0, 0, 0))
        screen.blit(game_over, (200, 250))

    def show_boss_name():
        game_over = font.render("GREAT MAO, THE GOD OF COMMUNISM", True, (0, 0, 0))
        screen.blit(game_over, (200, 20))

    def show_player_name():
        game_over = player_font.render("Brave Capitalist", True, (0, 0, 0))
        screen.blit(game_over, (5, 520))

    def dark(x, y):
        screen.blit(darkImg, (x, y))

    def cast(x, y):
        global f_state
        f_state = 'fire'
        screen.blit(fireballImg, (x + 16, y + 10))

    def show_score(x, y):
        score = font.render(str(score_value), True, (0, 0, 0))
        screen.blit(score, (x, y))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def falling(x, y, i):
        screen.blit(fallingImg[i], (x, y))

    def falling2(x, y, i):
        screen.blit(falling2Img[i], (x, y))

    def falling3(x, y, i):
        screen.blit(falling3Img[i], (x, y))

    def shoot(x, y):
        global arrow_state
        arrow_state = 'fire'
        screen.blit(arrowImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, arrowX, arrowY):
        distance = math.sqrt((math.pow(enemyX - arrowX, 2)) + (math.pow(enemyY - arrowY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def isCollision2(dX, dY, arrowX, arrowY):
        distance = math.sqrt((math.pow(dX - arrowX, 2)) + (math.pow(dY - arrowY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def isCollision3(playerX, playerY, fireballX, fireballY):
        distance = math.sqrt((math.pow(playerX - fireballX, 2)) + (math.pow(playerY - fireballY, 2)))
        if distance < 27:
            return True
        else:
            return False

    class HealthBar():
      def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = x
        self.y2 = y
        self.w2 = w
        self.h2 = h
        
        self.hp = max_hp
        self.max_hp = max_hp
        self.ratio2 = self.hp / self.max_hp
        self.anim_y = None  # Store the animation object
      def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp
        
        pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "yellow", (self.x2, self.y2, self.w2, self.h2))
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w * ratio, self.h))
        if self.anim_y is not None:
            self.anim_y.update()
            self.w2 = self.anim_y.value  # Update the width with the animated value
        
    
    health_bar = HealthBar(150, 60, 700, 20, 50)
    health_bar.hp = 1
    
    
    def dmg_health():
        
        current_health = health_bar.hp
        health_bar.hp -= 1
        if health_bar.w2 == health_bar.w * health_bar.hp / health_bar.max_hp:
            health_bar.anim_y = Tween(begin=health_bar.w * current_health / health_bar.max_hp,
                end=health_bar.w * health_bar.hp / health_bar.max_hp,
                duration=1000,
                easing=Easing.SINE,
                easing_mode=EasingMode.OUT,
                boomerang=False, 
                loop=False)
        else:
            health_bar.anim_y = Tween(begin=health_bar.w2,
                end=health_bar.w * health_bar.hp / health_bar.max_hp,
                duration=1000,
                easing=Easing.SINE,
                easing_mode=EasingMode.OUT,
                boomerang=False, 
                loop=False)
            
        
        health_bar.anim_y.start()


    class PHealthBar():
        def __init__(self, x, y, w, h, max_hp):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.hp = max_hp
            self.max_hp = max_hp

        def draw(self, surface):
            ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h))
            pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

    phealth_bar = PHealthBar(5, 520, 100, 10, 6)
    phealth_bar.hp = phealth_bar.max_hp

    enemy_X_c = 10
    falling_start = False
    enemy_start = True
    dark_start = False
    falling2_start = True
    falling3_start = True

    running = True
    while running:
        screen.fill((0, 0, 0))

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 250, 700, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -playerX_des_c

                if event.key == pygame.K_RIGHT:
                    playerX_change = playerX_des_c

                if event.key == pygame.K_SPACE:
                    if arrow_state == "ready":
                        arrow_sound = mixer.Sound('resources/sounds/arr.wav')
                        arrow_sound.play()
                        arrowX = playerX
                        shoot(arrowX, arrowY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX <= 150:
            playerX = 150

        elif playerX >= 850:
            playerX = 850

        if dark_start:
            darkX += darkX_change

            if darkX <= 160:
                darkX_change = 0.7

            elif darkX >= 810:
                darkX_change = -0.7

            collision = isCollision(darkX, darkY, arrowX, arrowY)
            if collision:
                orc_sound = mixer.Sound('resources/sounds/orco.wav')
                orc_sound.play()
                arrowY = 580
                arrow_state = 'ready'
                health_bar.hp -= 1

            collision2 = isCollision2(playerX, playerY, fireballX, fireballY)
            if collision2:
                phealth_bar.hp -= 1
                fireballY = darkY
                f_state = "ready"

            dark(darkX, darkY)

        if enemy_start:
            for i in range(num_of_enemies):
                if enemyY[i] > 650:
                    enemyX[i] = random.randint(0, 1000)
                    enemyY[i] = random.randint(0, 570)

                enemyX[i] += enemyX_change[i]

                if enemyX[i] <= 0:
                    enemyX_change[i] = enemy_X_c
                    enemyY[i] += enemyY_change[i]

                elif enemyX[i] >= 1000:
                    enemyX_change[i] = -enemy_X_c
                    enemyY[i] += enemyY_change[i]

                enemy(enemyX[i], enemyY[i], i)

        if falling_start:
            for i in range(num_of_fallings):
                if fallingY[i] > 650:
                    fallingX[i] = random.randint(0, 1000)
                    fallingY[i] = random.randint(0, 570)

                fallingY[i] += fallingY_change[i]

                player_attacked2 = isCollision(fallingX[i], fallingY[i], playerX, playerY)
                if player_attacked2:
                    phealth_bar.hp -= 1
                    fallingX[i] = random.randint(0, 1000)
                    fallingY[i] = random.randint(0, 570)

                falling(fallingX[i], fallingY[i], i)

        if falling2_start:
            for i in range(num_of_fallings2):
                if falling2Y[i] > 650:
                    falling2X[i] = random.randint(0, 1000)
                    falling2Y[i] = random.randint(0, 570)

                falling2Y[i] += falling2Y_change[i]

                falling2(falling2X[i], falling2Y[i], i)

        if falling3_start:
            for i in range(num_of_fallings3):
                if falling3Y[i] > 650:
                    falling3X[i] = random.randint(0, 1000)
                    falling3Y[i] = random.randint(0, 570)

                falling3Y[i] += falling3Y_change[i]

                falling3(falling3X[i], falling3Y[i], i)

        if arrowY <= 250:
            arrowY = 580
            arrow_state = 'ready'

        if arrow_state == "fire":
            shoot(arrowX, arrowY)
            arrowY -= arrowY_change

        # if f_state == "ready":
        #     f_sound = mixer.Sound('resources/sounds/fire.wav')
        #     f_sound.play()
        #     fireballX = darkX
        #     cast(fireballX, fireballY)

        # if f_state == "fire":
        #     cast(fireballX, fireballY)
        #     fireballY += fY_change

        # if fireballY >= 650:
        #     fireballY = darkY
        #     f_state = "ready"

        if phealth_bar.hp <= 0:
            game_over_num = 1
            messagebox.showerror("Game", "You are dead")
            running = False

        if health_bar.hp <= 30:
            enemy_start = True

        if health_bar.hp <= 20:
            falling_start = True
            playerX_des_c = 1.4

        if health_bar.hp <= 10:
            falling2_start = True

        if health_bar.hp <= 5:
            falling3_start = True

        # if health_bar.hp <= 1:
        #     game_win_num = 3
        #     running = False

        health_bar.draw(screen)
        phealth_bar.draw(screen)

        player(playerX, playerY)

        show_boss_name()
        show_player_name()

        tck += 1

        if tck == 200:
            phealth_bar.hp -= 4
            for i in range(1, 101):
                posq = abs((start_pos - i * 90) % 360)
                screenm.rotate_to(posq)
                game_win_num = 3

            running = False

        pygame.display.update()






























if game_win_num == 3:
    

    pygame.init()
    screen = pygame.display.set_mode((1000, 653))

    background = pygame.image.load('resources/images/back2.jpg')
    

    mixer.music.load('resources/sounds/finale.mp3')
    mixer.music.play(-1)

    messagebox.showinfo("...", "...")
    messagebox.showinfo("...", "...")


    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "You are stronger than I thought")
    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "I have one HP left, so do you")
    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "I have last final surprise for you")
    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "The damage I will receive won't be my damage, it will be OUR damage")
    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "And I don't mean just us, I mean THE WHOLE WORLD!")
    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "That's right, if you kill me, you will destroy the universe")
    messagebox.showinfo("Mao Zedong, The Red Sun In The Sky", "Just surrender, it's not worth it")

    pygame.display.set_caption("THE BATTLE FOR CAPITALIST WORLD")
    dark_lord_health = 10
    win_num = 0
    icon = pygame.image.load('resources/images/elvenemblem.png')
    pygame.display.set_icon(icon)

    playerImg = pygame.image.load('resources/images/goc2.png')
    playerX = 500
    playerY = 580
    playerX_change = 0
    playerX_des_c = 0.7

    winnum = 0

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 10
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('resources/images/star1.png'))
        enemyX.append(random.randint(160, 500))
        enemyY.append(random.randint(270, 300))
        enemyX_change.append(1)
        enemyY_change.append(40)

    fallingImg = []
    fallingX = []
    fallingY = []
    fallingX_change = []
    fallingY_change = []
    num_of_fallings = 4
    for i in range(num_of_fallings):
        fallingImg.append(pygame.image.load('resources/images/star1.png'))
        fallingX.append(random.randint(160, 500))
        fallingY.append(random.randint(270, 300))
        fallingX_change.append(0)
        fallingY_change.append(0.2)

    falling2Img = []
    falling2X = []
    falling2Y = []
    falling2X_change = []
    falling2Y_change = []
    num_of_fallings2 = 1
    for i in range(num_of_fallings2):
        falling2Img.append(pygame.image.load('resources/images/communist.png'))
        falling2X.append(500)
        falling2Y.append(400)
        falling2X_change.append(0)
        falling2Y_change.append(0)

    falling3Img = []
    falling3X = []
    falling3Y = []
    falling3X_change = []
    falling3Y_change = []
    num_of_fallings3 = 2
    for i in range(num_of_fallings3):
        falling3Img.append(pygame.image.load('resources/images/deathar.png'))
        falling3X.append(random.randint(160, 500))
        falling3Y.append(random.randint(270, 300))
        falling3X_change.append(0)
        falling3Y_change.append(0.15)

    darkImg = pygame.image.load('resources/images/lor.png')
    darkX = 500
    darkY = 400
    darkX_change = 0.7
    darkY_change = 40

    fireballImg = pygame.image.load('resources/images/flames.png')
    fireballX = 500
    fireballY = 400
    fX_change = 0
    fY_change = 2
    f_state = 'ready'

    arrowImg = pygame.image.load('resources/images/dollarw.png')
    arrowX = 0
    arrowY = 580
    arrowX_change = 0
    arrowY_change = 3
    arrow_state = 'ready'

    game_over_num = 0
    game_win_num = 0

    score_value = 0

    font = pygame.font.Font('freesansbold.ttf', 32)
    player_font = pygame.font.Font('freesansbold.ttf', 17)

    textX = 10
    textY = 10

    over_font = pygame.font.Font('freesansbold.ttf', 64)



    def game_over_text():
        game_over = over_font.render("Game over!", True, (0, 0, 0))
        screen.blit(game_over, (200, 250))

    def show_boss_name():
        game_over = font.render("GREAT MAO, THE GOD OF COMMUNISM", True, (0, 0, 0))
        screen.blit(game_over, (200, 20))

    def show_player_name():
        game_over = player_font.render("Brave Capitalist", True, (0, 0, 0))
        screen.blit(game_over, (5, 520))

    def show_surrender():
        game_over2 = font.render('Press "Tab" to surrender ', True, (225, 225, 225))
        screen.blit(game_over2, (350, 600))

    def dark(x, y):
        screen.blit(darkImg, (x, y))

    def cast(x, y):
        global f_state
        f_state = 'fire'
        screen.blit(fireballImg, (x + 16, y + 10))

    def show_score(x, y):
        score = font.render(str(score_value), True, (0, 0, 0))
        screen.blit(score, (x, y))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def falling(x, y, i):
        screen.blit(fallingImg[i], (x, y))

    def falling2(x, y, i):
        screen.blit(falling2Img[i], (x, y))

    def falling3(x, y, i):
        screen.blit(falling3Img[i], (x, y))

    def shoot(x, y):
        global arrow_state
        arrow_state = 'fire'
        screen.blit(arrowImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, arrowX, arrowY):
        distance = math.sqrt((math.pow(enemyX - arrowX, 2)) + (math.pow(enemyY - arrowY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def isCollision2(dX, dY, arrowX, arrowY):
        distance = math.sqrt((math.pow(dX - arrowX, 2)) + (math.pow(dY - arrowY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def isCollision3(playerX, playerY, fireballX, fireballY):
        distance = math.sqrt((math.pow(playerX - fireballX, 2)) + (math.pow(playerY - fireballY, 2)))
        if distance < 27:
            return True
        else:
            return False

    class HealthBar():
      def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = x
        self.y2 = y
        self.w2 = w
        self.h2 = h

        self.hp = max_hp
        self.max_hp = max_hp
        self.ratio2 = self.hp / self.max_hp
        self.anim_y = None  # Store the animation object
      def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp

        pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "yellow", (self.x2, self.y2, self.w2, self.h2))
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w * ratio, self.h))
        if self.anim_y is not None:
            self.anim_y.update()
            self.w2 = self.anim_y.value  # Update the width with the animated value


    health_bar = HealthBar(150, 60, 700, 20, 1)
    health_bar.hp = health_bar.max_hp


    def dmg_health():

        current_health = health_bar.hp
        health_bar.hp -= 1
        if health_bar.w2 == health_bar.w * health_bar.hp / health_bar.max_hp:
            health_bar.anim_y = Tween(begin=health_bar.w * current_health / health_bar.max_hp,
                end=health_bar.w * health_bar.hp / health_bar.max_hp,
                duration=1000,
                easing=Easing.SINE,
                easing_mode=EasingMode.OUT,
                boomerang=False, 
                loop=False)
        else:
            health_bar.anim_y = Tween(begin=health_bar.w2,
                end=health_bar.w * health_bar.hp / health_bar.max_hp,
                duration=1000,
                easing=Easing.SINE,
                easing_mode=EasingMode.OUT,
                boomerang=False, 
                loop=False)


        health_bar.anim_y.start()


    class PHealthBar():
        def __init__(self, x, y, w, h, max_hp):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.hp = max_hp
            self.max_hp = max_hp

        def draw(self, surface):
            ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h))
            pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

    phealth_bar = PHealthBar(5, 520, 100, 10, 1)
    phealth_bar.hp = 1

    enemy_X_c = 1
    falling_start = False
    enemy_start = False
    dark_start = False
    falling2_start = True
    falling3_start = False

    running = True
    while running:
        screen.fill((0, 0, 0))

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 250, 700, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -playerX_des_c

                if event.key == pygame.K_RIGHT:
                    playerX_change = playerX_des_c

                if event.key == pygame.K_SPACE:
                    if arrow_state == "ready":
                        arrow_sound = mixer.Sound('resources/sounds/arr.wav')
                        arrow_sound.play()
                        arrowX = playerX
                        shoot(arrowX, arrowY)

                if event.key == pygame.K_TAB:
                    phealth_bar.hp = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX <= 150:
            playerX = 150

        elif playerX >= 850:
            playerX = 850

        if dark_start:
            darkX += darkX_change

            if darkX <= 160:
                darkX_change = 0.7

            elif darkX >= 810:
                darkX_change = -0.7

            collision = isCollision(darkX, darkY, arrowX, arrowY)
            if collision:
                orc_sound = mixer.Sound('resources/sounds/orco.wav')
                orc_sound.play()
                arrowY = 580
                arrow_state = 'ready'
                dmg_health()

            collision2 = isCollision2(playerX, playerY, fireballX, fireballY)
            if collision2:
                phealth_bar.hp -= 1
                fireballY = darkY
                f_state = "ready"

            dark(darkX, darkY)

        if falling2_start:
            for i in range(num_of_fallings2):
                if falling2Y[i] > 650:
                    falling2X[i] = random.randint(160, 500)
                    falling2Y[i] = random.randint(270, 300)

                falling2Y[i] += falling2Y_change[i]

                player_attacked2 = isCollision(falling2X[i], falling2Y[i], playerX, playerY)
                if player_attacked2:
                    phealth_bar.hp -= 1
                    falling2X[i] = random.randint(160, 500)
                    falling2Y[i] = random.randint(270, 300)

                collisionf = isCollision(falling2X[i], falling2Y[i], arrowX, arrowY)
                if collisionf:
                    dmg_health()

                    pygame.draw.rect(screen, (21, 27, 84), pygame.Rect(0, 0, 2000, 2000))
                    orc_sound = mixer.Sound('shieldex.wav')
                    orc_sound.play()
                    arrowY = 580
                    arrow_state = 'ready'
                    
                falling2(falling2X[i], falling2Y[i], i)

        if arrowY <= 250:
            arrowY = 580
            arrow_state = 'ready'

        if arrow_state == "fire":
            shoot(arrowX, arrowY)
            arrowY -= arrowY_change

        # if phealth_bar.hp <= 0:
        #     game_over_num = 1
        #     messagebox.showerror("Game", "You are dead")
        #     running = False

        if health_bar.hp <= 0:
            pygame.draw.rect(screen, (21, 27, 84), pygame.Rect(0, 0, 2000, 2000))
            messagebox.showinfo("Game", "GOD FELLED")
            messagebox.showinfo("Game", "Mao lied to you, you didn't destroy the world")
            messagebox.showinfo("Game", "Because communism never works")
            messagebox.showinfo("Game", "Welcome to the world without communism")
            running = False

        health_bar.draw(screen)
        phealth_bar.draw(screen)

        player(playerX, playerY)

        show_surrender()
        show_boss_name()
        show_player_name()

        pygame.display.update()






























































if game_win_num == 8:
    

    pygame.init()
    screen = pygame.display.set_mode((1000, 653))

    background = pygame.image.load('resources/images/back9.jpg')
    

    mixer.music.load('horror.mp3')
    mixer.music.play(-1)

    messagebox.showinfo("...", "...")
    messagebox.showinfo("...", "...")



    pygame.display.set_caption("THE BATTLE FOR CAPITALIST WORLD")
    dark_lord_health = 10
    win_num = 0
    icon = pygame.image.load('resources/images/elvenemblem.png')
    pygame.display.set_icon(icon)

    playerImg = pygame.image.load('resources/images/goc2.png')
    playerX = 500
    playerY = 580
    playerX_change = 0
    playerX_des_c = 0.7

    winnum = 0

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 10
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('resources/images/star1.png'))
        enemyX.append(random.randint(160, 500))
        enemyY.append(random.randint(270, 300))
        enemyX_change.append(1)
        enemyY_change.append(40)

    fallingImg = []
    fallingX = []
    fallingY = []
    fallingX_change = []
    fallingY_change = []
    num_of_fallings = 4
    for i in range(num_of_fallings):
        fallingImg.append(pygame.image.load('resources/images/star1.png'))
        fallingX.append(random.randint(160, 500))
        fallingY.append(random.randint(270, 300))
        fallingX_change.append(0)
        fallingY_change.append(0.2)

    falling2Img = []
    falling2X = []
    falling2Y = []
    falling2X_change = []
    falling2Y_change = []
    num_of_fallings2 = 1
    for i in range(num_of_fallings2):
        falling2Img.append(pygame.image.load('resources/images/communist.png'))
        falling2X.append(500)
        falling2Y.append(400)
        falling2X_change.append(0)
        falling2Y_change.append(0)

    falling3Img = []
    falling3X = []
    falling3Y = []
    falling3X_change = []
    falling3Y_change = []
    num_of_fallings3 = 2
    for i in range(num_of_fallings3):
        falling3Img.append(pygame.image.load('resources/images/deathar.png'))
        falling3X.append(random.randint(160, 500))
        falling3Y.append(random.randint(270, 300))
        falling3X_change.append(0)
        falling3Y_change.append(0.15)

    darkImg = pygame.image.load('resources/images/lor.png')
    darkX = 500
    darkY = 400
    darkX_change = 0.7
    darkY_change = 40

    fireballImg = pygame.image.load('resources/images/flames.png')
    fireballX = 500
    fireballY = 400
    fX_change = 0
    fY_change = 2
    f_state = 'ready'

    arrowImg = pygame.image.load('resources/images/dollarw.png')
    arrowX = 0
    arrowY = 580
    arrowX_change = 0
    arrowY_change = 3
    arrow_state = 'ready'

    game_over_num = 0
    game_win_num = 0

    score_value = 0

    font = pygame.font.Font('freesansbold.ttf', 32)
    player_font = pygame.font.Font('freesansbold.ttf', 17)

    textX = 10
    textY = 10

    over_font = pygame.font.Font('freesansbold.ttf', 64)



    def game_over_text():
        game_over = over_font.render("Game over!", True, (0, 0, 0))
        screen.blit(game_over, (200, 250))

    def show_boss_name():
        game_over = font.render("GREAT MAO, THE GOD OF COMMUNISM", True, (0, 0, 0))
        screen.blit(game_over, (200, 20))

    def show_player_name():
        game_over = player_font.render("Brave Capitalist", True, (0, 0, 0))
        screen.blit(game_over, (5, 520))

    def show_surrender():
        game_over2 = font.render('Press "Tab" to surrender ', True, (225, 225, 225))
        screen.blit(game_over2, (350, 600))

    def dark(x, y):
        screen.blit(darkImg, (x, y))

    def cast(x, y):
        global f_state
        f_state = 'fire'
        screen.blit(fireballImg, (x + 16, y + 10))

    def show_score(x, y):
        score = font.render(str(score_value), True, (0, 0, 0))
        screen.blit(score, (x, y))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def falling(x, y, i):
        screen.blit(fallingImg[i], (x, y))

    def falling2(x, y, i):
        screen.blit(falling2Img[i], (x, y))

    def falling3(x, y, i):
        screen.blit(falling3Img[i], (x, y))

    def shoot(x, y):
        global arrow_state
        arrow_state = 'fire'
        screen.blit(arrowImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, arrowX, arrowY):
        distance = math.sqrt((math.pow(enemyX - arrowX, 2)) + (math.pow(enemyY - arrowY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def isCollision2(dX, dY, arrowX, arrowY):
        distance = math.sqrt((math.pow(dX - arrowX, 2)) + (math.pow(dY - arrowY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def isCollision3(playerX, playerY, fireballX, fireballY):
        distance = math.sqrt((math.pow(playerX - fireballX, 2)) + (math.pow(playerY - fireballY, 2)))
        if distance < 27:
            return True
        else:
            return False

    class HealthBar():
      def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = x
        self.y2 = y
        self.w2 = w
        self.h2 = h

        self.hp = max_hp
        self.max_hp = max_hp
        self.ratio2 = self.hp / self.max_hp
        self.anim_y = None  # Store the animation object
      def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp

        pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "yellow", (self.x2, self.y2, self.w2, self.h2))
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w * ratio, self.h))
        if self.anim_y is not None:
            self.anim_y.update()
            self.w2 = self.anim_y.value  # Update the width with the animated value


    health_bar = HealthBar(150, 60, 700, 20, 1)
    health_bar.hp = health_bar.max_hp


    def dmg_health():

        current_health = health_bar.hp
        health_bar.hp -= 1
        if health_bar.w2 == health_bar.w * health_bar.hp / health_bar.max_hp:
            health_bar.anim_y = Tween(begin=health_bar.w * current_health / health_bar.max_hp,
                end=health_bar.w * health_bar.hp / health_bar.max_hp,
                duration=1000,
                easing=Easing.SINE,
                easing_mode=EasingMode.OUT,
                boomerang=False, 
                loop=False)
        else:
            health_bar.anim_y = Tween(begin=health_bar.w2,
                end=health_bar.w * health_bar.hp / health_bar.max_hp,
                duration=1000,
                easing=Easing.SINE,
                easing_mode=EasingMode.OUT,
                boomerang=False, 
                loop=False)


        health_bar.anim_y.start()


    class PHealthBar():
        def __init__(self, x, y, w, h, max_hp):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.hp = max_hp
            self.max_hp = max_hp

        def draw(self, surface):
            ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h))
            pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

    phealth_bar = PHealthBar(5, 520, 100, 10, 1)
    phealth_bar.hp = 1

    enemy_X_c = 1
    falling_start = False
    enemy_start = False
    dark_start = False
    falling2_start = True
    falling3_start = False

    running = True
    while running:
        screen.fill((0, 0, 0))

        screen.blit(background, (0, 0))
        messagebox.showinfo("John Piss", "29.02.05.05.2025/106.230.140.124 - release date of Legend of John Piss. Qont'o Laeirangunei/ Ancap > Communism / Iq byn dheën fouhrerr / when 0=0, 8*0=0 and 3*0=0, then 8*0=3*0|/0 -> 8=3/ 10.3.2098 death of universe/John Piss 2 -> 1.09.1939/ www.cdprojekt.netlify.app/I know where you live/ you are on RNQL death note/ buy John Piss /what's the meaning of life?/ 7-9/ We're coming for you...")

        pygame.display.update()