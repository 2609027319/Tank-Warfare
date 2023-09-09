#   导入模块，文件......
from typing import Any
import pygame
import os
import random
from pygame.sprite import Group
from bullt import Bullet
from player import Player
#   一些变量
FPS = 60
WIDTH = 1000
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
running = True
player_life = 5
player1_life = 5
painted_eggshell = False
Defeat = False
paused = False

#   初始化
pygame.init()
pygame.mixer.init()
pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(1000,4000))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("坦克大战")
clock = pygame.time.Clock()

#   播放开始音乐
Start_music = pygame.mixer.Sound("audios/start.wav")
Start_music.play()

#   角色区

#   生命
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

#   爆炸
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

#   坦克
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
        self.last_shoot_time = 0
        self.BULLET_COOLDOWN = 250
        self.old_position = self.rect.topleft
    def update(self):
        self.old_position = self.rect.topleft
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
        wall_hit_list = pygame.sprite.spritecollide(self, wall_group, False)
        if wall_hit_list:
            self.rect.topleft = self.old_position
        iron_hit_list = pygame.sprite.spritecollide(self, iron_group, False)
        if iron_hit_list:
            self.rect.topleft = self.old_position


    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.BULLET_COOLDOWN:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            bullets_fired = pygame.mixer.Sound("audios/fire.wav")
            bullets_fired.play()
            all_sprites.add(bullet)
            bullet_group.add(bullet) 
            player_bullet_group.add(bullet)
            self.last_shoot_time = current_time

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
        self.rect.centerx = 380
        self.rect.bottom = HEIGHT - 10
        self.speed = 8
        self.direction = "UP"
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.initial_position = (380, HEIGHT - 10)
        self.last_shoot_time = 0
        self.BULLET_COOLDOWN = 250
        self.old_position = self.rect.topleft


    def update(self):
        self.old_position = self.rect.topleft
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
        wall_hit_list = pygame.sprite.spritecollide(self, wall_group, False)
        if wall_hit_list:
            self.rect.topleft = self.old_position
        iron_hit_list = pygame.sprite.spritecollide(self, iron_group, False)
        if iron_hit_list:
            self.rect.topleft = self.old_position
            
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.BULLET_COOLDOWN:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            bullets_fired = pygame.mixer.Sound("audios/fire.wav")
            bullets_fired.play()
            all_sprites.add(bullet)
            bullet_group.add(bullet) 
            player_bullet_group.add(bullet)
            self.last_shoot_time = current_time

    def hit(self):
        if not self.invulnerable:
            self.invulnerable = True
            self.invulnerable_timer = 300  

class EnemyTank(pygame.sprite.Sprite):

    def __init__(self,x) -> None:
        super().__init__()
        tank_img = pygame.image.load(os.path.join("img/enemyTank", "enemy_1_0.png")).convert()
        self.tank = tank_img
        self.image = self.tank.subsurface((0, 0), (48, 48))
        self.rect = self.image.get_rect()
        self.speed = 1
        self.direction = "DOWN"
        
        self.rect.top = random.randint(0, 400)
        self.rect.left = random.randint(0, 1000)
        
        self.step = 120
        FIRE_BULLET_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(FIRE_BULLET_EVENT, 1000)
        self.old_position = self.rect.topleft
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


    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
        all_sprites.add(bullet)
        enemy_bullet_group.add(bullet)
    
    def update(self):
        self.old_position = self.rect.topleft
        if self.step < 0:
            self.step = 50
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
        wall_hit_list = pygame.sprite.spritecollide(self, wall_group, False)
        if wall_hit_list:
            self.rect.topleft = self.old_position
        iron_hit_list = pygame.sprite.spritecollide(self, iron_group, False)
        if iron_hit_list:
            self.rect.topleft = self.old_position

#   墙
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, img_choice) -> None:
        super().__init__()
        self.images = ["img/scene/brick.png", "img/scene/brick1.png", "img/scene/brick2.png"]
        self.image = pygame.image.load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.img_choice = img_choice  # 使用self.img_choice

        if self.img_choice == 1:
            self.image = pygame.image.load(self.images[0])
        elif self.img_choice == 2:
            self.image = pygame.image.load(self.images[1])
        elif self.img_choice == 3:
            self.image = pygame.image.load(self.images[2])



    def update(self):
        for bullet in bullet_group:
            if self is not None and pygame.sprite.collide_circle(bullet, self):
                self.kill()
                bullet.kill()

        for bullet in enemy_bullet_group:
            if self is not None and pygame.sprite.collide_circle(bullet, self):
                self.kill()
                bullet.kill()

class Iron(pygame.sprite.Sprite):
    def __init__(self,enemy_tank_group) -> None:
        super().__init__()
        self.images = ("img/scene/iron.png")
        self.image = pygame.image.load(self.images)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(50, 1000)
        self.rect.centery = random.randint(0, WIDTH - self.rect.width)
        self.rect.inflate_ip(-10, -10)
        while True:
            self.rect.centerx = random.randint(50, 1000)
            self.rect.centery = random.randint(0, WIDTH - self.rect.width)
            if (not pygame.sprite.spritecollideany(self, enemy_tank_group) and 
                not pygame.sprite.collide_mask(self, player) and
                not pygame.sprite.collide_mask(self, player1)):
                break
    def update(self):
        for bullet in bullet_group:
            if self is not None and pygame.sprite.collide_circle(bullet,self):
                bullet.kill()

        for bullet in enemy_bullet_group:
            if self is not None and pygame.sprite.collide_circle(bullet,self):
                bullet.kill()

#   家
class Home(pygame.sprite.Sprite):
    def __init__(self,) -> None:
        super().__init__()
        self.image_png = 0
        self.images = ["img/home/home1.png","img/home/home1.png","img/home/home_destroyed.png"]
        self.image = pygame.image.load(self.images[self.image_png])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT -10
    def update(self):
        global Defeat
        for bullet in bullet_group:
            if pygame.sprite.collide_rect(bullet, self):
                Defeat = True
                bullet.kill()
                self.kill()
                pygame.display.flip()
        for bullet in enemy_bullet_group:
            if pygame.sprite.collide_rect(bullet, self):
                Defeat=  True
                bullet.kill()
                self.kill()

#   退出
class Exit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/exit/exit.png")
        self.image = pygame.transform.scale(self.image, (60, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, 20)
    def update(self):
        global screen
        global running
        for bullet in bullet_group:
            if pygame.sprite.collide_rect(bullet, self) and painted_eggshell:
                font = pygame.font.Font("font/simkai.ttf", 80)
                text = font.render("彩蛋！！！", True, (255, 255, 255))
                text_rect = text.get_rect(center = (WIDTH//2 , HEIGHT//2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                bullet.kill()
                pygame.time.wait(2000)
                running = False

#   定义精灵组
all_sprites = pygame.sprite.Group()
enemy_tank_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
iron_group = pygame.sprite.Group()

#   角色
player = Player()
player1 = Player1()
life = Life()
life1 = Life1()
exit = Exit()
home = Home()

#   将角色添加到精灵组
all_sprites.add(home)
all_sprites.add(life)
all_sprites.add(life1)
all_sprites.add(exit)
all_sprites.add(player)
all_sprites.add(player1)

#   角色数量
Number_of_enemies = 15
Number_of_walls = 20
Number_of_iron = 50

victory_music_played = False

#   定义墙的x，y坐标
wall_positions = [
    (540, 560),
    (540, 550),    # x, y坐标
    (540, 530),
    (520, 530),
    (500, 530),
    (480, 530),
    (460, 530),
    (440, 530),
    (440, 550),
    (440, 560),

]


#   创建多数量的角色，并用专用的精灵组
for i in range(Number_of_enemies):
    enemy = EnemyTank(i)
    enemy_tank_group.add(enemy)

for position in wall_positions:
    x, y = position
    wall = Wall(x, y, 2)
    wall_group.add(wall)

for s in range(Number_of_iron):
    iron = Iron(enemy_tank_group)
    iron_group.add(iron)

#  计时器
COUNT = pygame.USEREVENT +1
pygame.time.set_timer(COUNT,1000)

DEFEAT = pygame.USEREVENT +2
pygame.time.set_timer(DEFEAT,1000)



#   文字
font = pygame.font.Font("font/simkai.ttf", 35)

game_failed = font.render("失败", True, (255, 255, 255))
game_failed_race= game_failed.get_rect(center=(WIDTH // 2 ,HEIGHT // 2))

invincible_time = font.render("无敌时间", True, (255, 255, 255))
P2_invincible_time_race = invincible_time.get_rect(center=(930 , 100))

invincible_time = font.render("无敌时间", True, (255, 255, 255))
P1_invincible_time_race = invincible_time.get_rect(center=(70 , 100))

# 主循环开始
while running:

    # 如果 player 对象存在且处于无敌状态，则在 screen 上显示无敌时间
    if player and player.invulnerable:
        screen.blit(invincible_time, P1_invincible_time_race)

    # 如果 player1 对象存在且处于无敌状态，则在 screen 上显示无敌时间
    if player1 and player1.invulnerable:
        screen.blit(invincible_time, P2_invincible_time_race)

    # 更新整个pygame窗口
    pygame.display.flip()

    # 处理pygame事件
    for event in pygame.event.get():
        # 如果事件类型是退出，则停止运行
        if event.type == pygame.QUIT:
            running = False
        # 如果按下键盘按键
        elif event.type == pygame.KEYDOWN:
            # 如果按下的是'p'键，切换暂停状态，并在暂停状态中监听事件
            if event.key == pygame.K_p:
                paused = not paused
                while paused:
                    for e in pygame.event.get():
                        # 如果在暂停状态下再次按下'p'键，取消暂停
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                            paused = False
                        # 如果在暂停状态下收到退出事件，停止运行并取消暂停
                        elif e.type == pygame.QUIT:
                            running = False
                            paused = False
            # 如果player1存在且按下空格键，执行player1的射击方法
            elif player1 and event.key == pygame.K_SPACE:
                player1.shoot()
            # 如果player存在且按下'j'键，执行player的射击方法
            elif player and event.key == pygame.K_j:
                player.shoot()
        # 处理自定义事件1，敌人坦克射击
        elif event.type == pygame.USEREVENT + 1:
            for enemy in enemy_tank_group:
                enemy.shoot()
        # 处理鼠标按下事件，如果点击退出按钮，则停止运行
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if exit.rect.collidepoint(pos):
                running = False
        # 如果player和player1都不存在，且触发了自定义事件2，显示游戏失败画面并在3秒后停止运行
        elif player == None and player1 == None and event.type == pygame.USEREVENT + 2:
            screen.fill(BLACK)
            screen.blit(game_failed, game_failed_race)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

    # 如果游戏处于暂停状态，则跳过下面的逻辑
    if paused:
        continue

    # 检查敌人的子弹是否击中player，如果击中则进行相关处理
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

    # 检查敌人的子弹是否击中player1，如果击中则进行相关处理
    for bullet in enemy_bullet_group:
        if player1 is not None and pygame.sprite.collide_rect(bullet, player1):
            bullet.kill()
            if not player1.invulnerable and player1_life > 0:
                player1_life -= 1
                player1.rect.topleft = player1.initial_position
                player1.hit() 
            if player1_life == 0:
                player1.kill()
                player1 = None

    # 检查player的子弹是否击中敌人坦克，如果击中则创建爆炸效果并消灭敌人和子弹
    for bullet in player_bullet_group:
        enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_tank_group, True)
        if enemy_hit_list:
            enemy = enemy_hit_list[0]
            explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
            all_sprites.add(explosion)
            bullet.kill()
        bullet.update()

    # 如果游戏失败，显示失败消息并在3秒后清空屏幕并停止运行
    if Defeat == True:
        screen.fill(BLACK)
        font = pygame.font.Font("font/simkai.ttf", 80)
        text = font.render("被偷家了！", True, (255, 255, 255))
        text_rect = text.get_rect(center = (WIDTH//2 , HEIGHT//2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)    
        screen.fill(BLACK)
        running = False

    # 如果敌人坦克全部被消灭，播放胜利音效
    if len(enemy_tank_group) == 0 and not victory_music_played:
        print("Playing finish music")
        Finish_music = pygame.mixer.Sound("audios/Finish.wav")
        Finish_music.play()
        painted_eggshell= True
        victory_music_played = True

    # 更新所有游戏元素的状态
    all_sprites.update()

    # 清空屏幕背景为黑色
    screen.fill(BLACK)

    # 更新和绘制所有游戏元素组
    enemy_bullet_group.update()
    enemy_bullet_group.draw(screen)

    enemy_tank_group.update()
    enemy_tank_group.draw(screen)

    bullet_group.update()
    bullet_group.draw(screen)

    wall_group.update()
    wall_group.draw(screen)

    iron_group.update()
    iron_group.draw(screen)

    all_sprites.draw(screen)

    # 控制游戏运行速度
    clock.tick(FPS)

# 退出游戏
pygame.quit()

