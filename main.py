import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
FONT = pygame.font.SysFont('Arial', 30)
BIG_FONT = pygame.font.SysFont('Arial', 50)

# Global variables
state = {
    'level': 1,
    'score': 0,
    'paused': False,
    'difficulty': (3, -3),
    'high_score': 0
}

def create_bricks(level):
    bricks = []
    rows = min(5 + level, 10)
    for i in range(rows):
        for j in range(8):
            brick = pygame.Rect(j * 100 + 20, i * 30 + 20, 80, 20)
            bricks.append(brick)
    return bricks

def draw_bricks(bricks):
    for brick in bricks:
        pygame.draw.rect(SCREEN, GREEN, brick)

def move_paddle(paddle, direction):
    if direction == 'left' and paddle.left > 0:
        paddle.move_ip(-20, 0)
    if direction == 'right' and paddle.right < WIDTH:
        paddle.move_ip(20, 0)

def toggle_pause():
    state['paused'] = not state['paused']

def update_ball(ball, paddle, bricks):
    ball.move_ip(state['ball_dx'], state['ball_dy'])

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        state['ball_dx'] = -state['ball_dx']
    if ball.top <= 0:
        state['ball_dy'] = -state['ball_dy']
    if ball.bottom >= HEIGHT:
        return "game_over"

    # Ball collision with paddle
    if ball.colliderect(paddle):
        state['ball_dy'] = -state['ball_dy']
        # Adjust ball direction based on where it hits the paddle
        if ball.centerx < paddle.centerx:
            state['ball_dx'] = -abs(state['ball_dx'])
        else:
            state['ball_dx'] = abs(state['ball_dx'])

    # Ball collision with bricks
    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            state['score'] += 10
            # Determine which side of the brick was hit
            if abs(ball.bottom - brick.top) < 10:
                state['ball_dy'] = -state['ball_dy']
            elif abs(ball.top - brick.bottom) < 10:
                state['ball_dy'] = -state['ball_dy']
            elif abs(ball.right - brick.left) < 10:
                state['ball_dx'] = -state['ball_dx']
            elif abs(ball.left - brick.right) < 10:
                state['ball_dx'] = -state['ball_dx']
            break

    # Check if all bricks are cleared to move to the next level
    if not bricks:
        state['level'] += 1
        if state['level'] > 10:
            return "win"
        else:
            state['bricks'] = create_bricks(state['level'])
            return "next_level"

    return "running"

def draw_text(text, font, color, x, y):
    screen_text = font.render(text, True, color)
    SCREEN.blit(screen_text, [x, y])

def show_start_menu():
    while True:
        SCREEN.fill(BLACK)
        draw_text("Brick Breaker", BIG_FONT, WHITE, WIDTH // 2 - 150, HEIGHT // 2 - 100)
        draw_text("Easy", FONT, WHITE, WIDTH // 2 - 30, HEIGHT // 2 - 20)
        draw_text("Medium", FONT, WHITE, WIDTH // 2 - 45, HEIGHT // 2 + 20)
        draw_text("Hard", FONT, WHITE, WIDTH // 2 - 30, HEIGHT // 2 + 60)
        draw_text("Press 1 for Easy, 2 for Medium, 3 for Hard", FONT, WHITE, WIDTH // 2 - 230, HEIGHT // 2 + 120)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    state['difficulty'] = (3, -3)
                    return
                elif event.key == pygame.K_2:
                    state['difficulty'] = (5, -5)
                    return
                elif event.key == pygame.K_3:
                    state['difficulty'] = (7, -7)
                    return

def game_loop():
    paddle = pygame.Rect(350, 550, 100, 10)
    ball = pygame.Rect(390, 540, 20, 20)
    state['ball_dx'], state['ball_dy'] = state['difficulty']
    state['bricks'] = create_bricks(state['level'])

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    toggle_pause()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move_paddle(paddle, 'left')
        if keys[pygame.K_RIGHT]:
            move_paddle(paddle, 'right')

        if not state['paused']:
            game_status = update_ball(ball, paddle, state['bricks'])
            if game_status == "game_over":
                if state['score'] > state['high_score']:
                    state['high_score'] = state['score']
                return "Game Over"
            elif game_status == "win":
                return "You Win!"
            elif game_status == "next_level":
                ball = pygame.Rect(390, 540, 20, 20)
                state['ball_dx'], state['ball_dy'] = state['difficulty']

        SCREEN.fill(BLACK)
        pygame.draw.rect(SCREEN, BLUE, paddle)
        pygame.draw.ellipse(SCREEN, RED, ball)
        draw_bricks(state['bricks'])
        draw_text(f"Score: {state['score']}", FONT, WHITE, 10, 10)
        draw_text(f"Level: {state['level']}", FONT, WHITE, WIDTH - 150, 10)
        draw_text(f"High Score: {state['high_score']}", FONT, WHITE, WIDTH // 2 - 100, 10)
        if state['paused']:
            draw_text("Paused", BIG_FONT, WHITE, WIDTH // 2 - 80, HEIGHT // 2 - 30)

        pygame.display.flip()
        clock.tick(60)

def main():
    while True:
        show_start_menu()
        result = game_loop()
        SCREEN.fill(BLACK)
        draw_text(result, BIG_FONT, WHITE, WIDTH // 2 - 100, HEIGHT // 2 - 30)
        draw_text(f"Final Score: {state['score']}", FONT, WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 40)
        draw_text("Press R to restart, M for main menu", FONT, WHITE, WIDTH // 2 - 200, HEIGHT // 2 + 80)
        pygame.display.flip()
        pygame.time.wait(2000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        state['level'] = 1
                        state['score'] = 0
                        state['paused'] = False
                        return
                    elif event.key == pygame.K_m:
                        state['level'] = 1
                        state['score'] = 0
                        state['paused'] = False
                        break

main()
