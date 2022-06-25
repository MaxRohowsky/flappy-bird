import pygame
import os
import random
pygame.init()

# Global Constants
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))


# Images
bird = [pygame.image.load("assets/bird-down.png"),
        pygame.image.load("assets/bird-mid.png"),
        pygame.image.load("assets/bird-up.png")]
skyline = pygame.image.load("assets/background.png")
ground = pygame.image.load("assets/ground.png")
bottom_pipe_image = pygame.image.load("assets/pipe.png")
top_pipe_image = pygame.transform.rotate(bottom_pipe_image, 180)



pygame.display.set_caption("First Game")


class Pipe:
    def __init__(self):
        # Images
        self.bottom_pipe = bottom_pipe_image
        self.top_pipe = top_pipe_image
        # Position
        self.x = 500
        self.top_pipe_y = random.randint(-600, -480)
        self.delta = random.randint(90, 130)
        self.length = bottom_pipe_image.get_height()
        self.bottom_pipe_y = self.top_pipe_y + self.length + self.delta

    def update(self):
        self.x -= 2

    def draw(self, win):
        win.blit(self.top_pipe, (self.x, self.top_pipe_y))
        win.blit(self.bottom_pipe, (self.x, self.bottom_pipe_y))


class Background:
    def __init__(self):
        self.x = 0

    def update(self, image, y):
        window.blit(image, (self.x, y))
        window.blit(image, (win_width + self.x, y))
        if self.x == -win_width:
            window.blit(image, (win_width + self.x, 0))
            self.x = 0
        self.x -= 1





clock = pygame.time.Clock()
pipes = []
background = Background()
counter = 5

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((0, 0, 0))


    background.update(skyline, 0)


    for pipe in pipes:
        pipe.draw(window)
        pipe.update()

    background.update(ground, 510)


    if counter <= 0:
        pipes.append(Pipe())
        counter = random.randint(180, 300)
    counter -= 1



    window.blit(bird[0], (0, win_height // 2))

    clock.tick(100)
    pygame.display.update()