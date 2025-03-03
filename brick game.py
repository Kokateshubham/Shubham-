import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('BRICK BREAKER')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game constants
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_SIZE = 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
BRICK_COLOR = BLUE
PADDLE_COLOR = GREEN
BALL_COLOR = RED

# Game states
MAIN_MENU, RUNNING, GAME_OVER, WIN, HOW_TO_PLAY = "MAIN_MENU", "RUNNING", "GAME_OVER", "WIN", "HOW_TO_PLAY"

# Create a paddle
def draw_paddle(paddle_x):
    pygame.draw.rect(SCREEN, PADDLE_COLOR, (paddle_x, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))

# Create a ball
def draw_ball(ball_x, ball_y):
    pygame.draw.circle(SCREEN, BALL_COLOR, (ball_x, ball_y), BALL_SIZE)

# Create bricks
def draw_bricks(bricks):
    for brick in bricks:
        pygame.draw.rect(SCREEN, BRICK_COLOR, brick)

# Display text
def display_message(text, size, color, position):
    font = pygame.font.SysFont('Arial', size)
    label = font.render(text, True, color)
    SCREEN.blit(label, position)

# Display time
def display_time(elapsed_time):
    font = pygame.font.SysFont('Arial', 24)
    time_text = font.render(f"Time: {elapsed_time:.1f} s", True, BLACK)
    SCREEN.blit(time_text, (WIDTH - 150, 10))

# Show main menu
def show_main_menu():
    SCREEN.fill(WHITE)
    display_message("Brick Breaker", 48, BLACK, (WIDTH // 4, HEIGHT // 4))
    display_message("1. Start Game", 36, BLACK, (WIDTH // 4, HEIGHT // 4 + 80))
    display_message("2. How to Play", 36, BLACK, (WIDTH // 4, HEIGHT // 4 + 140))
    display_message("3. Quit", 36, BLACK, (WIDTH // 4, HEIGHT // 4 + 200))
    pygame.display.flip()

# Show How to Play screen
def show_how_to_play():
    SCREEN.fill(WHITE)
    display_message("How to Play", 48, BLACK, (WIDTH // 4, HEIGHT // 4))
    display_message("Use Left and Right arrow keys to move the paddle.", 24, BLACK, (WIDTH // 4 - 50, HEIGHT // 4 + 80))
    display_message("Break all the bricks without letting the ball fall.", 24, BLACK, (WIDTH // 4 - 50, HEIGHT // 4 + 120))
    display_message("Press 'M' to return to Main Menu", 24, BLACK, (WIDTH // 4, HEIGHT // 4 + 200))
    pygame.display.flip()

# Generate bricks for levels
def generate_bricks(level):
    rows = 5 + level  # Increase the number of rows as the level increases
    cols = 8
    bricks = [pygame.Rect(c * (BRICK_WIDTH + 10) + 35, r * (BRICK_HEIGHT + 10) + 35, BRICK_WIDTH, BRICK_HEIGHT)
              for r in range(rows) for c in range(cols)]
    return bricks

# Main game loop
def main():
    clock = pygame.time.Clock()
    game_state = MAIN_MENU
    level = 1
    score = 0
    paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = 4, -4
    start_time = 0

    bricks = generate_bricks(level)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == MAIN_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_state = RUNNING
                        start_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_2:
                        game_state = HOW_TO_PLAY
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        sys.exit()
            elif game_state == HOW_TO_PLAY:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    game_state = MAIN_MENU
            elif game_state in [GAME_OVER, WIN]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    main()

        # Running game logic
        if game_state == RUNNING:
            # Paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle_x -= 10
            if keys[pygame.K_RIGHT]:
                paddle_x += 10

            # Ensure the paddle stays within screen boundaries
            paddle_x = max(0, min(WIDTH - PADDLE_WIDTH, paddle_x))

            # Ball movement
            ball_x += ball_dx
            ball_y += ball_dy

            # Ball collision with walls
            if ball_x <= BALL_SIZE or ball_x >= WIDTH - BALL_SIZE:
                ball_dx *= -1
            if ball_y <= BALL_SIZE:
                ball_dy *= -1

            # Ball collision with paddle
            if (paddle_x < ball_x < paddle_x + PADDLE_WIDTH) and (HEIGHT - PADDLE_HEIGHT < ball_y < HEIGHT - PADDLE_HEIGHT + BALL_SIZE):
                ball_dy *= -1
                ball_y = HEIGHT - PADDLE_HEIGHT - BALL_SIZE

            # Ball collision with bricks
            for brick in bricks[:]:
                if brick.collidepoint(ball_x, ball_y):
                    ball_dy *= -1
                    bricks.remove(brick)
                    score += 10
                    break

            # Check for win condition
            if not bricks:
                level += 1
                bricks = generate_bricks(level)
                ball_dx *= 1.1  # Increase ball speed
                ball_dy *= 1.1
                game_state = WIN

            # Ball below paddle (lose condition)
            if ball_y >= HEIGHT:
                game_state = GAME_OVER

        # Drawing
        SCREEN.fill(WHITE)
        if game_state == MAIN_MENU:
            show_main_menu()
        elif game_state == HOW_TO_PLAY:
            show_how_to_play()
        elif game_state == RUNNING:
            draw_paddle(paddle_x)
            draw_ball(ball_x, ball_y)
            draw_bricks(bricks)
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            display_time(elapsed_time)
        elif game_state == GAME_OVER:
            display_message(f"Game Over! Your score is: {score}", 36, RED, (WIDTH // 4, HEIGHT // 2))
            display_message("Press 'R' to Restart", 24, BLACK, (WIDTH // 3, HEIGHT // 2 + 40))
        elif game_state == WIN:
            display_message(f"Level {level} Complete!", 36, GREEN, (WIDTH // 4, HEIGHT // 2))
            display_message("Press 'R' to Continue", 24, BLACK, (WIDTH // 3, HEIGHT // 2 + 40))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
