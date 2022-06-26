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
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.flap = False
        self.vel = 0
        self.image_index = 0
        self.alive = True

    def update(self):
        # Animate Bird
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = bird_images[self.image_index // 10]

        # Rotate Bird
        self.image = pygame.transform.rotate(self.image, self.vel * -7)

        # Gravity and Flap
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 520:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # User Input
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
player = Bird(100, 100)
bird.add(player)
pipes = pygame.sprite.Group()
ground = pygame.sprite.Group()

x_pos_ground = 0
pipe_timer = 0
scroll_speed = 1
ground.add(Ground(x_pos_ground, 520), Ground(win_width + x_pos_ground, 520))

run = True
while run:
    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Reset Frame
    window.fill((0, 0, 0))

    # User Input
    if player.alive:
        user_input = pygame.key.get_pressed()

    # Draw Background
    window.blit(skyline_image, (0, 0))

    # Pipes, Ground, and Bird
    pipes.draw(window)
    ground.draw(window)
    bird.draw(window)

    if player.alive:
        pipes.update()
        ground.update()
    bird.update()

    # Collision Detection
    collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
    collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
    if collision_pipes or collision_ground:
        print('collision')
        player.alive = False

    # Spawn Ground
    if len(ground) == 1:
        ground.add(Ground(win_width, 520))

    # Spawn Pipes
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
