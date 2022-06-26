import pygame
import random

pygame.init()
clock = pygame.time.Clock()

# Window
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))

# Images
bird_images = [pygame.image.load("assets/bird-down.png"),
               pygame.image.load("assets/bird-mid.png"),
               pygame.image.load("assets/bird-up.png")]
skyline_image = pygame.image.load("assets/background.png")
ground_image = pygame.image.load("assets/ground.png")
top_pipe_image = pygame.image.load("assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")


class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y, image=bird_images[0]):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.flap = False
        self.flying = True
        self.vel = 0

    def update(self):
        if self.flying:
            self.vel += 0.5
            if self.vel > 7:
                self.vel = 7
            if self.rect.y < 520:
                self.rect.y += int(self.vel)
            if self.vel == 0:
                self.flap = False

        if user_input[pygame.K_SPACE] and not self.flap:
            self.flap = True
            self.vel = -7


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()


bird = pygame.sprite.Group()
bird.add(Bird(100, 100))
pipes = pygame.sprite.Group()
ground = pygame.sprite.Group()

x_pos_ground = 0
pipe_timer = 0
scroll_speed = 1
ground.add(Ground(x_pos_ground, 520), Ground(win_width + x_pos_ground, 520))


run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    window.fill((0, 0, 0))

    window.blit(skyline_image, (0, 0))

    user_input = pygame.key.get_pressed()

    pipes.update()
    pipes.draw(window)

    ground.update()
    ground.draw(window)

    bird.update()
    bird.draw(window)

    if len(ground) == 1:
        ground.add(Ground(win_width, 520))

    if pipe_timer <= 0:
        x_top, x_bottom = 550, 550
        y_top = random.randint(-600, -480)
        y_bottom = y_top + random.randint(90, 130) + bottom_pipe_image.get_height()
        pipes.add(Pipe(x_top, y_top, top_pipe_image))
        pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image))
        pipe_timer = random.randint(180, 250)
    pipe_timer -= 1

    clock.tick(60)
    pygame.display.update()
