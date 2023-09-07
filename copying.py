import pygame
FPS = 60
WIDTH = 1000
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
player_life = 5
player1_life = 5
painted_eggshell = False

all_sprites = pygame.sprite.Group()
enemy_tank_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
iron_group = pygame.sprite.Group()

