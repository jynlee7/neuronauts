import pygame

class Enemy:
    base_image = pygame.image.load("assets/hamsterjohn.png")
    def __init__(self, x, y, scale_factor=1.0):
        self.x, self.y = x, y
        scale_size = int(50 * scale_factor)
        self.image = pygame.transform.scale(self.base_image, (scale_size, scale_size))
        self.speed = 2
        self.rect = self.image.get_rect(center=(x, y))
        self.max_health = 3
        self.health = self.max_health

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max((dx**2 + dy**2) ** 0.5, 1)
        self.x += self.speed * dx / dist
        self.y += self.speed * dy / dist
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # Draw health bar
        bar_width = self.rect.width
        bar_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 10, bar_width * health_ratio, bar_height))

    def is_alive(self):
        return self.health > 0
    