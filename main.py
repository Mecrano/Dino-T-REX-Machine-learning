import sys
import pygame
from pygame.locals import *
from characters.dyno import Dyno
from characters.cactus import Cactuses

pygame.init()
pygame.display.set_caption('Dyno T-REX - Machine Learning')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
dyno = Dyno(screen)
cactuses = Cactuses(screen)
cactuses.run()
enemies = pygame.sprite.Group()
hero = pygame.sprite.Group()
hero.add(dyno)

def init():
    while (True):
        """ Get User intention of close game """
        for event in pygame.event.get(QUIT):
            if event.type == QUIT:
                cactuses.stop()
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            cactuses.stop()
            pygame.quit()
            sys.exit()

        for cactus in cactuses.cactuses:
            enemies.add(cactus)
        
        screen.fill((255, 255, 255))
        dyno.update()
        enemies.update()

        # collision = pygame.sprite.spritecollide(dyno, enemies, False)

        # if collision:
        #     print("collision")

        pygame.display.update()
        clock.tick(60)


init()
