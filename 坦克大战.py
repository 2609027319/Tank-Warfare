#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import Any
import pygame
import os
import random
import time
from pygame.sprite import  Group
player_bullet_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_tank_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
FPS = 60
WIDTH = 1000
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
player_life = 5
player1_life = 5

pygame.init()
pygame.mixer.init()
pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(1000,4000))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("坦克大战")
clock = pygame.time.Clock()
running = True

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction) -> None:
        super().__init__()
        self.bullets = ["img/bullet/bullet_up.png", "img/bullet/bullet_down.png",
                        "img/bullet/bullet_left.png", "img/bullet/bullet_right.png"]
        self.direction = direction
        if direction == "UP":
            self.bullet = pygame.image.load(self.bullets[0])
        elif direction == "DOWN":
            self.bullet = pygame.image.load(self.bullets[1])
        elif direction == "LEFT":
            self.bullet = pygame.image.load(self.bullets[2])
        elif direction == "RIGHT":
            self.bullet = pygame.image.load(self.bullets[3])
        self.image = self.bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        if self.direction == "UP":
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.rect.y += self.speed
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
        elif self.direction == "RIGHT":
            self.rect.x += self.speed
        if self.rect.bottom > HEIGHT or self.rect.right > WIDTH or self.rect.left < 0 or self.rect.top < 0:
            self.kill()

class Life(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.width = 120
        self.height = 50
        self.images = 6
        self.life_images = [
            "img/life/life0.png","img/life/life1.png","img/life/life2.png","img/life/life3.png","img/life/life4.png"
            ,"img/life/life5.png",
            "img/life/life6.png"]
        self.image = pygame.image.load(self.life_images[self.images])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = 50
        self.rect.bottom = 50
        self.player_death = 0
    def update(self):
        self.life_images = [
            "img/life/life0.png","img/life/life1.png","img/life/life2.png","img/life/life3.png","img/life/life4.png"
            ,"img/life/life5.png",
            "img/life/life6.png"]
        self.image = pygame.image.load(self.life_images[self.images])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        if player_life == 7:
            self.images = 6

        elif player_life == 6:
            self.images = 6

        elif player_life == 5:
            self.images = 5

        elif player_life == 4:
            self.images = 4

        elif player_life == 3:
            self.images = 3

        elif player_life == 2:
            self.images = 2

        elif player_life == 1:
            self.images = 1

        elif player_life == 0:
            self.images = 0

class Life1(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.width = 120
        self.height = 50
        self.images = 6
        self.life_images = [
            "img/life/life0.png","img/life/life1.png","img/life/life2.png","img/life/life3.png","img/life/life4.png"
            ,"img/life/life5.png",
            "img/life/life6.png"]
        self.image = pygame.image.load(self.life_images[self.images])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = 950
        self.rect.bottom = 50
        self.player1_death = 0
    def update(self):
        self.life_images = [
            "img/life/life0.png","img/life/life1.png","img/life/life2.png","img/life/life3.png","img/life/life4.png"
            ,"img/life/life5.png",
            "img/life/life6.png"]
        self.image = pygame.image.load(self.life_images[self.images])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        if player1_life == 7:
            self.images = 6

        elif player1_life == 6:
            self.images = 6

        elif player1_life == 5:
            self.images = 5

        elif player1_life == 4:
            self.images = 4

        elif player1_life == 3:
            self.images = 3

        elif player1_life == 2:
            self.images = 2

        elif player1_life == 1:
            self.images = 1

        elif player1_life == 0:
            self.images = 0

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.explosion_frames = [
            pygame.image.load("img/explosion/expl0.png"),
            pygame.image.load("img/explosion/expl1.png"),
            pygame.image.load("img/explosion/expl2.png"),
            pygame.image.load("img/explosion/expl3.png"),
            pygame.image.load("img/explosion/expl4.png")
        ]
        self.image_index = 0
        self.image = self.explosion_frames[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.animation_delay = 50
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_delay:
            self.last_update = now
            self.image_index += 1
            if self.image_index >= len(self.explosion_frames):
                self.kill()
            else:
                self.image = self.explosion_frames[self.image_index]

class Player1(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        tank_img = pygame.image.load(os.path.join("img/myTank", "tank_T2_0.png")).convert()
        self.tank = tank_img
        self.image = self.tank.subsurface((0, 0), (48, 48))
        self.rect = self.image.get_rect()
        self.rect.centerx = 600
        self.rect.bottom = HEIGHT - 10
        self.speed = 8
        self.direction = "UP"
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.initial_position = (600, HEIGHT - 10)

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x = self.rect.x + self.speed
            self.image = self.tank.subsurface((0, 144), (48, 42))
            self.direction = "RIGHT"
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speed
            self.image = self.tank.subsurface((0, 96), (48, 42))
            self.direction = "LEFT"
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speed
            self.image = self.tank.subsurface((0, 0), (48, 48))
            self.direction = "UP"
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speed
            self.image = self.tank.subsurface((0, 48), (48, 48))
            self.direction = "DOWN"
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
        bullets_fired = pygame.mixer.Sound("audios/fire.wav")
        bullets_fired.play()
        all_sprites.add(bullet)
        bullet_group.add(bullet) 
        player_bullet_group.add(bullet)

    def hit(self):
        if not self.invulnerable:
            self.invulnerable = True
            self.invulnerable_timer = 300 

class Player(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        tank_img = pygame.image.load(os.path.join("img/myTank", "tank_T1_0.png")).convert()
        self.tank = tank_img
        self.image = self.tank.subsurface((0, 0), (48, 48))
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.bottom = HEIGHT - 10
        self.speed = 8
        self.direction = "UP"
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.initial_position = (400, HEIGHT - 10)
        

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x = self.rect.x + self.speed
            self.image = self.tank.subsurface((0, 144), (48, 42))
            self.direction = "RIGHT"
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = self.tank.subsurface((0, 96), (48, 42))
            self.direction = "LEFT"
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
            self.image = self.tank.subsurface((0, 0), (48, 48))
            self.direction = "UP"
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.image = self.tank.subsurface((0, 48), (48, 48))
            self.direction = "DOWN"
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
            
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
        bullets_fired = pygame.mixer.Sound("audios/fire.wav")
        bullets_fired.play()
        all_sprites.add(bullet)
        bullet_group.add(bullet) 
        player_bullet_group.add(bullet)

    def hit(self):
        if not self.invulnerable:
            self.invulnerable = True
            self.invulnerable_timer = 300 

class EnemyTank(pygame.sprite.Sprite):

    def __init__(self,x) -> None:
        print("Creating enemy tank at position:", x)
        super().__init__()
        tank_img = pygame.image.load(os.path.join("img/enemyTank", "enemy_1_0.png")).convert()
        self.tank = tank_img
        self.image = self.tank.subsurface((0, 0), (48, 48))
        self.rect = self.image.get_rect()
        self.speed = 1
        self.direction = "DOWN"
        
        self.rect.top = random.randint(50, 600)
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        
        self.step = 120
        FIRE_BULLET_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(FIRE_BULLET_EVENT, 1000)

    def rand_direction(self):
        nmn = random.randint(1,4)
        if nmn == 1:
            return "UP"
        elif nmn == 2:
            return "DOWN"
        elif nmn == 3:
            return "RIGHT"
        else:
            return "LEFT"
            
    def move(self):
        if self.step < 0:
            self.step = 120
            self.direction = self.rand_direction()
        if self.direction == "UP":
            self.image = self.tank.subsurface((0, 0), (48, 42))
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.image = self.tank.subsurface((0, 48), (48, 42))
            self.rect.y += self.speed
        elif self.direction == "LEFT":
            self.image = self.tank.subsurface((0, 96), (48, 42))
            self.rect.x -= self.speed
        elif self.direction == "RIGHT":
            self.image = self.tank.subsurface((0, 144), (48, 42))
            self.rect.x += self.speed
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        self.step -= 1
        

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
        all_sprites.add(bullet)
        enemy_bullet_group.add(bullet)
    

    def update(self):
        print("Enemy Tank X:", self.rect.x, "Y:", self.rect.y)
        if self.direction == "UP":
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.rect.y += self.speed
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
        elif self.direction == "RIGHT":
            self.rect.x += self.speed
        
        if self.rect.bottom > HEIGHT:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()
        if self.rect.left > 0:
            self.kill()
        if self.rect.top > 0:
            self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.images = ["img/scene/brick.png","img/scene/brick1.png",
                  "img/scene/brick2.png"]
        self.image = pygame.image.load(self.images[random.randint(0,2)])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT

class Exit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/exit/exit.png")
        self.image = pygame.transform.scale(self.image, (60, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, 20)
all_sprites = pygame.sprite.Group()
enemy_tank_group = pygame.sprite.Group()
player_tank_group = pygame.sprite.Group()

player = Player()
player1 = Player1()
life = Life()
life1 = Life1()
exit = Exit()
wall = Wall()

all_sprites.add(player)
all_sprites.add(life)
all_sprites.add(life1)
all_sprites.add(exit)
all_sprites.add(wall)

Number_of_enemies = 15

victory_music_played = False
for i in range(15):
    enemy = EnemyTank(i)
    enemy_tank_group.add(enemy)

COUNT = pygame.USEREVENT +1
pygame.time.set_timer(COUNT,1000)
all_sprites.add(player1)

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player1.shoot()
            if player is not None:
                if event.key == pygame.K_j:
                    player.shoot()
        if event.type == pygame.USEREVENT + 1:
            for enemy in enemy_tank_group:
                enemy.shoot()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if exit.rect.collidepoint(pos):
                running = False
    
    for bullet in enemy_bullet_group:
        if player is not None and pygame.sprite.collide_rect(bullet, player):
            bullet.kill()
            if not player.invulnerable and player_life > 0:
                player_life -= 1
                player.rect.topleft = player.initial_position
                player.hit() 
            if player_life == 0:
                player.kill()
                player = None
        
    for bullet in enemy_bullet_group:
        if player1 is not None and pygame.sprite.collide_rect(bullet, player1):
            bullet.kill()
            if not player1.invulnerable and player1_life > 0:
                player1.hit() 
                player1_life -= 1
                player1.rect.topleft = player1.initial_position
                if player1_life == 0:
                    player1.kill()
                    player1 = None

    for enemy in enemy_tank_group:
        enemy.move()
        
    for bullet in player_bullet_group:
        enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_tank_group, True)
        if enemy_hit_list:
            enemy = enemy_hit_list[0]
            explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
            all_sprites.add(explosion)
            Number_of_enemies -= 1
            bullet.kill()
        bullet.update()

    if Number_of_enemies == 0 and not victory_music_played:
        print("Playing finish music")
        Finish_music = pygame.mixer.Sound("audios/Finish.wav")
        Finish_music.play()
        victory_music_played = True

    all_sprites.update()
    
    screen.fill(BLACK)
    
    enemy_bullet_group.update()  
    enemy_bullet_group.draw(screen)
    
    enemy_tank_group.draw(screen)
    
    bullet_group.update()  
    bullet_group.draw(screen)
    
    player_tank_group.draw(screen)
    
    if player is not None and player.invulnerable:
        font = pygame.font.Font("font/simkai.ttf", 36)
        text = font.render("无敌时间", True, (255, 255, 255))
        text_rect = text.get_rect(center=(70 , 100))
        screen.blit(text, text_rect)

    if player1 is not None and player1.invulnerable:
        font = pygame.font.Font("font/simkai.ttf", 36)
        text = font.render("无敌时间", True, (255, 255, 255))
        text_rect = text.get_rect(center=(930 , 100))
        screen.blit(text, text_rect)

    all_sprites.draw(screen)  
    
    pygame.display.flip()
pygame.quit()
