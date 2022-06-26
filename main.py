import pygame
import random
from sys import exit

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
game_over_image = pygame.image.load("assets/gameover.png")
start_image = pygame.image.load("assets/start.png")

# Game
scroll_speed = 1
game_over = True
score = 0


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

    def update(self, user_input):
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
        if user_input[pygame.K_SPACE] and not self.flap and self.alive:
            self.flap = True
            self.vel = -7


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.passed = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        global score
        print(score)
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()
        # if self.rect.x == 100 and not self.passed:
        #     score += 1
        #     self.passed = True


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


def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def main():
    bird = pygame.sprite.Group()
    player = Bird(100, 250)
    bird.add(player)
    pipes = pygame.sprite.Group()
    ground = pygame.sprite.Group()
    x_pos_ground = 0
    pipe_timer = 0

    ground.add(Ground(x_pos_ground, 520), Ground(win_width + x_pos_ground, 520))

    run = True
    while run:
        # Quit
        quit_game()

        # Reset Frame
        window.fill((0, 0, 0))

        # User Input
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
        bird.update(user_input)

        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            player.alive = False
            if collision_ground:
                window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                              win_height // 2 - game_over_image.get_height() // 2))
                if user_input[pygame.K_SPACE]:
                    break

        # Spawn Ground
        if len(ground) == 1 and player.alive:
            ground.add(Ground(win_width, 520))

        # Spawn Pipes
        if pipe_timer <= 0 and player.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipe_image))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        clock.tick(60)
        pygame.display.update()


def menu():
    global game_over

    while game_over:
        quit_game()
        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        window.blit(ground_image, Ground(0, 520))
        window.blit(ground_image, Ground(0, 520))
        window.blit(bird_images[0], (100, 250))
        window.blit(start_image, (win_width // 2 - game_over_image.get_width() // 2,
                            win_height // 2 - game_over_image.get_height() // 2))
        user_input = pygame.key.get_pressed()

        if user_input[pygame.K_SPACE]:
            main()

        pygame.display.update()


menu()
