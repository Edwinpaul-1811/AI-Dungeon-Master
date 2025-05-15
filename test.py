import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Load assets (placeholder square as player)
player_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
player_img.fill((0, 128, 255))

# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Dungeon Story")
clock = pygame.time.Clock()

# Player starting position
player_x, player_y = WIDTH // 2, HEIGHT // 2

# Movement velocity
vel = 4

# Main loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= vel
    if keys[pygame.K_s]:
        player_y += vel
    if keys[pygame.K_a]:
        player_x -= vel
    if keys[pygame.K_d]:
        player_x += vel

    # Draw player
    screen.blit(player_img, (player_x, player_y))

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
