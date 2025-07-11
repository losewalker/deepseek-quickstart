import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
GRAY = (200, 200, 200)

# Screen dimensions
DIS_WIDTH = 600
DIS_HEIGHT = 400

# Game settings
SNAKE_BLOCK = 10
INITIAL_SPEED = 15
SPEED_OPTIONS = [10, 15, 20, 25]  # Easy, Medium, Hard, Extreme

# Initialize display
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game')

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
title_font = pygame.font.SysFont("comicsansms", 50)

# Game states
MENU = 0
GAME = 1
SETTINGS = 2
GAME_OVER = 3


# Draw grid background
def draw_grid():
    for x in range(0, DIS_WIDTH, SNAKE_BLOCK):
        pygame.draw.line(dis, GRAY, (x, 0), (x, DIS_HEIGHT))
    for y in range(0, DIS_HEIGHT, SNAKE_BLOCK):
        pygame.draw.line(dis, GRAY, (0, y), (DIS_WIDTH, y))


# Display score
def display_score(score):
    value = score_font.render("Score: " + str(score), True, BLACK)
    dis.blit(value, [0, 0])


# Draw snake
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])


# Display message
def display_message(msg, color, y_displace=0, size="small"):
    if size == "small":
        text_surface = font_style.render(msg, True, color)
    elif size == "medium":
        text_surface = score_font.render(msg, True, color)
    else:  # large
        text_surface = title_font.render(msg, True, color)

    text_rect = text_surface.get_rect(center=(DIS_WIDTH / 2, DIS_HEIGHT / 2 + y_displace))
    dis.blit(text_surface, text_rect)


# Main menu
def show_menu():
    dis.fill(WHITE)
    draw_grid()
    display_message("SNAKE GAME", GREEN, -100, "large")
    display_message("Press SPACE to Start", BLACK, -30)
    display_message("Press S for Settings", BLACK, 10)
    display_message("Press Q to Quit", BLACK, 50)
    pygame.display.update()


# Settings menu
def show_settings(current_speed_idx):
    dis.fill(WHITE)
    draw_grid()
    display_message("SETTINGS", BLUE, -100, "large")

    # Difficulty options
    difficulties = ["Easy", "Medium", "Hard", "Extreme"]
    for i, (diff, speed) in enumerate(zip(difficulties, SPEED_OPTIONS)):
        color = GREEN if i == current_speed_idx else BLACK
        display_message(f"{diff}: Speed {speed}", color, -30 + i * 40)

    display_message("Press UP/DOWN to change", BLACK, 120)
    display_message("Press ENTER to confirm", BLACK, 160)
    pygame.display.update()


# Game over screen
def show_game_over(score):
    dis.fill(WHITE)
    draw_grid()
    display_message("GAME OVER", RED, -100, "large")
    display_message(f"Your Score: {score}", BLACK, -30)
    display_message("Press SPACE to Play Again", BLACK, 30)
    display_message("Press M for Main Menu", BLACK, 80)
    pygame.display.update()


# Main game loop
def game_loop(speed):
    game_pause = False
    game_state = GAME

    # Snake initial position
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    # Snake movement
    x1_change = 0
    y1_change = 0

    # Snake body
    snake_list = []
    snake_length = 1

    # Food position
    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while game_state == GAME:
        # Handle pause state
        while game_pause:
            dis.fill(WHITE)
            draw_grid()
            display_message("PAUSED", BLUE, -50, "medium")
            display_message("Press C to Continue", BLACK, 0)
            display_message("Press Q to Quit", BLACK, 40)
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = MENU
                    game_pause = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_state = MENU
                        game_pause = False
                    if event.key == pygame.K_c:
                        game_pause = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = MENU
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != SNAKE_BLOCK:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -SNAKE_BLOCK:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != SNAKE_BLOCK:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -SNAKE_BLOCK:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_p:  # Pause game
                    game_pause = True

        # Check wall collision
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_state = GAME_OVER

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Draw everything
        dis.fill(WHITE)
        draw_grid()
        pygame.draw.rect(dis, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        # Update snake body
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check self collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_state = GAME_OVER

        draw_snake(snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        # Check food collision
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            snake_length += 1

        clock.tick(speed)

    return snake_length - 1  # Return final score


# Main function
def main():
    current_state = MENU
    speed_idx = 1  # Default to Medium difficulty
    score = 0

    while True:
        if current_state == MENU:
            show_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_state = GAME
                    elif event.key == pygame.K_s:
                        current_state = SETTINGS
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        elif current_state == SETTINGS:
            show_settings(speed_idx)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        speed_idx = max(0, speed_idx - 1)
                    elif event.key == pygame.K_DOWN:
                        speed_idx = min(len(SPEED_OPTIONS) - 1, speed_idx + 1)
                    elif event.key == pygame.K_RETURN:
                        current_state = MENU

        elif current_state == GAME:
            score = game_loop(SPEED_OPTIONS[speed_idx])
            current_state = GAME_OVER

        elif current_state == GAME_OVER:
            show_game_over(score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_state = GAME
                    elif event.key == pygame.K_m:
                        current_state = MENU

        pygame.time.delay(50)


if __name__ == "__main__":
    main()