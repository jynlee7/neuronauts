import pygame
from player import Player
from enemy import Enemy
import random
import time

last_enemy_killed_time = None
next_round_delay = 3  # seconds

WIDTH, HEIGHT = 800, 600
FPS = 60

def spawn_enemies(round_number):
    num_enemies = round_number * 2 + 2
    return [Enemy(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), scale_factor=1.0 + 0.1 * round_number) for _ in range(num_enemies)]

pygame.init()
font = pygame.font.SysFont(None, 36)
current_round = 1
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Johnopocalypse")
clock = pygame.time.Clock()

player = Player(x=WIDTH//2, y=HEIGHT//2)
enemies = spawn_enemies(current_round)

running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    if keys[pygame.K_SPACE]:
        player.shoot()

    # Update
    player.update(enemies)
    for enemy in enemies:
        enemy.update(player)
    enemies = [enemy for enemy in enemies if enemy.is_alive()]
    if not enemies and last_enemy_killed_time is None:
        last_enemy_killed_time = time.time()
    elif last_enemy_killed_time is not None and time.time() - last_enemy_killed_time >= next_round_delay:
        current_round += 1
        enemies = spawn_enemies(current_round)
        last_enemy_killed_time = None

    # Draw
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    ammo_text = font.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (WIDTH - ammo_text.get_width() - 10, 10))
    round_text = font.render(f"Round: {current_round}", True, (255, 255, 255))
    screen.blit(round_text, (10, 10))

    pygame.display.flip()

pygame.quit()