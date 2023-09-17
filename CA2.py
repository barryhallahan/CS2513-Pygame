#IMPORTS
import pygame
from pygame.locals import *
from pygame import mixer




# PYGAME FPS HANDLE
clock = pygame.time.Clock()
fps = 60


#VARIABLES DEFINED
rows = 5
cols = 5
screen_width = 600
screen_height = 600

# SCREEN DISPLAY - DIMENSIONS / CAPTION / 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invanders')

# GAME MUSIC 
pygame.mixer.pre_init(20000, -16, 34, 1024)

# INITIALISATION 
mixer.init()
# SOUND PLAYED -> BULLET - ENEMY COLLISION
player_laser = pygame.mixer.Sound("laser.mp3")

#GAME BG MUSIC
mixer.music.load("bg_music.mp3")
#CONSTANT PLAYTIME [-1]
mixer.music.play(-1)

player_score = 0

# FONT INITIALISE 
pygame.font.init()

font = font = pygame.font.Font('freesansbold.ttf', 20)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

# SCOREBOARD [ POS TOP RIGHT SCREEN ]
def show_score(score_statX, score_statY):

    score = font.render("SCORE: " + str(player_score), True, (255,255,255))
    screen.blit(score, (score_statX , score_statY ))
 
# GAME OVER - Q WHEN END 
def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over_text, (100, 50))



# GAME BG IMAGE
bg = pygame.image.load("bg.jpg")
# SCALE TO WINDOW SIZE
bg_window_size = (600,600)

# WINDOW SIZE CONVERT
bg = pygame.transform.scale(bg, bg_window_size)

# DRAW THE BG ON SCREEN
def draw_bg():
    screen.blit(bg, (0, 0))


#SPACESHIP [PLAYER] CLASS
class Spaceship(pygame.sprite.Sprite):
    '''
    THIS IS THE CLASS THAT THE USER CONTROLS

    INCLUDES SPRITE IMAGE [ OVERLAY ]
    PLAYER - SPEED - SHOOT ABILITY 
    
    LEFT / RIGHT KEY PRESS -> MOVEMENT 
    '''
    def __init__(self, x, y):
        
        #SPRITE
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("spaceship.png")

        # SCALE TO SCREEN 
        self.image_scaled = (60, 60)

        self.image = pygame.transform.scale(self.image, self.image_scaled)

        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()

    # UPDATED IN-GAME
    def update(self):
        # SHIP MOVEMENT SPEED
        speed = 4
        
        # SHOOT COOLDOWN 
        time_between_shot = 200 
    
        


        # PLAYER KEY PRESS 
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        # ALLOW DELAY BETWEEN SHOT
        time_now = pygame.time.get_ticks()
        
        # PLAYER SHOOT ABILITY
        if key[pygame.K_SPACE] and time_now - self.last_shot > time_between_shot:
            bullet = Player_Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now


# BULLET CLASS [SHOT FROM PLAYER]
class Player_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):

        # SPRITE
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png") 

        #SCALE
        self.image_scaled = (10, 10)

        self.image = pygame.transform.scale(self.image, self.image_scaled)

        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    # IN-GAME UPDATE
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()

            global player_score
            player_score += 1
            
           
            # SOUND Q
            player_laser.play()

            if len(alien_group) == 0:
                create_aliens()


# ENEMY CLASS [ALIEN]
class Aliens(pygame.sprite.Sprite):
    '''
    THIS IS THE CLASS THAT MOVES ALIEN [ENEMY] DOWN GAME SCREEN

    INCLUDES SPRITE IMAGE [ OVERLAY ]
    SPEED - MOVE ABILITY 
    
    PROGRESSIVELY GETS CLOSER TO PLAYER / REMOVED DUE TO COLLSIONS  
    '''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # SPRITE IMAGE
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # BEGIN
        self.move_counter = 0
        self.move_direction = 1

    # MOVEMENT
    def update(self):
        self.rect.x += self.move_direction
        # SPEED
        self.move_counter += 1.5

        # KEEP ALIEN ON SCREEN
        if abs(self.move_counter) > 80:
            # RETURN ALIEN DIRECTION
            self.move_direction *= -1

            # REDUCE ALIEN Y VALUE -> DROP DOWN GAME SCREEN
            self.rect.y -= -5
            self.move_counter *= self.move_direction
        

# CREATE SPRITE GROUPS - HOLD TOGETHER 
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()


def create_aliens():
    # CREATE ALIEN GROUP ON SCREEN VIA LOOP
    for row in range(rows):
        for item in range(cols):

            # SIZE / SPACING 
            alien = Aliens(100 + item * 100, 80 + row * 40)
            alien_group.add(alien)
# CALL
create_aliens()


# PLACE PLAYER ON SCREEN
spaceship = Spaceship(int(screen_width / 2), screen_height - 35)

# ADD TO SPRITE GROUP
spaceship_group.add(spaceship)


# GAME LOOP
while True:

    clock.tick(fps)

    # SCREEN BG
    draw_bg()

    # SCORE COUNTER
    show_score(10, 10)

    # CHECK IF ALL ENEMY KILL()
    if len(alien_group) == 0:
            
            # GAME OVER
            game_over()
    if pygame.sprite.spritecollide(spaceship, alien_group, False):
        # Display "Game Over" when a collision occurs
        game_over()
        pygame.display.update()
        pygame.time.delay(2000)  # Wait for 2 seconds (adjust as needed)
        pygame.quit()  # Quit the game
        


    # EVENT HANDLE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # PLAYER UPDATE
    spaceship.update()
    
    # DRAW SPRITE GROUP
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)


    # SPRITE GROUP UPDATE
    bullet_group.update()
    alien_group.update()

    pygame.display.update()

  






