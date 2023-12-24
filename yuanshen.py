import pygame
import subprocess
pygame.init()


subprocess.run(['cmd', '/c', 'start', 'D:\\yuanshen.lnk'])

screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Full Screen White Window')
WHITE = (255, 255, 255)
start_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）

running1 = True
while running1:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running1 = False
                    screen.fill(WHITE)
                    pygame.display.flip()
                    elapsed_time = pygame.time.get_ticks() - start_time  # 获取经过的时间
                    if elapsed_time >= 15000:  # 15000毫秒等于15秒
                        running1 = False


