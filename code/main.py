# space_invaders

import pygame
from os.path import join
import random

pygame.init()

# Window settings
WINDOW_WIDTH, WINDOW_HEIGHT = 750, 750
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Game settings
FPS = 60
FONT = pygame.font.SysFont("comicsons", 50)

# Imports
BACKGROUND = pygame.transform.scale(pygame.image.load(join("assets/images", "background-black.png")).convert(), (WINDOW_WIDTH, WINDOW_HEIGHT))
PLAYER_SHIP = pygame.image.load(join("assets/images", "pixel_ship_yellow.png")).convert_alpha()
SHIP_BLUE_SMALL = pygame.image.load(join("assets/images", "pixel_ship_blue_small.png")).convert_alpha()
SHIP_GREEN_SMALL = pygame.image.load(join("assets/images", "pixel_ship_green_small.png")).convert_alpha()
SHIP_RED_SMALL = pygame.image.load(join("assets/images", "pixel_ship_red_small.png")).convert_alpha()
LASER_BLUE  = pygame.image.load(join("assets/images", "pixel_laser_blue.png")).convert_alpha()
LASER_GREEN  = pygame.image.load(join("assets/images", "pixel_laser_green.png")).convert_alpha()
LASER_RED  = pygame.image.load(join("assets/images", "pixel_laser_red.png")).convert_alpha()
LASER_YELLOW  = pygame.image.load(join("assets/images", "pixel_laser_yellow.png")).convert_alpha()

def draw(lives, level):
    lives_label = FONT.render(f"Lives: {lives}", True, "white")
    level_label = FONT.render(f"Level: {level}", True, "white")
    
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (WINDOW_WIDTH - level_label.get_width() - 10, 10))
    pygame.display.update()
    


def main():
    run = True
    clock = pygame.time.Clock()
    
    # Game variables
    lives = 5
    level = 1

    while run:
        clock.tick(FPS)  # Limit the frame rate to 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

        draw(lives, level)
        
    pygame.quit()

if __name__ == "__main__":
    main()