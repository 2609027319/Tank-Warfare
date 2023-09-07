import pygame
from copying import *
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