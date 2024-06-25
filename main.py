import pygame
import math
import random

class Player:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.angle = 0
        self.health = 100

    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy

    def rotate(self, x, y):
        self.angle = math.atan2(y - self.pos[1], x - self.pos[0])

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, self.pos, 10)
        end_x = self.pos[0] + math.cos(self.angle) * 20
        end_y = self.pos[1] + math.sin(self.angle) * 20
        pygame.draw.line(screen, GREEN, self.pos, (end_x, end_y), 2)

class Enemy:
    SIZE = 20

    def __init__(self, x, y):
        self.pos = [x, y]

    def move_towards(self, target):
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.pos[0] += dx
        self.pos[1] += dy

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.pos[0] - self.SIZE // 2, self.pos[1] - self.SIZE // 2, self.SIZE, self.SIZE))

class Bullet:
    SPEED = 10

    def __init__(self, x, y, angle):
        self.pos = [x, y]
        self.dx = math.cos(angle) * self.SPEED
        self.dy = math.sin(angle) * self.SPEED

    def update(self):
        self.pos[0] += self.dx
        self.pos[1] += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.pos[0]), int(self.pos[1])), 3)

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pygame FPS")
        self.clock = pygame.time.Clock()
        
        self.player = Player(width // 2, height // 2)
        self.enemies = []
        self.bullets = []
        self.max_enemies = 5

    def spawn_enemy(self):
        if len(self.enemies) < self.max_enemies:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.enemies.append(Enemy(x, y))

    def shoot(self):
        self.bullets.append(Bullet(self.player.pos[0], self.player.pos[1], self.player.angle))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(0, -2)
        if keys[pygame.K_s]:
            self.player.move(0, 2)
        if keys[pygame.K_a]:
            self.player.move(-2, 0)
        if keys[pygame.K_d]:
            self.player.move(2, 0)

        self.spawn_enemy()

        for enemy in self.enemies:
            enemy.move_towards(self.player.pos)

        for bullet in self.bullets[:]:
            bullet.update()
            if not (0 <= bullet.pos[0] < self.width and 0 <= bullet.pos[1] < self.height):
                self.bullets.remove(bullet)

        self.check_collisions()

    def check_collisions(self):
        for enemy in self.enemies[:]:
            if math.hypot(enemy.pos[0] - self.player.pos[0], enemy.pos[1] - self.player.pos[1]) < Enemy.SIZE // 2 + 10:
                self.player.health -= 10
                self.enemies.remove(enemy)
            for bullet in self.bullets[:]:
                if math.hypot(enemy.pos[0] - bullet.pos[0], enemy.pos[1] - bullet.pos[1]) < Enemy.SIZE // 2 + 3:
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    break

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.draw_health()
        pygame.display.flip()

    def draw_health(self):
        pygame.draw.rect(self.screen, RED, (10, 10, self.player.health, 20))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    self.player.rotate(x, y)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.shoot()

            self.update()
            self.draw()
            self.clock.tick(60)

            if self.player.health <= 0:
                running = False

        pygame.quit()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

if __name__ == "__main__":
    game = Game(800, 600)
    game.run()