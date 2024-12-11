import pygame
import random
import sys

# Pygame initialization
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Create window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize snake, food, direction, and score
snake_pos = [(200, 200)]
food_pos = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
            random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
direction = 'RIGHT'
score = 0

# Function to draw the game
def draw_game():
    win.fill(WHITE)

    # Draw the snake
    for segment in snake_pos:
        pygame.draw.rect(win, RED, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw the food
    pygame.draw.rect(win, GREEN, (food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw the score
    font = pygame.font.SysFont('arial', 25)
    score_surface = font.render(f'Score: {score}', True, BLACK)
    win.blit(score_surface, (10, 10))

    pygame.display.update()

# Function to check if food is eaten
def is_food_eaten():
    return snake_pos[0] == food_pos

# Function to spawn food
def spawn_food():
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_position = (x, y)
        if food_position not in snake_pos:  # Ensure the food doesn't spawn on the snake
            return food_position

# Function to handle key presses
def handle_keys():
    global direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != 'DOWN':
        direction = 'UP'
    elif keys[pygame.K_DOWN] and direction != 'UP':
        direction = 'DOWN'
    elif keys[pygame.K_LEFT] and direction != 'RIGHT':
        direction = 'LEFT'
    elif keys[pygame.K_RIGHT] and direction != 'LEFT':
        direction = 'RIGHT'

# Function to show the game over screen
def show_game_over():
    font = pygame.font.SysFont('arial', 50)
    game_over_surface = font.render('Game Over!', True, BLACK)
    score_surface = font.render(f'Final Score: {score}', True, BLACK)
    win.fill(WHITE)
    win.blit(game_over_surface, (WIDTH // 4, HEIGHT // 3))
    win.blit(score_surface, (WIDTH // 4, HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(2000)  # Wait for 2 seconds before quitting
    pygame.quit()
    sys.exit()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    handle_keys()
    
    # Calculate the new head position
    head_x, head_y = snake_pos[0]
    if direction == 'UP':
        head_y -= BLOCK_SIZE
    elif direction == 'DOWN':
        head_y += BLOCK_SIZE
    elif direction == 'LEFT':
        head_x -= BLOCK_SIZE
    elif direction == 'RIGHT':
        head_x += BLOCK_SIZE

    # Check for wall collision
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        show_game_over()

    # Update the snake's position
    new_head = (head_x, head_y)
    
    # Add new head to the snake
    snake_pos.insert(0, new_head)

    # Check if food is eaten
    if is_food_eaten():
        score += 1  # Increment score
        food_pos = spawn_food()  # Spawn new food
    else:
        snake_pos.pop()  # Remove the last segment if no food is eaten

    # Check for self-collision
    if snake_pos[0] in snake_pos[1:]:
        show_game_over()

    draw_game()
    pygame.time.delay(100)  # Control the game speed