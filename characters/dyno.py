from pygame.locals import *
import pygame
import os


def load_image(
    name,
    sx=-1,
    sy=-1,
    colorkey=None,
):

    fullname = os.path.join('sprites', name)
    img = pygame.image.load(fullname)
    img = img.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, RLEACCEL)

    if sx != -1 or sy != -1:
        img = pygame.transform.scale(img, (sx, sy))

    return (img, img.get_rect())


def load_sprite_sheet(
        s_name,
        namex,
        scx=-1,
        scy=-1,
        c_key=-1,
):
    fullname = os.path.join('sprites', s_name)
    sh = pygame.image.load(fullname)
    sh = sh.convert()

    sh_rect = sh.get_rect()

    sprites = []

    sx = sh_rect.width / namex
    sy = sh_rect.height / 1

    for i in range(0, 1):
        for j in range(0, namex):
            rect = pygame.Rect((j*sx, i*sy, sx, sy))
            img = pygame.Surface(rect.size)
            img = img.convert()
            img.blit(sh, (0, 0), rect)

            if c_key is not None:
                if c_key == -1:
                    c_key = img.get_at((0, 0))
                img.set_colorkey(c_key, RLEACCEL)

            if scx != -1 or scy != -1:
                img = pygame.transform.scale(img, (scx, scy))

            sprites.append(img)

    return sprites


class Dyno(pygame.sprite.Sprite):
    def __init__(self, screen, sx=80, sy=90):
        super().__init__()
        self.imgs = load_sprite_sheet('dino.png', 5, sx, sy)
        self.imgs1 = load_sprite_sheet('dino_ducking.png', 2, 59, sy)
        self.image = self.imgs[0]
        self.screen = screen
        self.jump_acc = 12
        self.can_jump = True
        self.last_jump = pygame.time.get_ticks()
        self.jump_cool_down = 500
        self.init_position = {
            "x": 50,
            "y": 580,
            "w": 83,
            "h": 90,
        }

        self.rect = pygame.Rect(self.init_position["x"], self.init_position["y"], self.init_position["w"], self.init_position["h"])

    def update(self):
        self.movement()
        self.draw()

    def return_to_original_position(self):
        if self.rect.height < self.init_position["h"]:
            self.rect.height += self.jump_acc
        if self.rect.height > self.init_position["h"]:
            self.rect.height -= self.jump_acc

        if self.rect.left < self.init_position["x"]:
            self.rect.left += self.jump_acc
        if self.rect.left > self.init_position["x"]:
            self.rect.left -= self.jump_acc

        if self.rect.top < self.init_position["y"]:
            self.rect.top += self.jump_acc
        if self.rect.top > self.init_position["y"]:
            self.rect.top -= self.jump_acc

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def movement(self):
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get(KEYUP):
            if event.key == K_UP:
                self.can_jump = False

        if self.rect.top == self.init_position["y"]:
            now = pygame.time.get_ticks()
            if now - self.last_jump >= self.jump_cool_down:
                self.last_jump = now
                self.can_jump = True
        elif self.rect.top == (self.init_position["y"] - (self.init_position["h"] * 2)):
            pygame.time.delay(100)
            self.can_jump = False

        if pressed_keys[K_DOWN]:
            if self.rect.top < (self.init_position["y"] + (self.init_position["h"] / 2)):
                self.rect.top += self.jump_acc
            if self.rect.height > (self.init_position["h"] / 2):
                self.rect.height -= self.jump_acc
        elif pressed_keys[K_UP] and self.can_jump:
            if self.rect.top >= (self.init_position["y"] - (self.init_position["h"] * 2)):
                self.rect.top -= self.jump_acc
        else:
            self.return_to_original_position()
