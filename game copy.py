import pygame
import sys
import os
from pyswip import Prolog
import json

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 500
TILE_SIZE = 32
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Setup game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Dungeon Story")
clock = pygame.time.Clock()

# Load assets directory and images
assets_dir = "assets"

def load_image(name):
    path = os.path.join(assets_dir, name)
    if not os.path.isfile(path):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        if name == "wall.png":
            surf.fill((100, 100, 100))
        elif name == "floor.png":
            surf.fill((220, 220, 220))
        elif name == "player.png":
            surf.fill((0, 128, 255))
        pygame.image.save(surf, path)
    return pygame.image.load(path).convert_alpha()

player_img = load_image("player.png")
floor_img = load_image("floor.png")
wall_img = load_image("wall.png")

# Load story and Prolog
with open("story.json") as f:
    story = json.load(f)

prolog = Prolog()
prolog.consult("logic.pl")

def get_next(current, choice):
    query = f"path('{current}', '{choice}', Next)."
    result = list(prolog.query(query))
    return result[0]["Next"] if result else None

def is_ending(state):
    result = list(prolog.query(f"ending({state})."))
    return bool(result)

# Floors folder
floors_dir = "floors"

def load_floor_from_path(path):
    with open(path, "r") as f:
        return [list(line.strip()) for line in f if line.strip()]

def set_current_state(state):
    global current_state, tilemap
    current_state = state
    map_path = os.path.join(floors_dir, f"floor_{state}.txt")
    if os.path.isfile(map_path):
        tilemap[:] = load_floor_from_path(map_path)
        print(f"Loaded map for state: {state}")
    else:
        print(f"No map found for state: {state}, using current map")

# Set initial state
current_state = "start"
tilemap = load_floor_from_path(os.path.join(floors_dir, f"floor_{current_state}.txt"))
if tilemap is None:
    sys.exit("Initial floor map not found!")

# Player position
player_tile_x, player_tile_y = 1, 1
player_px = player_tile_x * TILE_SIZE
player_py = player_tile_y * TILE_SIZE

move_x = 0
move_y = 0
vel = 4

font = pygame.font.SysFont("Arial", 16, True, True)

def draw_dialog(prompt, options):
    pygame.draw.rect(screen, BLACK, (10, HEIGHT - 110, WIDTH - 20, 100))
    pygame.draw.rect(screen, WHITE, (12, HEIGHT - 108, WIDTH - 24, 96))
    y = HEIGHT - 100
    lines = [prompt] + [f"[{i+1}] {opt}" for i, opt in enumerate(options)]
    for line in lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (20, y))
        y += 20

def draw_instructions():
    lines = [
        "Instructions:",
        "Move: WASD or Arrow Keys",
        "Interact: E",
        "Doors (D) move you to next floor",
        "Press number keys [1-9] to select options"
    ]
    y = 385
    for line in lines:
        text = font.render(line, True, RED)
        screen.blit(text, (10, y))
        y += 20

choice_made = False
initial_pos = (player_tile_x, player_tile_y)
instruction_display = True

def can_move(x, y):
    if y < 0 or y >= len(tilemap) or x < 0 or x >= len(tilemap[0]):
        return False
    return tilemap[y][x] in ['.', 'D']

# Buttons
def draw_button(text, x, y, width, height, color, action=None):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.SysFont("Arial", 20, True)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height)

def reset_game():
    global current_state, tilemap, player_tile_x, player_tile_y, player_px, player_py, move_x, move_y, choice_made, instruction_display
    current_state = "start"
    tilemap = load_floor_from_path(os.path.join(floors_dir, f"floor_{current_state}.txt"))
    player_tile_x, player_tile_y = 1, 1
    player_px = player_tile_x * TILE_SIZE
    player_py = player_tile_y * TILE_SIZE
    move_x = 0
    move_y = 0
    choice_made = False
    instruction_display = True

# Main game loop
running = True
game_over = False
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    if game_over:
        draw_button("Restart", WIDTH // 2 - 75, HEIGHT // 2 - 25, 150, 50, RED)
        restart_button = draw_button("Restart", WIDTH // 2 - 75, HEIGHT // 2 - 25, 150, 50, RED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    reset_game()
                    game_over = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()
                game_over = False
        pygame.display.flip()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if choice_made:
                keys = list(story[current_state]["options"].keys())
                if pygame.K_1 <= event.key <= pygame.K_9:
                    idx = event.key - pygame.K_1
                    if idx < len(keys):
                        choice = keys[idx]
                        next_state = get_next(current_state, choice)
                        if next_state:
                            set_current_state(next_state)
                            choice_made = False
                            if is_ending(current_state):
                                print("Game ended at:", current_state)
                                game_over = True
                        else:
                            print("Invalid choice.")
            elif move_x == 0 and move_y == 0:
                if event.key in (pygame.K_w, pygame.K_UP) and can_move(player_tile_x, player_tile_y - 1):
                    move_y = -TILE_SIZE
                elif event.key in (pygame.K_s, pygame.K_DOWN) and can_move(player_tile_x, player_tile_y + 1):
                    move_y = TILE_SIZE
                elif event.key in (pygame.K_a, pygame.K_LEFT) and can_move(player_tile_x - 1, player_tile_y):
                    move_x = -TILE_SIZE
                elif event.key in (pygame.K_d, pygame.K_RIGHT) and can_move(player_tile_x + 1, player_tile_y):
                    move_x = TILE_SIZE
                elif event.key == pygame.K_e:
                    choice_made = True

    if move_x != 0:
        step = vel if move_x > 0 else -vel
        player_px += step
        move_x -= step
        if move_x == 0:
            player_tile_x = player_px // TILE_SIZE

    elif move_y != 0:
        step = vel if move_y > 0 else -vel
        player_py += step
        move_y -= step
        if move_y == 0:
            player_tile_y = player_py // TILE_SIZE

    distance = abs(player_tile_x - initial_pos[0]) + abs(player_tile_y - initial_pos[1])
    if distance >= 2:
        instruction_display = False

    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == 'W':
                screen.blit(wall_img, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == '.':
                screen.blit(floor_img, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == 'D':
                pygame.draw.rect(screen, (255, 215, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    screen.blit(player_img, (player_px, player_py))

    if instruction_display:
        draw_instructions()

    if choice_made:
        scene = story[current_state]
        draw_dialog(scene["prompt"], list(scene["options"].keys()))

    pygame.display.flip()

pygame.quit()
sys.exit()
