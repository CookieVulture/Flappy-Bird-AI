import pygame
import neat
import time
import os
import random

WIDTH = 720
HEIGHT = 1080

# Increase the size of images
BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird3.png")))]
PIPE = [pygame.transform.scale2x(pygame.image.load(os.path.join("img", "pipe.png")))]
BASE = [pygame.transform.scale2x(pygame.image.load(os.path.join("img", "base.png")))]
BG = [pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bg.png")))]


class Bird:
    IMGS = BIRD
    MAX_ROTATION = 25       # Tilt of Bird
    ROT_VEL = 20            # Rotate in each frame
    ANIMATION_TIME = 5      # Time

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.tilt = 0   # how much image tilted
        self.tick_count = 0
        self.vel = 0
        self.height = self.a
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0     # Count for last jump
        self.height = self.b

    def move(self):
        self.tick_count += 1

        dist = self.vel*self.tick_count + 1.5*self.tick_count**2       # x = ut +

        if dist >= 16:
            dist = 16
        if dist < 0:
            dist -= 2           # Jump

        self.b = self.b + dist

        if dist < 0 or self.b < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # This is how to rotate image in pygame
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topLeft=(self.a, self.b)).center)
        win.blit(rotated_image, new_rect.topLeft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


