# space_invaders

import pygame
from os.path import join
import random

pygame.init()

# Window settings
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Game settings
FPS = 60
FONT = pygame.font.Font(join("assets/fonts", "chopsic.otf"), 30)

# Player settings
LIVES = 1
PLAYER_SPEED = 400

# Imports
BACKGROUND = pygame.transform.scale(pygame.image.load(join("assets/images", "bg.jpeg")).convert(), (WINDOW_WIDTH, WINDOW_HEIGHT))
PLAYER_SHIP = pygame.image.load(join("assets/images", "player_ship.png")).convert_alpha()

ENEMY_1 = pygame.transform.scale(pygame.image.load(join("assets/images", "enemy_green.png")).convert_alpha(), (50, 70))
ENEMY_2 = pygame.transform.scale(pygame.image.load(join("assets/images", "enemy_blue.png")).convert_alpha(), (50, 60))
ENEMY_3 = pygame.transform.scale(pygame.image.load(join("assets/images", "enemy_red.png")).convert_alpha(), (60, 60))
ENEMY_4 = pygame.transform.scale(pygame.image.load(join("assets/images", "enemy_cian.png")).convert_alpha(), (50, 50))

PLAYER_LASER  = pygame.image.load(join("assets/images", "player_laser.png")).convert_alpha()
LASER_1  = pygame.image.load(join("assets/images", "laser_green.png")).convert_alpha()
LASER_2  = pygame.image.load(join("assets/images", "laser_blue.png")).convert_alpha()
LASER_3  = pygame.image.load(join("assets/images", "laser_red.png")).convert_alpha()
LASER_4  = pygame.image.load(join("assets/images", "laser_cian.png")).convert_alpha()

EXPLOSION = [pygame.image.load(join("assets/images/explosion", f"{i}.png")).convert_alpha() for i in range(21)]

# Sound Effects
GAME_MUSIC = pygame.mixer.Sound(join("assets/audio/", "game_music.mp3"))
PLAYER_LASER_SFX = pygame.mixer.Sound(join("assets/audio/", "player_laser.wav"))
PLAYER_HIT_SFX = pygame.mixer.Sound(join("assets/audio/", "player_hit.wav"))
PLAYER_DEATH_SFX = pygame.mixer.Sound(join("assets/audio/", "player_death.mp3"))
ENEMY_DEATH_SFX = pygame.mixer.Sound(join("assets/audio/", "enemy_death.wav"))
ENEMY_LASER_SFX = pygame.mixer.Sound(join("assets/audio/", "enemy_laser.wav"))
LEVEL_UP = pygame.mixer.Sound(join("assets/audio/", "level_up.mp3"))

GAME_MUSIC.set_volume(0.1)
PLAYER_LASER_SFX.set_volume(0.05)
ENEMY_LASER_SFX.set_volume(0.1)
ENEMY_DEATH_SFX.set_volume(0.3)
PLAYER_HIT_SFX.set_volume(0.3)




class Ship(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_frect(center=pos)
        self.width = self.rect.width
        self.height = self.rect.height
        self.speed = speed
        self.direction = pygame.math.Vector2()


class Player(Ship):
    def __init__(self, image, laser_image, pos, speed, *groups):
        super().__init__(image, pos, speed, groups[0])
        self.lives = LIVES
        self.level = 1
        self.score = 0
        self.lost = False
        self.groups = groups
        
        # Laser attributes
        self.laser_image = laser_image
        self.can_shoot_laser = True
        self.last_shot = 0
        self.shoot_delay = 300
        self.laser_speed = 900
        self.max_health = 10
        self.health = self.max_health
        
    def draw_health_bar(self):
        pygame.draw.rect(WIN, 'red', (self.rect.left, self.rect.bottom + 10, self.width, 10))
        pygame.draw.rect(WIN, 'green', (self.rect.left, self.rect.bottom + 10, self.health * (self.width/self.max_health), 10))
        
    def check_laser_delay(self):
        if not self.can_shoot_laser:
            if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
                self.can_shoot_laser = True
        
    def shoot_laser(self):
        keys = pygame.key.get_just_pressed()
        if int(keys[pygame.K_SPACE]) and self.can_shoot_laser:
            PLAYER_LASER_SFX.play()
            self.can_shoot_laser = False
            self.last_shot = pygame.time.get_ticks()
            Laser(self.laser_image, self.rect.midtop, self.laser_speed, -1, self.groups)
        self.check_laser_delay()
            
    def update(self, dt):
        
        
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        
        new_position = self.rect.center + self.direction * self.speed * dt
        if self.width/2 <= new_position.x <= WINDOW_WIDTH - self.width/2 and self.height/2 <= new_position.y <= WINDOW_HEIGHT - self.height/2:
           self.rect.center = new_position
           
        
           
        self.shoot_laser()
 
 
class Enemy(Ship):
    enemie_map = [
        (ENEMY_1, LASER_1),
        (ENEMY_2, LASER_2),
        (ENEMY_3, LASER_3),
        (ENEMY_4, LASER_4)
    ]
    def __init__(self, pos, speed, *groups):
        ship_image, laser_image = random.choice(self.enemie_map)
        super().__init__(ship_image, pos, speed, groups[0], groups[1], groups[2])
        
        
        # Laser settings 
        self.laser_image = laser_image
        self.laser_speed = self.speed + random.randint(50, 600)
        self.laser_can_shoot = False
        self.laser_delay = random.randint(500, 3000)
        self.laser_creation_time = pygame.time.get_ticks()
        self.laser_groups = (groups[0], groups[1], groups[3])
    
    def check_laser_delay(self):
        '''Check if the delay from the last laser has passed to shoot another one'''
        if not self.laser_can_shoot:
            if pygame.time.get_ticks() - self.laser_creation_time > self.laser_delay:
                self.laser_can_shoot = True
        
    def update(self, dt):
        # Move enemy ship
        self.direction.y = 1
        self.rect.center += self.direction * self.speed * dt
        
        # Shoot laser
        if self.laser_can_shoot:
            ENEMY_LASER_SFX.play()
            Laser(self.laser_image, self.rect.midbottom, self.laser_speed, 1, self.laser_groups)
            self.laser_creation_time = pygame.time.get_ticks()
            self.laser_can_shoot = False
        # Check if the delay to shoot another laser has passed
        self.check_laser_delay()
        
        
        if self.rect.bottom >= WINDOW_HEIGHT + 100:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed, direction, *groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2(0,direction)
        self.speed = speed
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.bottom <= 0 or self.rect.top >= WINDOW_HEIGHT:
            self.kill()
        

class Explosion(pygame.sprite.Sprite):
    def __init__(self, frame_list, pos, *groups):
        super().__init__(*groups)
        self.index = 0
        self.frame_list = frame_list
        self.image = frame_list[self.index]
        self.rect = self.image.get_frect(center=pos)
        self.animation_speed = 100
    
    def update(self, dt):
        self.index += self.animation_speed * dt
        if self.index < len(self.frame_list):
            self.image = self.frame_list[int(self.index)]
        else:
            self.kill()
 
            
def score(player):
    lives_label = FONT.render(f"Lives:  {player.lives}", True, "white")
    level_label = FONT.render(f"Level:  {player.level}", True, "white")
    score_label = FONT.render(f"Score:  {player.score}", True, "white")
    
    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (WINDOW_WIDTH - level_label.get_width() - 10, 10))
    WIN.blit(score_label, (WINDOW_WIDTH/2-score_label.get_width()/2, 10))


def colision(player, all_sprites, all_enemies, all_player_lasers, all_enemies_ships):
    player_colision = pygame.sprite.spritecollide(player, all_enemies, True, pygame.sprite.collide_mask)
    if player_colision:
        for enemy in player_colision:
            PLAYER_HIT_SFX.play()
            Explosion(EXPLOSION, enemy.rect.center, all_sprites)
            player.health -= 1
            if player.health <= 0:
                PLAYER_DEATH_SFX.play()
                player.lives -= 1
                if player.lives <= 0:
                    player.lost = True
                if not player.lost:    
                    player.health = player.max_health
    
            
    laser_collision = pygame.sprite.groupcollide(all_player_lasers, all_enemies_ships, True, True, pygame.sprite.collide_mask)
    if laser_collision:
        for laser in laser_collision:
            ENEMY_DEATH_SFX.play()
            Explosion(EXPLOSION, laser.rect.center, all_sprites)
        player.score += 1

         
def game():
    run = True
    clock = pygame.time.Clock()
 
    lost = False
    enemy_speed = 50
    enemy_speed_increment = 50
    enemy_creation_decrement = 2000
    enemy_create_event = pygame.event.custom_type()
    last_score_check = 0
    pygame.time.set_timer(enemy_create_event, 2000)
    
    all_sprites = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    all_enemies_ships = pygame.sprite.Group()
    all_enemies_lasers = pygame.sprite.Group()
    all_player_lasers = pygame.sprite.Group()
    
    player = Player(PLAYER_SHIP, PLAYER_LASER, (WINDOW_WIDTH/2,WINDOW_HEIGHT-70), PLAYER_SPEED, all_sprites, all_player_lasers)

    while run:
        dt = clock.tick(FPS) / 1000
        
        if player.score % 10 == 0 and player.score != last_score_check:
            LEVEL_UP.play()
            player.level += 1
            enemy_creation_decrement -= 100
            enemy_speed_increment += 20
            enemy_speed = random.randint(50, enemy_speed_increment)
            enemy_creation_speed = max(200, enemy_creation_decrement)
            
            last_score_check = player.score
            pygame.time.set_timer(enemy_create_event, enemy_creation_speed)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            if event.type == enemy_create_event:
                x = random.randint(50, WINDOW_WIDTH - 50) 
                Enemy((x, -50), enemy_speed, all_sprites, all_enemies, all_enemies_ships, all_enemies_lasers)
                
        # Check coollision
        colision(player, all_sprites, all_enemies, all_player_lasers, all_enemies_ships)
        
        # Update sprites position      
        all_sprites.update(dt)
        
        # Draw bakcground, score, and sprites 
        WIN.blit(BACKGROUND, (0, 0))
        score(player)
        all_sprites.draw(WIN)
        
        player.draw_health_bar()

        
      
        if player.lost:
            lost_label = FONT.render("You Lost!", True, "white")
            WIN.blit(lost_label, (WINDOW_WIDTH/2-lost_label.get_width()/2, WINDOW_HEIGHT/2))
            pygame.display.update()
            pygame.time.delay(4000)
            pygame.event.clear()
            return
        
        pygame.display.update()
        
    pygame.quit()

def main():
    run = True
    start_label = FONT.render(f'Press "SPACE" bar to start', True, "white")
    exit_label = FONT.render(f'Press "ESC" to exit', True, "white")
    start_label_rect = start_label.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
    exit_label_rect = exit_label.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2 + 50))
    GAME_MUSIC.play(loops=-1)
    while run:
        WIN.blit(BACKGROUND, (0,0)) 
        WIN.blit(start_label, start_label_rect)
        WIN.blit(exit_label, exit_label_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game()
    pygame.quit()

if __name__ == "__main__":
    main()