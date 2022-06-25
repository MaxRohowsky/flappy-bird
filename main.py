import pygame
import os
import random
pygame.init()

# Global Constants
win_height =720
win_width =551
window = pygame.display.set_mode((win_width, win_height))


# Images
bird_images = [pygame.image.load("assets/bird-down.png"),
        pygame.image.load("assets/bird-mid.png"),
        pygame.image.load("assets/bird-up.png")]
skyline_image = pygame.image.load("assets/background.png")
ground_image = pygame.image.load("assets/ground.png")
bottom_pipe_image = pygame.image.load("assets/pipe.png")
top_pipe_image = pygame.transform.rotate(bottom_pipe_image, 180)




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
        self.x -= 1

    def draw(self, win):
        win.blit(self.top_pipe, (self.x, self.top_pipe_y))
        win.blit(self.bottom_pipe, (self.x, self.bottom_pipe_y))







clock = pygame.time.Clock()
pipes = []
x=0
counter = 5


run = True
while run:
    # Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    window.fill((0, 0, 0))


    # Skyline Background
    window.blit(skyline_image, (0,0))
    userInput = pygame.key.get_pressed()



    for pipe in pipes:
        pipe.draw(window)
        pipe.update()

    # Ground
    window.blit(ground_image, (x, 520))
    window.blit(ground_image, (win_width + x, 520))
    if x == -win_width:
        window.blit(ground_image, (win_width + x, 0))
        x = 0
    x -= 1


    if counter <= 0:
        pipes.append(Pipe())
        counter = random.randint(180, 300)
    counter -= 1





    clock.tick(100)
    pygame.display.update()