from asyncio.windows_events import NULL
from pygame.locals import *
import pygame
import random
from threading import Timer

class Cactus(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.x = screen.get_width()
        self.y = 640
        self.h = 30
        self.w = 60
        self.acc = 3.5

    def update(self):
        self.x -= self.acc
        self.draw()
    
    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.x, self.y, self.w, self.h))

class Cactuses:
    def __init__(self, screen):
        self.screen = screen
        self.cactuses = []
        self.can_run = True
        self.t = False

    def stop(self):
        self.run = False
        if self.t:
            self.t.cancel()

    def run(self):
        self.generate_new_cactus()
        if self.can_run:
            secs = random.uniform(1.5, 5.0)
            self.t = Timer(secs, self.run)
            self.t.start()

    def update(self):
        self.remove_outside_window()

        for cactus in self.cactuses:
            cactus.update()

    def outside_cactus(self, cactus):
        if cactus.x < cactus.w * -1:
            cactus.kill()
            return False
        
        return True

    def remove_outside_window(self):
        self.cactuses = list(filter(self.outside_cactus, self.cactuses))


    def generate_new_cactus(self):
        print("Create new cactus")
        cactus = Cactus(self.screen)
        self.cactuses.append(cactus)