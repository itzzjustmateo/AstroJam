import pygame, time, random

pygame.init()
pygame.font.init()

# =========================
# Logical resolution
# =========================
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Astrojam 2026")

# This is where we actually draw the game
GAME_SURFACE = pygame.Surface((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# =========================
# Assets & Fonts
# =========================
BG = pygame.transform.scale(
    pygame.image.load("./assets/background.jpeg").convert(),
    (WIDTH, HEIGHT)
)

FONT = pygame.font.SysFont("arial", 26)
BIG_FONT = pygame.font.SysFont("arial", 64, bold=True)

# =========================
# Colors
# =========================
WHITE = (240, 240, 240)
YELLOW = (255, 220, 120)
RED = (220, 60, 60)
UI_BG = (20, 20, 30, 160)

# =========================
# Player
# =========================
PLAYER_WIDTH, PLAYER_HEIGHT = 24, 48
PLAYER_VEL = 5

# =========================
# Stars
# =========================
STAR_WIDTH = 6
STAR_HEIGHT = 18
STAR_VEL = 3

# =========================
# UI helpers
# =========================
def draw_glow_rect(surface, rect, color):
    glow = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
    pygame.draw.rect(
        glow,
        (*color, 90),
        glow.get_rect(),
        border_radius=6
    )
    surface.blit(glow, (rect.x - 5, rect.y - 5))
    pygame.draw.rect(surface, color, rect, border_radius=4)

def draw_ui(surface, elapsed_time):
    panel = pygame.Surface((WIDTH, 50), pygame.SRCALPHA)
    panel.fill(UI_BG)
    surface.blit(panel, (0, 0))

    time_text = FONT.render(f"TIME  {round(elapsed_time)}s", True, WHITE)
    surface.blit(
        time_text,
        (WIDTH // 2 - time_text.get_width() // 2, 12)
    )

def draw_game(surface, player, elapsed_time, stars):
    surface.blit(BG, (0, 0))

    for star in stars:
        pygame.draw.rect(surface, YELLOW, star, border_radius=3)

    draw_glow_rect(surface, player, RED)
    draw_ui(surface, elapsed_time)

def draw_game_over(surface, elapsed_time):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    title = BIG_FONT.render("YOU LOST", True, RED)
    score = FONT.render(
        f"Survived {round(elapsed_time)} seconds",
        True,
        WHITE
    )

    surface.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60)
    )
    surface.blit(
        score,
        (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2 + 10)
    )

# =========================
# Scaling helper
# =========================
def scale_and_blit():
    window_width, window_height = SCREEN.get_size()
    scale = min(window_width / WIDTH, window_height / HEIGHT)

    scaled_surface = pygame.transform.smoothscale(
        GAME_SURFACE,
        (int(WIDTH * scale), int(HEIGHT * scale))
    )

    x = (window_width - scaled_surface.get_width()) // 2
    y = (window_height - scaled_surface.get_height()) // 2

    SCREEN.fill((0, 0, 0))
    SCREEN.blit(scaled_surface, (x, y))
    pygame.display.update()

# =========================
# Main
# =========================
def main():
    global SCREEN

    fullscreen = False

    player = pygame.Rect(
        WIDTH // 2,
        HEIGHT - PLAYER_HEIGHT - 10,
        PLAYER_WIDTH,
        PLAYER_HEIGHT
    )

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_timer = 0
    stars = []

    hit = False
    run = True

    while run:
        dt = clock.tick(60)
        elapsed_time = time.time() - start_time
        star_timer += dt

        if star_timer > star_add_increment:
            for _ in range(3):
                x = random.randint(0, WIDTH - STAR_WIDTH)
                stars.append(pygame.Rect(x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT))
            star_add_increment = max(250, star_add_increment - 50)
            star_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        SCREEN = pygame.display.set_mode(
                            (0, 0), pygame.FULLSCREEN
                        )
                    else:
                        SCREEN = pygame.display.set_mode(
                            (WIDTH, HEIGHT), pygame.RESIZABLE
                        )

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + player.width < WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                hit = True
                break

        GAME_SURFACE.fill((0, 0, 0))

        if hit:
            draw_game_over(GAME_SURFACE, elapsed_time)
            scale_and_blit()
            pygame.time.delay(2500)
            break

        draw_game(GAME_SURFACE, player, elapsed_time, stars)
        scale_and_blit()

    pygame.quit()

if __name__ == "__main__":
    main()
