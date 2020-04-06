import pygame
import neat
import time
import os
import random
pygame.font.init()

WIDTH = 540
HEIGHT = 960

# Increase the size of images
BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird3.png")))]
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "pipe.png")))
BASE = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "base.png")))
BG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

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

        dist = self.vel*self.tick_count + 1.5*self.tick_count**2

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

    # Win = Window
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
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.a, self.b)).center)
        win.blit(rotated_image, new_rect.topleft)

# Mask can detect pixel, it returns list
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


    # Blit means draw

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, a):
        self.a = a
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE, False, True)
        self.PIPE_BOTTOM = PIPE

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(40,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.a -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.a, self.top))
        win.blit(self.PIPE_BOTTOM, (self.a, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.a - bird.a, self.top - round(bird.b))
        bottom_offset = (self.a - bird.a, self.bottom - round(bird.b))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # Returns none if doesn't collide
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VEL = 5     # Always same as PIPE
    WIDTH = BASE.get_width()
    IMG = BASE

    def __init__(self, b):
        self.b = b
        self.a1 = 0
        self.a2 = self.WIDTH

# Use two images so base looks continuous. First image on screen and second image behind it.
    def move(self):
        self.a1 -= self.VEL
        self.a2 -= self.VEL

        if self.a1 + self.WIDTH < 0:
            self.a1 = self.a2 + self.WIDTH

        if self.a2 + self.WIDTH < 0:
            self.a2 = self.a1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.a1, self.b))
        win.blit(self.IMG, (self.a2, self.b))


def draw_window(win, bird, pipes, base, score):
    win.blit(BG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move()

        add_pipe = False
        rem = []
        for pipe in pipes:
            # Check the collision with bird
            if pipe.collide(bird):
                pass

            # Check if pipe is visible on screen
            if pipe.a + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            # Check if we have pass the pipe
            if not pipe.passed and pipe.a < bird.a:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(550))

        for r in rem:
            pipes.remove(r)

        if bird.b + bird.img.get_height() >= 730:
            pass

        base.move()
        draw_window(win, bird, pipes, base, score)
    pygame.quit()
    quit()


main()
