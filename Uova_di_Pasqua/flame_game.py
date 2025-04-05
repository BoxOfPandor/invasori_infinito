import pygame
import random
import sys

WIDTH = 800
HEIGHT = 600

player_x = WIDTH // 2
player_y = HEIGHT - 40

flames = []

score = 0

FLAME_COLORS = [(255, 0, 0), (255, 255, 0), (255, 255, 255)]

INITIAL_FLAME_SPAWN_RATE = 0.1
FLAME_SPAWN_INCREASE_RATE = 0.01

MAX_FLAMES = 12

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drop dodger")

clock = pygame.time.Clock()


player = pygame.image.load('Uova_di_Pasqua/img/olympic-torch.png').convert_alpha()
player = pygame.transform.scale(player, (14, 40))

# Load flame sprite
flame = pygame.image.load('Uova_di_Pasqua/img/water_drop.png').convert_alpha()
flame = pygame.transform.scale(flame, (14, 20))

background = pygame.image.load('Uova_di_Pasqua/img/jeux-olympiques-paris-2024.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

pygame.mixer.music.load('Uova_di_Pasqua/music/The_P_____Eek.mp3')
pygame.mixer.music.play(-1)

HIGH_SCORE_FILE = "Uova_di_Pasqua/high_score.txt"


def get_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def save_high_score(new_high_score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(new_high_score))


def update_player_position(keys):
    global player_x, player_y
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 10
    elif keys[pygame.K_RIGHT] and player_x < WIDTH - 20:
        player_x += 10
    elif keys[pygame.K_UP] and player_y > 0:
        player_y -= 10
    elif keys[pygame.K_DOWN] and player_y < HEIGHT - 40:
        player_y += 10


def update_flames():
    global flames, score
    speed = score / 100 + 5
    new_flames = []
    for fx, fy in flames:
        if fy < HEIGHT:
            new_flames.append((fx, fy + speed))
        else:
            score += 1
    flames = new_flames

    flame_spawn_rate = INITIAL_FLAME_SPAWN_RATE + FLAME_SPAWN_INCREASE_RATE * score

    if len(flames) < MAX_FLAMES and random.random() < flame_spawn_rate:
        flames.append((random.randint(0, WIDTH - 20), 0))


def check_collision():
    global player_x, player_y
    player_rect = player.get_rect(topleft=(player_x, player_y))
    for fx, fy in flames:
        flame_rect = flame.get_rect(topleft=(fx, fy))
        if player_rect.colliderect(flame_rect):
            return True
    return False


def draw_screen():
    screen.blit(background, (0, 0))
    screen.blit(player, (player_x, player_y))
    for fx, fy in flames:
        screen.blit(flame, (fx, fy))
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {get_high_score()}", True, (255, 255, 255))
    screen.blit(high_score_text, (10, 50))
    pygame.display.flip()


def end_screen(final_score, high_score):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 48)

    game_over_text = font.render("Game Over!", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(game_over_text, game_over_rect)

    final_score_text = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
    final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(final_score_text, final_score_rect)

    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(high_score_text, high_score_rect)

    retry_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), retry_button)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), quit_button)
    easy_button = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 + 180, 150, 50)
    pygame.draw.rect(screen, (0, 0, 255), easy_button)
    medium_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 180, 150, 50)
    pygame.draw.rect(screen, (255, 255, 0), medium_button)
    hard_button = pygame.Rect(WIDTH // 2 + 150, HEIGHT // 2 + 180, 150, 50)
    pygame.draw.rect(screen, (255, 0, 0), hard_button)

    retry_text = font.render("Retry", True, (0, 0, 0))
    retry_text_rect = retry_text.get_rect(center=retry_button.center)
    screen.blit(retry_text, retry_text_rect)

    quit_text = font.render("Quit", True, (0, 0, 0))
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_text_rect)

    easy_text = font.render("Easy", True, (0, 0, 0))
    easy_text_rect = easy_text.get_rect(center=easy_button.center)
    screen.blit(easy_text, easy_text_rect)

    medium_text = font.render("Medium", True, (0, 0, 0))
    medium_text_rect = medium_text.get_rect(center=medium_button.center)
    screen.blit(medium_text, medium_text_rect)

    hard_text = font.render("Hard", True, (0, 0, 0))
    hard_text_rect = hard_text.get_rect(center=hard_button.center)
    screen.blit(hard_text, hard_text_rect)

    pygame.display.flip()

    return retry_button, quit_button, easy_button, medium_button, hard_button


def set_difficulty(difficulty):
    global MAX_FLAMES
    if difficulty == "easy":
        MAX_FLAMES = 12
    elif difficulty == "medium":
        MAX_FLAMES = 20
    elif difficulty == "hard":
        MAX_FLAMES = 40


def game_over():
    final_score = score
    high_score = get_high_score()
    if final_score > high_score:
        save_high_score(final_score)
    end_screen(final_score, high_score)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                retry_button, quit_button, easy_button, medium_button, hard_button = end_screen(final_score, get_high_score())
                if retry_button.collidepoint(mouse_pos):
                    return True
                elif quit_button.collidepoint(mouse_pos):
                    return False
                elif easy_button.collidepoint(mouse_pos):
                    set_difficulty("easy")
                    return True
                elif medium_button.collidepoint(mouse_pos):
                    set_difficulty("medium")
                    return True
                elif hard_button.collidepoint(mouse_pos):
                    set_difficulty("hard")
                    return True


def main():
    global score, player_x, player_y, flames
    # Main game loop
    running = True
    fullscreen = False

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        update_player_position(keys)
        update_flames()
        if check_collision():
            final_score = score
            high_score = get_high_score()
            end_screen(final_score, high_score)
            retry = game_over()
            if retry:
                score = 0
                player_x = WIDTH // 2
                player_y = HEIGHT - 40
                flames = []
            else:
                running = False  # End the game loop

        draw_screen()
        clock.tick(30)  # Limit frame rate to 30 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
