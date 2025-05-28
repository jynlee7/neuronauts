import pygame
import time

class Player:
    textures = {
        1: pygame.transform.scale(pygame.image.load("assets/johnsprite.png"), (50, 50)),
        2: pygame.transform.scale(pygame.image.load("assets/evojohn.png"), (50, 50)),
    }
    bullets = {
        1: pygame.transform.scale(pygame.image.load("assets/bullet1.png"), (16, 32)),
        2: pygame.transform.scale(pygame.image.load("assets/bullet2.png"), (16, 32))
    }

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.level = 1
        self.image = self.textures[self.level]
        self.bullet_img = Player.bullets[self.level]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4
        self.bullets = []
        self.cooldown = 0
        self.direction = (0, -1)
        self.ammo = 10

    def handle_input(self, keys):
        if keys[pygame.K_e]:
            self.evolve()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1
        if dx != 0 or dy != 0:
            self.direction = (dx, dy)
            self.x += dx * self.speed
            self.y += dy * self.speed

    def evolve(self):
        if self.level < 2:
            self.level += 1
            self.image = self.textures[self.level]
            self.speed += 1
            self.bullet_img = Player.bullets[self.level]

    def update(self, enemies):
        global last_enemy_killed_time
        self.rect.center = (self.x, self.y)
        if self.cooldown > 0:
            self.cooldown -= 1
        for bullet in self.bullets[:]:
            bullet["rect"].x += bullet["direction"][0] * bullet["speed"]
            bullet["rect"].y += bullet["direction"][1] * bullet["speed"]
            for enemy in enemies[:]:
                if bullet["rect"].colliderect(enemy.rect):
                    enemy.health -= bullet["damage"]
                    self.bullets.remove(bullet)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        self.ammo += 5
                        if not enemies:
                            last_enemy_killed_time = time.time()
                    break
            else:
                if bullet["rect"].bottom < 0:
                    self.bullets.remove(bullet)

    def shoot(self):
        if self.ammo > 0 and self.cooldown == 0:
            dx, dy = self.direction
            bullet_rect = self.bullet_img.get_rect(center=(self.x + dx * 25, self.y + dy * 25))
            mag = max((dx ** 2 + dy ** 2) ** 0.5, 1e-6)
            norm_dir = (dx / mag, dy / mag)
            bullet = {
                "rect": bullet_rect,
                "img": self.bullet_img,
                "speed": 10,
                "direction": norm_dir,
                "damage": 1
            }
            self.bullets.append(bullet)
            self.ammo -= 1
            self.cooldown = 15

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            surface.blit(bullet["img"], bullet["rect"])