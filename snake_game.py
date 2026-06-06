import sys
import os
import random
import math
import pygame

# Ховаємо стартове повідомлення pygame в консолі
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
# Форсуємо використання Direct3D для Windows, щоб уникнути помилок рендерера
os.environ["SDL_RENDER_DRIVER"] = "direct3d"
pygame.init()

# Розміри вікна та сітки
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20

# Кольорова палітра
COLOR_BACKGROUND = (195, 230, 195)
COLOR_PURPLE_BG = (45, 25, 65)
COLOR_DOOM_BG = (25, 5, 5)
COLOR_FLAPPY_BG = (113, 197, 207)
COLOR_SPACE_BG = (10, 10, 25)

COLOR_SNAKE_HEAD = (60, 115, 60)
COLOR_SNAKE_BODY = (80, 140, 80)
COLOR_OBSTACLE = (139, 90, 43)

COLOR_TEXT = (40, 65, 40)
COLOR_TEXT_LIGHT = (230, 215, 245)
COLOR_TEXT_DOOM = (240, 40, 40)
COLOR_TEXT_FLAPPY = (255, 255, 255)
COLOR_TEXT_SPACE = (0, 255, 120)

COLOR_BUTTON_BG = (165, 210, 165)
COLOR_BUTTON_BG_PURPLE = (95, 60, 135)
COLOR_BUTTON_BG_DOOM = (95, 15, 15)
COLOR_BUTTON_BG_FLAPPY = (222, 114, 53)
COLOR_BUTTON_BG_SPACE = (0, 130, 65)

TETRIS_X_OFFSET = 200
TETRIS_Y_OFFSET = 0

# Фігури Тетрісу
TETRIS_SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]]
]

TETRIS_COLORS = [
    (0, 180, 180), (180, 180, 0), (128, 0, 128),
    (0, 150, 0), (180, 0, 0), (0, 0, 180), (180, 100, 0)
]

# Карти DOOM (5 рівнів)
DOOM_MAPS = [
    # Рівень 1: Коридори зі стовпами
    [
        "##############################",
        "#P                           #",
        "#                            #",
        "#    ####            ####    #",
        "#    ####            ####    #",
        "#                            #",
        "#             E              #",
        "#                            #",
        "#             E              #",
        "#                            #",
        "#                            #",
        "#             E              #",
        "#                            #",
        "#    ####            ####    #",
        "#    ####            ####    #",
        "#                           X#",
        "##############################"
    ],
    # Рівень 2: Лабіринт кімнат
    [
        "##############################",
        "#P           #              X#",
        "#            #               #",
        "#    E       #       E       #",
        "#######   ####    ############",
        "#                            #",
        "#    E                       #",
        "###########    #######   #####",
        "#                    #       #",
        "#          E         #   E   #",
        "######   #############   #####",
        "#                            #",
        "#             E              #",
        "##########   #################",
        "#                            #",
        "#    E                       #",
        "##############################"
    ],
    # Рівень 3: Фінальна Арена Пекла
    [
        "##############################",
        "#P            E             X#",
        "#                            #",
        "#   E                    E   #",
        "#        ############        #",
        "#        #    E     #        #",
        "#   E    #          #    E   #",
        "#        #    E     #        #",
        "#        #####  #####        #",
        "#                            #",
        "#        #####  #####        #",
        "#        #    E     #        #",
        "#   E    #          #    E   #",
        "#        #    E     #        #",
        "#        ############        #",
        "#                            #",
        "##############################"
    ],
    # Рівень 4: Заплутані катакомби перед Босом
    [
        "##############################",
        "#P        #          #       #",
        "#         #    E     #   E   #",
        "#   ####  #######    #       #",
        "#   #  #        #    #####   #",
        "#   #E #   E    #            #",
        "#   ####        #    #####   #",
        "#               #    #   #   #",
        "#   #############    # E #   #",
        "#   #                #   #   #",
        "#       E            #####   #",
        "#                            #",
        "#   ##########   #########   #",
        "#            #   #           #",
        "#     E      #   #     E     #",
        "#            #   #          X#",
        "##############################"
    ],
    # Рівень 5: ТРОН БОСА ТА ПОРТАЛ ДОДОМУ
    [
        "##############################",
        "#P                           #",
        "#                            #",
        "#                            #",
        "#                            #",
        "#                            #",
        "#              E             #",
        "#              B             #",
        "#              E             #",
        "#                            #",
        "#                            #",
        "#                            #",
        "#                            #",
        "#                            #",
        "#                            #",
        "#                           X#",
        "##############################"
    ]
]

global screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ретро Ігровий Центр")
clock = pygame.time.Clock()


def draw_text(text, size, x, y, color=COLOR_TEXT):
    font = pygame.font.SysFont("Arial", size, bold=True)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    screen.blit(render, rect)


def draw_button(rect, text, size, bg_color=COLOR_BUTTON_BG, text_color=COLOR_TEXT):
    pygame.draw.rect(screen, bg_color, rect, border_radius=8)
    pygame.draw.rect(screen, text_color, rect, width=2, border_radius=8)
    draw_text(text, size, rect.centerx, rect.centery, text_color)


def draw_arrow_button(rect, direction, theme="SNAKE"):
    if theme == "SNAKE":
        bg, border = COLOR_BUTTON_BG, COLOR_TEXT
    elif theme == "TETRIS":
        bg, border = COLOR_BUTTON_BG_PURPLE, COLOR_TEXT_LIGHT
    elif theme == "DOOM":
        bg, border = COLOR_BUTTON_BG_DOOM, COLOR_TEXT_DOOM
    elif theme == "FLAPPY":
        bg, border = COLOR_BUTTON_BG_FLAPPY, COLOR_TEXT_FLAPPY
    else:
        bg, border = COLOR_BUTTON_BG_SPACE, COLOR_TEXT_SPACE

    pygame.draw.circle(screen, bg, rect.center, rect.width // 2)
    pygame.draw.circle(screen, border, rect.center, rect.width // 2, width=2)

    cx, cy = rect.center
    if direction == "RIGHT":
        points = [(cx - 4, cy - 8), (cx + 6, cy), (cx - 4, cy + 8)]
    else:
        points = [(cx + 4, cy - 8), (cx - 6, cy), (cx + 4, cy + 8)]

    pygame.draw.polygon(screen, border, points)


def draw_flappy_bird(x, y):
    pygame.draw.circle(screen, (247, 219, 79), (int(x), int(y)), 14)
    pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 14, width=2)
    pygame.draw.circle(screen, (255, 255, 255), (int(x + 5), int(y - 4)), 5)
    pygame.draw.circle(screen, (0, 0, 0), (int(x + 5), int(y - 4)), 5, width=1)
    pygame.draw.circle(screen, (0, 0, 0), (int(x + 6), int(y - 4)), 2)
    pygame.draw.polygon(screen, (247, 120, 37), [(x + 12, y - 2), (x + 22, y + 2), (x + 12, y + 6)])
    pygame.draw.polygon(screen, (0, 0, 0), [(x + 12, y - 2), (x + 22, y + 2), (x + 12, y + 6)], width=1)
    pygame.draw.ellipse(screen, (230, 190, 40), pygame.Rect(x - 10, y, 12, 8))
    pygame.draw.ellipse(screen, (0, 0, 0), pygame.Rect(x - 10, y, 12, 8), width=1)


def draw_realistic_apple(screen, pos, is_gold):
    cx = pos[0] + CELL_SIZE // 2
    cy = pos[1] + CELL_SIZE // 2
    color_body = (255, 215, 0) if is_gold else (220, 40, 40)
    color_stem = (100, 65, 30)
    color_leaf = (40, 140, 40)

    pygame.draw.line(screen, color_stem, (cx, cy - 2), (cx + 4, cy - 9), 2)
    pygame.draw.circle(screen, color_leaf, (cx + 5, cy - 8), 3)
    pygame.draw.circle(screen, color_body, (cx, cy + 1), 8)
    pygame.draw.circle(screen, (255, 255, 255), (cx - 3, cy - 2), 2)


def check_collision(grid, piece, offset):
    off_x, off_y = offset
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                tx = x + off_x
                ty = y + off_y
                if tx < 0 or tx >= 10 or ty >= 20:
                    return True
                if ty >= 0 and grid[ty][tx]:
                    return True
    return False


def rotate(piece):
    return [list(row) for row in zip(*piece[::-1])]


def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared = 20 - len(new_grid)
    while len(new_grid) < 20:
        new_grid.insert(0, [0 for _ in range(10)])
    return new_grid, cleared


def main():
    global screen
    state = "MENU_SNAKE"
    back_to_menu = "MENU_SNAKE"
    game_over_reason = "LOSE"
    is_fullscreen = False

    # Кнопки меню
    play_snake_rect = pygame.Rect(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 25, 160, 50)
    play_tetris_rect = pygame.Rect(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 25, 160, 50)
    play_doom_rect = pygame.Rect(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 25, 160, 50)
    play_flappy_rect = pygame.Rect(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 25, 160, 50)
    play_space_rect = pygame.Rect(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 25, 160, 50)

    arrow_left_snake = pygame.Rect(20, WINDOW_HEIGHT // 2 - 25, 50, 50)
    arrow_right_snake = pygame.Rect(WINDOW_WIDTH - 70, WINDOW_HEIGHT // 2 - 25, 50, 50)

    arrow_left_tetris = pygame.Rect(20, WINDOW_HEIGHT // 2 - 25, 50, 50)
    arrow_right_tetris = pygame.Rect(WINDOW_WIDTH - 70, WINDOW_HEIGHT // 2 - 25, 50, 50)

    arrow_left_doom = pygame.Rect(20, WINDOW_HEIGHT // 2 - 25, 50, 50)
    arrow_right_doom = pygame.Rect(WINDOW_WIDTH - 70, WINDOW_HEIGHT // 2 - 25, 50, 50)

    arrow_left_flappy = pygame.Rect(20, WINDOW_HEIGHT // 2 - 25, 50, 50)
    arrow_right_flappy = pygame.Rect(WINDOW_WIDTH - 70, WINDOW_HEIGHT // 2 - 25, 50, 50)

    arrow_left_space = pygame.Rect(20, WINDOW_HEIGHT // 2 - 25, 50, 50)
    arrow_right_space = pygame.Rect(WINDOW_WIDTH - 70, WINDOW_HEIGHT // 2 - 25, 50, 50)

    # Кнопка повноекранного режиму в кутку
    settings_rect = pygame.Rect(WINDOW_WIDTH - 70, 15, 55, 30)

    # Фон: Змійка
    bg_snake = [[140, 200], [120, 200], [100, 200], [80, 200], [60, 200], [40, 200]]
    bg_snake_dir = "RIGHT"
    last_bg_snake_move = 0

    # Фон: Тетріс
    bg_tetris_pieces = []
    for _ in range(6):
        idx = random.randint(0, len(TETRIS_SHAPES) - 1)
        bg_tetris_pieces.append({
            "shape": TETRIS_SHAPES[idx],
            "color": TETRIS_COLORS[idx],
            "x": random.randint(0, WINDOW_WIDTH - 60),
            "y": random.randint(-400, 0),
            "speed": random.uniform(1.5, 3.5)
        })

    # Фон: DOOM (іскри)
    doom_sparks = []
    for _ in range(35):
        doom_sparks.append({
            "x": random.randint(0, WINDOW_WIDTH),
            "y": random.randint(WINDOW_HEIGHT, WINDOW_HEIGHT + 200),
            "speed": random.uniform(2.0, 5.0),
            "radius": random.randint(2, 5)
        })

    # Фон: Космічні зірки (для Space Invaders)
    space_stars = []
    for _ in range(40):
        space_stars.append({
            "x": random.randint(0, WINDOW_WIDTH),
            "y": random.randint(0, WINDOW_HEIGHT),
            "speed": random.uniform(0.5, 2.0)
        })

    # Ігрові змінні для Snake & Tetris
    snake = []
    direction, change_to = "RIGHT", "RIGHT"
    obstacles, apples, score = [], [], 0
    tetris_grid, tetris_score, current_piece = [], 0, None
    snake_speed, tetris_speed = 160, 500
    last_snake_update, last_tetris_fall = 0, 0

    # Ігрові змінні для DOOM
    doom_level = 1
    doom_player_hp = 100
    doom_player_pos = [0, 0]
    doom_walls = []
    doom_enemies = []
    doom_bullets = []
    doom_enemy_bullets = []
    doom_exit_rect = pygame.Rect(0, 0, 1, 1)
    last_minigun_shot = 0

    # Ігрові змінні для Flappy Bird
    flappy_bird_y = 200.0
    flappy_bird_vel = 0.0
    flappy_pipes = []
    flappy_score = 0

    # Ігрові змінні для Space Invaders
    space_player_x = 300
    space_player_lives = 3
    space_invaders = []
    space_bullets = []
    space_enemy_bullets = []
    space_invader_dir = 1
    space_invader_speed = 1.5
    space_wave = 1
    last_space_shot = 0

    def spawn_piece():
        idx = random.randint(0, len(TETRIS_SHAPES) - 1)
        return {"shape": TETRIS_SHAPES[idx], "color": TETRIS_COLORS[idx], "x": 3, "y": 0}

    def init_doom_level(level_num):
        nonlocal doom_walls, doom_enemies, doom_bullets, doom_enemy_bullets, doom_player_pos, doom_exit_rect
        doom_walls = []
        doom_enemies = []
        doom_bullets = []
        doom_enemy_bullets = []

        map_lines = DOOM_MAPS[level_num - 1]
        for r_idx, row in enumerate(map_lines):
            for c_idx, char in enumerate(row):
                bx = c_idx * CELL_SIZE
                by = r_idx * CELL_SIZE
                if char == '#':
                    doom_walls.append(pygame.Rect(bx, by, CELL_SIZE, CELL_SIZE))
                elif char == 'P':
                    doom_player_pos = [bx + CELL_SIZE // 2, by + CELL_SIZE // 2]
                elif char == 'E':
                    doom_enemies.append({
                        "x": bx + CELL_SIZE // 2,
                        "y": by + CELL_SIZE // 2,
                        "hp": 2,
                        "max_hp": 2,
                        "is_boss": False,
                        "radius": 10,
                        "shoot_cooldown": random.randint(30, 90)
                    })
                elif char == 'B':
                    doom_enemies.append({
                        "x": bx + CELL_SIZE // 2,
                        "y": by + CELL_SIZE // 2,
                        "hp": 1000,
                        "max_hp": 1000,
                        "is_boss": True,
                        "radius": 24,
                        "shoot_cooldown": 20
                    })
                elif char == 'X':
                    doom_exit_rect = pygame.Rect(bx, by, CELL_SIZE, CELL_SIZE)

    def init_space_invaders():
        nonlocal space_invaders, space_bullets, space_enemy_bullets, space_invader_dir
        space_invaders = []
        space_bullets = []
        space_enemy_bullets = []
        space_invader_dir = 1

        # Створюємо сітку прибульців (6 колонок на 3 ряди)
        for row in range(3):
            for col in range(7):
                space_invaders.append({
                    "x": 80 + col * 60,
                    "y": 60 + row * 40,
                    "width": 30,
                    "height": 20,
                    "type": row
                })

    while True:
        current_time = pygame.time.get_ticks()
        fs_text = "WND" if is_fullscreen else "FULL"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = event.pos

                # Обробка повноекранного режиму в меню
                if state in ["MENU_SNAKE", "MENU_TETRIS", "MENU_DOOM", "MENU_FLAPPY",
                             "MENU_SPACE"] and settings_rect.collidepoint(m_pos):
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        try:
                            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                                             pygame.FULLSCREEN | pygame.SCALED)
                        except pygame.error:
                            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    continue

                if state == "MENU_SNAKE":
                    if play_snake_rect.collidepoint(m_pos):
                        snake = [[100, 100], [80, 100], [60, 100]]
                        direction, change_to = "RIGHT", "RIGHT"
                        score, apples, obstacles = 0, [], []
                        num_obstacles = random.randint(3, 4)
                        while len(obstacles) < num_obstacles:
                            obs_pos = [random.randrange(0, WINDOW_WIDTH // CELL_SIZE) * CELL_SIZE,
                                       random.randrange(0, WINDOW_HEIGHT // CELL_SIZE) * CELL_SIZE]
                            if obs_pos not in snake and obs_pos not in obstacles:
                                obstacles.append(obs_pos)
                        last_snake_update = current_time
                        back_to_menu = "MENU_SNAKE"
                        state = "PLAY_SNAKE"
                    elif arrow_right_snake.collidepoint(m_pos):
                        state = "MENU_TETRIS"
                    elif arrow_left_snake.collidepoint(m_pos):
                        state = "MENU_SPACE"

                elif state == "MENU_TETRIS":
                    if play_tetris_rect.collidepoint(m_pos):
                        tetris_grid = [[0 for _ in range(10)] for _ in range(20)]
                        tetris_score = 0
                        current_piece = spawn_piece()
                        last_tetris_fall = current_time
                        back_to_menu = "MENU_TETRIS"
                        state = "PLAY_TETRIS"
                    elif arrow_left_tetris.collidepoint(m_pos):
                        state = "MENU_SNAKE"
                    elif arrow_right_tetris.collidepoint(m_pos):
                        state = "MENU_DOOM"

                elif state == "MENU_DOOM":
                    if play_doom_rect.collidepoint(m_pos):
                        doom_level = 1
                        doom_player_hp = 100
                        init_doom_level(doom_level)
                        back_to_menu = "MENU_DOOM"
                        state = "PLAY_DOOM"
                    elif arrow_left_doom.collidepoint(m_pos):
                        state = "MENU_TETRIS"
                    elif arrow_right_doom.collidepoint(m_pos):
                        state = "MENU_FLAPPY"

                elif state == "MENU_FLAPPY":
                    if play_flappy_rect.collidepoint(m_pos):
                        flappy_bird_y = 200.0
                        flappy_bird_vel = 0.0
                        flappy_pipes = []
                        flappy_score = 0
                        back_to_menu = "MENU_FLAPPY"
                        state = "PLAY_FLAPPY"
                    elif arrow_left_flappy.collidepoint(m_pos):
                        state = "MENU_DOOM"
                    elif arrow_right_flappy.collidepoint(m_pos):
                        state = "MENU_SPACE"

                elif state == "MENU_SPACE":
                    if play_space_rect.collidepoint(m_pos):
                        space_player_x = 300
                        space_player_lives = 3
                        score = 0
                        space_wave = 1
                        space_invader_speed = 1.5
                        init_space_invaders()
                        back_to_menu = "MENU_SPACE"
                        state = "PLAY_SPACE"
                    elif arrow_left_space.collidepoint(m_pos):
                        state = "MENU_FLAPPY"
                    elif arrow_right_space.collidepoint(m_pos):
                        state = "MENU_SNAKE"

                elif state == "PLAY_DOOM" and event.button == 1:
                    if doom_level < 5:
                        px, py = doom_player_pos
                        mx, my = event.pos
                        base_angle = math.atan2(my - py, mx - px)
                        for spread in [-0.15, 0, 0.15]:
                            doom_bullets.append({
                                "x": px, "y": py,
                                "vx": math.cos(base_angle + spread) * 7,
                                "vy": math.sin(base_angle + spread) * 7,
                                "damage": 1,
                                "color": (255, 230, 100)
                            })

                elif state == "PLAY_FLAPPY" and event.button == 1:
                    flappy_bird_vel = -7.5

                elif state == "GAME_OVER":
                    state = back_to_menu

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = back_to_menu

                elif state == "MENU_SNAKE":
                    if event.key == pygame.K_RIGHT:
                        state = "MENU_TETRIS"
                    elif event.key == pygame.K_LEFT:
                        state = "MENU_SPACE"
                    elif event.key == pygame.K_RETURN:
                        snake = [[100, 100], [80, 100], [60, 100]]
                        direction, change_to = "RIGHT", "RIGHT"
                        score, apples, obstacles = 0, [], []
                        num_obstacles = random.randint(3, 4)
                        while len(obstacles) < num_obstacles:
                            obs_pos = [random.randrange(0, WINDOW_WIDTH // CELL_SIZE) * CELL_SIZE,
                                       random.randrange(0, WINDOW_HEIGHT // CELL_SIZE) * CELL_SIZE]
                            if obs_pos not in snake and obs_pos not in obstacles:
                                obstacles.append(obs_pos)
                        last_snake_update = current_time
                        back_to_menu = "MENU_SNAKE"
                        state = "PLAY_SNAKE"

                elif state == "MENU_TETRIS":
                    if event.key == pygame.K_LEFT:
                        state = "MENU_SNAKE"
                    elif event.key == pygame.K_RIGHT:
                        state = "MENU_DOOM"
                    elif event.key == pygame.K_RETURN:
                        tetris_grid = [[0 for _ in range(10)] for _ in range(20)]
                        tetris_score = 0
                        current_piece = spawn_piece()
                        last_tetris_fall = current_time
                        back_to_menu = "MENU_TETRIS"
                        state = "PLAY_TETRIS"

                elif state == "MENU_DOOM":
                    if event.key == pygame.K_LEFT:
                        state = "MENU_TETRIS"
                    elif event.key == pygame.K_RIGHT:
                        state = "MENU_FLAPPY"
                    elif event.key == pygame.K_RETURN:
                        doom_level = 1
                        doom_player_hp = 100
                        init_doom_level(doom_level)
                        back_to_menu = "MENU_DOOM"
                        state = "PLAY_DOOM"

                elif state == "MENU_FLAPPY":
                    if event.key == pygame.K_LEFT:
                        state = "MENU_DOOM"
                    elif event.key == pygame.K_RIGHT:
                        state = "MENU_SPACE"
                    elif event.key == pygame.K_RETURN:
                        flappy_bird_y = 200.0
                        flappy_bird_vel = 0.0
                        flappy_pipes = []
                        flappy_score = 0
                        back_to_menu = "MENU_FLAPPY"
                        state = "PLAY_FLAPPY"

                elif state == "MENU_SPACE":
                    if event.key == pygame.K_LEFT:
                        state = "MENU_FLAPPY"
                    elif event.key == pygame.K_RIGHT:
                        state = "MENU_SNAKE"
                    elif event.key == pygame.K_RETURN:
                        space_player_x = 300
                        space_player_lives = 3
                        score = 0
                        space_wave = 1
                        space_invader_speed = 1.5
                        init_space_invaders()
                        back_to_menu = "MENU_SPACE"
                        state = "PLAY_SPACE"

                elif state == "PLAY_SNAKE":
                    if event.key == pygame.K_UP and direction != "DOWN":
                        change_to = "UP"
                    elif event.key == pygame.K_DOWN and direction != "UP":
                        change_to = "DOWN"
                    elif event.key == pygame.K_LEFT and direction != "RIGHT":
                        change_to = "LEFT"
                    elif event.key == pygame.K_RIGHT and direction != "LEFT":
                        change_to = "RIGHT"

                elif state == "PLAY_TETRIS":
                    if event.key == pygame.K_LEFT:
                        current_piece["x"] -= 1
                        if check_collision(tetris_grid, current_piece["shape"],
                                           (current_piece["x"], current_piece["y"])):
                            current_piece["x"] += 1
                    elif event.key == pygame.K_RIGHT:
                        current_piece["x"] += 1
                        if check_collision(tetris_grid, current_piece["shape"],
                                           (current_piece["x"], current_piece["y"])):
                            current_piece["x"] -= 1
                    elif event.key == pygame.K_DOWN:
                        current_piece["y"] += 1
                        if check_collision(tetris_grid, current_piece["shape"],
                                           (current_piece["x"], current_piece["y"])):
                            current_piece["y"] -= 1
                    elif event.key == pygame.K_UP:
                        rotated = rotate(current_piece["shape"])
                        if not check_collision(tetris_grid, rotated, (current_piece["x"], current_piece["y"])):
                            current_piece["shape"] = rotated

                elif state == "PLAY_FLAPPY":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        flappy_bird_vel = -7.5

        # --- КЕРУВАННЯ В REAL-TIME ДЛЯ DOOM ТА SPACE INVADERS ---
        keys = pygame.key.get_pressed()
        if state == "PLAY_DOOM":
            p_speed = 3
            p_radius = 8
            dx, dy = 0, 0
            if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -p_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = p_speed
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -p_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = p_speed

            doom_player_pos[0] += dx
            p_rect = pygame.Rect(doom_player_pos[0] - p_radius, doom_player_pos[1] - p_radius, p_radius * 2,
                                 p_radius * 2)
            for wall in doom_walls:
                if p_rect.colliderect(wall):
                    doom_player_pos[0] -= dx
                    break

            doom_player_pos[1] += dy
            p_rect = pygame.Rect(doom_player_pos[0] - p_radius, doom_player_pos[1] - p_radius, p_radius * 2,
                                 p_radius * 2)
            for wall in doom_walls:
                if p_rect.colliderect(wall):
                    doom_player_pos[1] -= dy
                    break

            if doom_level == 5 and keys[pygame.K_SPACE]:
                if current_time - last_minigun_shot >= 100:
                    last_minigun_shot = current_time
                    px, py = doom_player_pos
                    mx, my = pygame.mouse.get_pos()
                    angle = math.atan2(my - py, mx - px)
                    spread = random.uniform(-0.08, 0.08)
                    doom_bullets.append({
                        "x": px, "y": py,
                        "vx": math.cos(angle + spread) * 11,
                        "vy": math.sin(angle + spread) * 11,
                        "damage": 10,
                        "color": (255, 215, 0)
                    })

            if p_rect.colliderect(doom_exit_rect):
                if doom_level < 5:
                    doom_level += 1
                    init_doom_level(doom_level)
                else:
                    score = 666
                    game_over_reason = "WIN"
                    state = "GAME_OVER"

        elif state == "PLAY_SPACE":
            # Рух гравця
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                space_player_x = max(20, space_player_x - 4)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                space_player_x = min(WINDOW_WIDTH - 20, space_player_x + 4)
            # Стрільба
            if keys[pygame.K_SPACE]:
                if current_time - last_space_shot > 450:
                    last_space_shot = current_time
                    space_bullets.append({"x": space_player_x, "y": 350})

        # --- МАЛЮВАННЯ ЕКРАНІВ МЕНЮ ---
        if state == "MENU_SNAKE":
            screen.fill(COLOR_BACKGROUND)
            if current_time - last_bg_snake_move > 140:
                last_bg_snake_move = current_time
                if random.random() < 0.15:
                    p_dirs = ["UP", "DOWN", "LEFT", "RIGHT"]
                    if bg_snake_dir == "UP":
                        p_dirs.remove("DOWN")
                    elif bg_snake_dir == "DOWN":
                        p_dirs.remove("UP")
                    elif bg_snake_dir == "LEFT":
                        p_dirs.remove("RIGHT")
                    elif bg_snake_dir == "RIGHT":
                        p_dirs.remove("LEFT")
                    bg_snake_dir = random.choice(p_dirs)
                bg_head = list(bg_snake[0])
                if bg_snake_dir == "UP":
                    bg_head[1] -= CELL_SIZE
                elif bg_snake_dir == "DOWN":
                    bg_head[1] += CELL_SIZE
                elif bg_snake_dir == "LEFT":
                    bg_head[0] -= CELL_SIZE
                elif bg_snake_dir == "RIGHT":
                    bg_head[0] += CELL_SIZE
                bg_head[0] %= WINDOW_WIDTH
                bg_head[1] %= WINDOW_HEIGHT
                bg_snake.insert(0, bg_head)
                bg_snake.pop()

            for idx, block in enumerate(bg_snake):
                color = (130, 175, 130) if idx == 0 else (150, 195, 150)
                pygame.draw.rect(screen, color, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))

            draw_text("SNAKE", 50, WINDOW_WIDTH // 2, 100)
            draw_button(play_snake_rect, "ГРАТИ", 24)
            draw_arrow_button(arrow_left_snake, "LEFT", "SNAKE")
            draw_arrow_button(arrow_right_snake, "RIGHT", "SNAKE")
            draw_button(settings_rect, fs_text, 14, COLOR_BUTTON_BG, COLOR_TEXT)
            pygame.display.flip()
            clock.tick(30)

        elif state == "MENU_TETRIS":
            screen.fill(COLOR_PURPLE_BG)
            for piece in bg_tetris_pieces:
                piece["y"] += piece["speed"]
                if piece["y"] > WINDOW_HEIGHT:
                    piece["y"] = random.randint(-150, -40)
                    piece["x"] = random.randint(0, WINDOW_WIDTH - 60)
                    idx = random.randint(0, len(TETRIS_SHAPES) - 1)
                    piece["shape"] = TETRIS_SHAPES[idx]
                    piece["color"] = TETRIS_COLORS[idx]

                for r_idx, row in enumerate(piece["shape"]):
                    for c_idx, cell in enumerate(row):
                        if cell:
                            px = piece["x"] + c_idx * CELL_SIZE
                            py = int(piece["y"]) + r_idx * CELL_SIZE
                            if py < WINDOW_HEIGHT:
                                light_color = tuple(min(255, int(c * 0.5 + 120)) for c in piece["color"])
                                pygame.draw.rect(screen, light_color, pygame.Rect(px, py, CELL_SIZE, CELL_SIZE))

            draw_text("TETRIS", 50, WINDOW_WIDTH // 2, 100, COLOR_TEXT_LIGHT)
            draw_button(play_tetris_rect, "ГРАТИ", 24, COLOR_BUTTON_BG_PURPLE, COLOR_TEXT_LIGHT)
            draw_arrow_button(arrow_left_tetris, "LEFT", "TETRIS")
            draw_arrow_button(arrow_right_tetris, "RIGHT", "TETRIS")
            draw_button(settings_rect, fs_text, 14, COLOR_BUTTON_BG_PURPLE, COLOR_TEXT_LIGHT)
            pygame.display.flip()
            clock.tick(30)

        elif state == "MENU_DOOM":
            screen.fill(COLOR_DOOM_BG)
            for spark in doom_sparks:
                spark["y"] -= spark["speed"]
                if spark["y"] < -10:
                    spark["y"] = random.randint(WINDOW_HEIGHT, WINDOW_HEIGHT + 100)
                    spark["x"] = random.randint(0, WINDOW_WIDTH)
                spark_color = (random.randint(200, 255), random.randint(50, 120), 0)
                pygame.draw.circle(screen, spark_color, (int(spark["x"]), int(spark["y"])), spark["radius"])

            draw_text("DOOM", 55, WINDOW_WIDTH // 2, 100, COLOR_TEXT_DOOM)
            draw_button(play_doom_rect, "ГРАТИ", 24, COLOR_BUTTON_BG_DOOM, COLOR_TEXT_DOOM)
            draw_arrow_button(arrow_left_doom, "LEFT", "DOOM")
            draw_arrow_button(arrow_right_doom, "RIGHT", "DOOM")
            draw_button(settings_rect, fs_text, 14, COLOR_BUTTON_BG_DOOM, COLOR_TEXT_DOOM)
            pygame.display.flip()
            clock.tick(30)

        elif state == "MENU_FLAPPY":
            screen.fill(COLOR_FLAPPY_BG)
            menu_bird_y = 260 + math.sin(current_time * 0.007) * 15
            draw_flappy_bird(WINDOW_WIDTH // 2, menu_bird_y)

            draw_text("FLAPPY BIRD", 50, WINDOW_WIDTH // 2, 100, COLOR_TEXT_FLAPPY)
            draw_button(play_flappy_rect, "ГРАТИ", 24, COLOR_BUTTON_BG_FLAPPY, COLOR_TEXT_FLAPPY)
            draw_arrow_button(arrow_left_flappy, "LEFT", "FLAPPY")
            draw_arrow_button(arrow_right_flappy, "RIGHT", "FLAPPY")
            draw_button(settings_rect, fs_text, 14, COLOR_BUTTON_BG_FLAPPY, COLOR_TEXT_FLAPPY)
            pygame.display.flip()
            clock.tick(30)

        elif state == "MENU_SPACE":
            screen.fill(COLOR_SPACE_BG)
            for star in space_stars:
                star["y"] += star["speed"]
                if star["y"] > WINDOW_HEIGHT: star["y"] = 0
                pygame.draw.circle(screen, (200, 220, 255), (int(star["x"]), int(star["y"])), 1)

            # Намалюємо маленького ворога по центру для стилю
            ex, ey = WINDOW_WIDTH // 2, 260 + math.sin(current_time * 0.005) * 8
            pygame.draw.rect(screen, (0, 255, 120), pygame.Rect(ex - 15, ey - 10, 30, 20), border_radius=4)
            pygame.draw.rect(screen, (0, 40, 10), pygame.Rect(ex - 10, ey - 4, 6, 6))
            pygame.draw.rect(screen, (0, 40, 10), pygame.Rect(ex + 4, ey - 4, 6, 6))

            draw_text("SPACE INVADERS", 46, WINDOW_WIDTH // 2, 100, COLOR_TEXT_SPACE)
            draw_button(play_space_rect, "ГРАТИ", 24, COLOR_BUTTON_BG_SPACE, COLOR_TEXT_SPACE)
            draw_arrow_button(arrow_left_space, "LEFT", "SPACE")
            draw_arrow_button(arrow_right_space, "RIGHT", "SPACE")
            draw_button(settings_rect, fs_text, 14, COLOR_BUTTON_BG_SPACE, COLOR_TEXT_SPACE)
            pygame.display.flip()
            clock.tick(30)

        # --- ЛОГІКА ІГРОВИХ ПРОЦЕСІВ ---
        elif state == "PLAY_SPACE":
            screen.fill(COLOR_SPACE_BG)

            # Малюємо фон
            for star in space_stars:
                star["y"] += star["speed"] * 1.5
                if star["y"] > WINDOW_HEIGHT: star["y"] = 0
                pygame.draw.circle(screen, (255, 255, 255), (int(star["x"]), int(star["y"])), 1)

            # Рух та оновлення куль гравця
            for b in space_bullets[:]:
                b["y"] -= 7
                if b["y"] < 0:
                    space_bullets.remove(b)
                    continue
                pygame.draw.rect(screen, (255, 255, 100), pygame.Rect(b["x"] - 2, b["y"], 4, 10))

            # Логіка руху прибульців
            invader_shift_down = False
            for inv in space_invaders:
                inv["x"] += space_invader_dir * space_invader_speed
                if inv["x"] + inv["width"] >= WINDOW_WIDTH - 15 or inv["x"] <= 15:
                    invader_shift_down = True

            if invader_shift_down:
                space_invader_dir *= -1
                for inv in space_invaders:
                    inv["y"] += 15
                    if inv["y"] >= 330:  # Прибульці дійшли до землі
                        game_over_reason = "LOSE"
                        state = "GAME_OVER"

            # Малювання прибульців та перевірка колізій з кулями гравця
            for inv in space_invaders[:]:
                inv_rect = pygame.Rect(inv["x"], inv["y"], inv["width"], inv["height"])

                # Малюємо прибульця
                color = (0, 255, 100) if inv["type"] == 0 else ((0, 200, 255) if inv["type"] == 1 else (255, 100, 255))
                pygame.draw.rect(screen, color, inv_rect, border_radius=3)
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(inv["x"] + 5, inv["y"] + 5, 4, 4))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(inv["x"] + 19, inv["y"] + 5, 4, 4))

                # Стрільба ворогів
                if random.random() < 0.004:
                    space_enemy_bullets.append({"x": inv["x"] + 15, "y": inv["y"] + 20})

                # Перевірка влучання
                for b in space_bullets[:]:
                    if inv_rect.collidepoint(b["x"], b["y"]):
                        space_bullets.remove(b)
                        space_invaders.remove(inv)
                        score += 15
                        break

            # Оновлення та малювання куль ворогів
            for eb in space_enemy_bullets[:]:
                eb["y"] += 4.5
                if eb["y"] > WINDOW_HEIGHT:
                    space_enemy_bullets.remove(eb)
                    continue
                pygame.draw.rect(screen, (255, 50, 50), pygame.Rect(eb["x"] - 2, eb["y"], 4, 12))

                # Влучання в гравця
                player_rect = pygame.Rect(space_player_x - 15, 360, 30, 20)
                if player_rect.collidepoint(eb["x"], eb["y"]):
                    space_enemy_bullets.remove(eb)
                    space_player_lives -= 1
                    if space_player_lives <= 0:
                        game_over_reason = "LOSE"
                        state = "GAME_OVER"

            # Наступна хвиля, якщо всіх вбили
            if len(space_invaders) == 0:
                space_wave += 1
                space_invader_speed += 0.5
                init_space_invaders()

            # Малюємо гравця (Корабель)
            pygame.draw.rect(screen, (50, 200, 50), pygame.Rect(space_player_x - 15, 365, 30, 15), border_radius=4)
            pygame.draw.rect(screen, (50, 200, 50), pygame.Rect(space_player_x - 4, 357, 8, 8))
            pygame.draw.line(screen, (255, 255, 255), (space_player_x, 353), (space_player_x, 357), 2)

            # Інтерфейс (Рахунок, Життя, Хвиля)
            draw_text(f"SCORE: {score}", 16, 60, 20, COLOR_TEXT_SPACE)
            draw_text(f"WAVE: {space_wave}", 16, WINDOW_WIDTH // 2, 20, (255, 255, 100))
            draw_text(f"LIVES: {'❤' * space_player_lives}", 16, WINDOW_WIDTH - 70, 20, (255, 50, 50))

            pygame.display.flip()
            clock.tick(30)

        elif state == "PLAY_DOOM":
            screen.fill((15, 10, 10))

            for b in doom_bullets[:]:
                b["x"] += b["vx"]
                b["y"] += b["vy"]
                b_rect = pygame.Rect(b["x"] - 2, b["y"] - 2, 4, 4)

                hit = False
                for wall in doom_walls:
                    if b_rect.colliderect(wall):
                        if b in doom_bullets: doom_bullets.remove(b)
                        hit = True
                        break
                if hit: continue

                for e in doom_enemies[:]:
                    e_rad = e["radius"]
                    if pygame.Rect(e["x"] - e_rad, e["y"] - e_rad, e_rad * 2, e_rad * 2).colliderect(b_rect):
                        e["hp"] -= b["damage"]
                        if b in doom_bullets: doom_bullets.remove(b)
                        if e["hp"] <= 0: doom_enemies.remove(e)
                        hit = True
                        break
                if hit: continue

                if b["x"] < 0 or b["x"] > WINDOW_WIDTH or b["y"] < 0 or b["y"] > 360:
                    if b in doom_bullets: doom_bullets.remove(b)

            for e in doom_enemies:
                edx = doom_player_pos[0] - e["x"]
                edy = doom_player_pos[1] - e["y"]
                dist = math.hypot(edx, edy)
                speed_modifier = 0.7 if e["is_boss"] else 1.2

                if dist > 0:
                    e["x"] += (edx / dist) * speed_modifier
                    e_rad = e["radius"]
                    if any(pygame.Rect(e["x"] - e_rad, e["y"] - e_rad, e_rad * 2, e_rad * 2).colliderect(w) for w in
                           doom_walls):
                        e["x"] -= (edx / dist) * speed_modifier

                    e["y"] += (edy / dist) * speed_modifier
                    if any(pygame.Rect(e["x"] - e_rad, e["y"] - e_rad, e_rad * 2, e_rad * 2).colliderect(w) for w in
                           doom_walls):
                        e["y"] -= (edy / dist) * speed_modifier

                e["shoot_cooldown"] -= 1
                if e["shoot_cooldown"] <= 0:
                    if e["is_boss"]:
                        e["shoot_cooldown"] = 25
                        e_angle = math.atan2(doom_player_pos[1] - e["y"], doom_player_pos[0] - e["x"])
                        for spread in [-0.25, 0, 0.25]:
                            doom_enemy_bullets.append({
                                "x": e["x"], "y": e["y"],
                                "vx": math.cos(e_angle + spread) * 4.5, "vy": math.sin(e_angle + spread) * 4.5
                            })
                    else:
                        e["shoot_cooldown"] = random.randint(40, 80)
                        e_angle = math.atan2(doom_player_pos[1] - e["y"], doom_player_pos[0] - e["x"])
                        doom_enemy_bullets.append({
                            "x": e["x"], "y": e["y"],
                            "vx": math.cos(e_angle) * 3.5, "vy": math.sin(e_angle) * 3.5
                        })

            for eb in doom_enemy_bullets[:]:
                eb["x"] += eb["vx"]
                eb["y"] += eb["vy"]
                eb_rect = pygame.Rect(eb["x"] - 3, eb["y"] - 3, 6, 6)

                hit = False
                for wall in doom_walls:
                    if eb_rect.colliderect(wall):
                        doom_enemy_bullets.remove(eb)
                        hit = True
                        break
                if hit: continue

                p_rect = pygame.Rect(doom_player_pos[0] - 8, doom_player_pos[1] - 8, 16, 16)
                if eb_rect.colliderect(p_rect):
                    doom_player_hp -= 12
                    doom_enemy_bullets.remove(eb)
                    if doom_player_hp <= 0:
                        doom_player_hp = 0
                        game_over_reason = "LOSE"
                        state = "GAME_OVER"
                    continue

                if eb["x"] < 0 or eb["x"] > WINDOW_WIDTH or eb["y"] < 0 or eb["y"] > 360:
                    if eb in doom_enemy_bullets: doom_enemy_bullets.remove(eb)

            if doom_level == 5:
                pygame.draw.rect(screen, (random.randint(200, 255), 215, random.randint(0, 100)), doom_exit_rect)
            else:
                pygame.draw.rect(screen, (0, 180, 255), doom_exit_rect)
            pygame.draw.rect(screen, (255, 255, 255), doom_exit_rect, 2)

            for wall in doom_walls:
                pygame.draw.rect(screen, (90, 25, 25), wall)
                pygame.draw.rect(screen, (40, 10, 10), wall, 1)

            for b in doom_bullets: pygame.draw.circle(screen, b["color"], (int(b["x"]), int(b["y"])), 3)
            for eb in doom_enemy_bullets: pygame.draw.circle(screen, (255, 90, 0), (int(eb["x"]), int(eb["y"])), 4)

            for e in doom_enemies:
                e_rad = e["radius"]
                if e["is_boss"]:
                    pygame.draw.circle(screen, (150, 20, 20), (int(e["x"]), int(e["y"])), e_rad)
                    pygame.draw.circle(screen, (40, 40, 50), (int(e["x"]), int(e["y"])), e_rad - 6)
                else:
                    pygame.draw.circle(screen, (200, 30, 30), (int(e["x"]), int(e["y"])), e_rad)
                    pygame.draw.circle(screen, (255, 160, 0), (int(e["x"]), int(e["y"])), 5)

                bar_width = e_rad * 2
                bar_x = int(e["x"] - e_rad)
                bar_y = int(e["y"] - e_rad - 8)
                pygame.draw.rect(screen, (80, 0, 0), pygame.Rect(bar_x, bar_y, bar_width, 4))
                pygame.draw.rect(screen, (50, 220, 50),
                                 pygame.Rect(bar_x, bar_y, int(bar_width * max(0.0, e["hp"] / e["max_hp"])), 4))

            mx, my = pygame.mouse.get_pos()
            p_angle = math.atan2(my - doom_player_pos[1], mx - doom_player_pos[0])
            pygame.draw.circle(screen, (50, 180, 50), (int(doom_player_pos[0]), int(doom_player_pos[1])), 8)
            gun_length = 15 if doom_level == 5 else 12
            gun_color = (255, 215, 0) if doom_level == 5 else (200, 200, 200)
            pygame.draw.line(screen, gun_color, doom_player_pos, (doom_player_pos[0] + math.cos(p_angle) * gun_length,
                                                                  doom_player_pos[1] + math.sin(p_angle) * gun_length),
                             4 if doom_level == 5 else 3)

            pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(0, 360, WINDOW_WIDTH, 40))
            pygame.draw.line(screen, COLOR_TEXT_DOOM, (0, 360), (WINDOW_WIDTH, 360), 2)
            draw_text("HP:", 16, 30, 380, COLOR_TEXT_LIGHT)
            pygame.draw.rect(screen, (100, 10, 10), pygame.Rect(50, 372, 120, 16))
            if doom_player_hp > 0: pygame.draw.rect(screen, (220, 20, 20),
                                                    pygame.Rect(50, 372, int(120 * (doom_player_hp / 100)), 16))
            draw_text(f"{doom_player_hp}%", 14, 110, 380, (255, 255, 255))
            draw_text("ЗОЛОТИЙ МІНІГАН" if doom_level == 5 else "ДРОБОВИК", 14, 250, 380,
                      (255, 215, 0) if doom_level == 5 else COLOR_TEXT_LIGHT)
            draw_text(f"LEVEL: {doom_level}/5", 15, 410, 380, COLOR_TEXT_LIGHT)
            draw_text(f"MONSTERS: {len(doom_enemies)}", 15, 520, 380, COLOR_TEXT_DOOM)
            pygame.display.flip()
            clock.tick(30)

        elif state == "PLAY_FLAPPY":
            screen.fill(COLOR_FLAPPY_BG)
            flappy_bird_vel += 0.5
            flappy_bird_y += flappy_bird_vel

            if len(flappy_pipes) == 0 or flappy_pipes[-1]["x"] < WINDOW_WIDTH - 240:
                flappy_pipes.append({"x": WINDOW_WIDTH, "top": random.randint(40, 240), "passed": False})

            bird_rect = pygame.Rect(100 - 11, int(flappy_bird_y) - 11, 22, 22)

            for p in flappy_pipes[:]:
                p["x"] -= 3.5
                if p["x"] < -60:
                    flappy_pipes.remove(p)
                    continue

                pipe_gap = 125
                top_pipe_rect = pygame.Rect(p["x"], 0, 52, p["top"])
                bot_pipe_rect = pygame.Rect(p["x"], p["top"] + pipe_gap, 52, WINDOW_HEIGHT - (p["top"] + pipe_gap))

                pygame.draw.rect(screen, (115, 191, 46), top_pipe_rect)
                pygame.draw.rect(screen, (0, 0, 0), top_pipe_rect, width=2)
                pygame.draw.rect(screen, (115, 191, 46), bot_pipe_rect)
                pygame.draw.rect(screen, (0, 0, 0), bot_pipe_rect, width=2)

                if not p["passed"] and p["x"] + 26 < 100:
                    flappy_score += 1
                    p["passed"] = True

                if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bot_pipe_rect):
                    score = flappy_score
                    game_over_reason = "LOSE"
                    state = "GAME_OVER"

            if flappy_bird_y > WINDOW_HEIGHT - 12 or flappy_bird_y < 12:
                score = flappy_score
                game_over_reason = "LOSE"
                state = "GAME_OVER"

            draw_flappy_bird(100, flappy_bird_y)
            draw_text(f"Рахунок: {flappy_score}", 22, 70, 25, COLOR_TEXT_FLAPPY)
            pygame.display.flip()
            clock.tick(30)

        elif state == "GAME_OVER":
            screen.fill(COLOR_BACKGROUND)
            if score == 666 and game_over_reason == "WIN":
                screen.fill((20, 20, 35))
                draw_text("ПОРТАЛ ВІДКРИТО!", 40, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40, (50, 200, 255))
                draw_text("Ви успішно повернулися у реальний світ!", 20, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 15,
                          (255, 255, 255))
            else:
                screen.fill((230, 100, 100) if game_over_reason == "LOSE" else COLOR_BACKGROUND)
                draw_text("ГРА ЗАКІНЧЕНА", 40, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30,
                          (255, 255, 255) if game_over_reason == "LOSE" else COLOR_TEXT)
                if score >= 0 and score != 666:
                    draw_text(f"Ваш результат: {score}", 24, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20,
                              (255, 255, 255) if game_over_reason == "LOSE" else COLOR_TEXT)

            draw_text("Натисніть ESC або мишку для виходу в меню", 16, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40,
                      COLOR_TEXT if score != 666 else (150, 150, 150))
            pygame.display.flip()
            clock.tick(30)

        elif state == "PLAY_SNAKE":
            screen.fill(COLOR_BACKGROUND)
            if current_time - last_snake_update > snake_speed:
                direction = change_to
                head = list(snake[0])
                if direction == "UP":
                    head[1] -= CELL_SIZE
                elif direction == "DOWN":
                    head[1] += CELL_SIZE
                elif direction == "LEFT":
                    head[0] -= CELL_SIZE
                elif direction == "RIGHT":
                    head[0] += CELL_SIZE

                snake.insert(0, head)
                ate_apple = False
                for apple in apples:
                    if head[0] == apple["pos"][0] and head[1] == apple["pos"][1]:
                        score += 5 if apple["type"] == "gold" else 1
                        apples.remove(apple)
                        ate_apple = True
                        break

                if not ate_apple: snake.pop()

                while len(apples) < (2 if score >= 10 else 1):
                    new_pos = [random.randrange(0, WINDOW_WIDTH // CELL_SIZE) * CELL_SIZE,
                               random.randrange(0, WINDOW_HEIGHT // CELL_SIZE) * CELL_SIZE]
                    if new_pos not in snake and new_pos not in [a["pos"] for a in apples] and new_pos not in obstacles:
                        apples.append({"pos": new_pos, "type": "gold" if random.random() < 0.3 else "red"})

                if head[0] < 0 or head[0] >= WINDOW_WIDTH or head[1] < 0 or head[
                    1] >= WINDOW_HEIGHT or head in obstacles:
                    game_over_reason = "LOSE"
                    state = "GAME_OVER"

                for block in snake[1:]:
                    if head[0] == block[0] and head[1] == block[1]:
                        game_over_reason = "LOSE"
                        state = "GAME_OVER"
                last_snake_update = current_time

            for index, block in enumerate(snake):
                pygame.draw.rect(screen, COLOR_SNAKE_HEAD if index == 0 else COLOR_SNAKE_BODY,
                                 pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))
            for apple in apples: draw_realistic_apple(screen, apple["pos"], apple["type"] == "gold")
            for obs in obstacles: pygame.draw.rect(screen, COLOR_OBSTACLE,
                                                   pygame.Rect(obs[0], obs[1], CELL_SIZE, CELL_SIZE))
            draw_text(f"Рахунок: {score}", 20, 60, 20)
            pygame.display.flip()
            clock.tick(30)

        elif state == "PLAY_TETRIS":
            screen.fill(COLOR_PURPLE_BG)
            if current_time - last_tetris_fall > tetris_speed:
                current_piece["y"] += 1
                if check_collision(tetris_grid, current_piece["shape"], (current_piece["x"], current_piece["y"])):
                    current_piece["y"] -= 1
                    for y, row in enumerate(current_piece["shape"]):
                        for x, cell in enumerate(row):
                            if cell and current_piece["y"] + y >= 0:
                                tetris_grid[current_piece["y"] + y][current_piece["x"] + x] = current_piece["color"]
                    tetris_grid, cleared = clear_lines(tetris_grid)
                    tetris_score += cleared * 10
                    current_piece = spawn_piece()
                    if check_collision(tetris_grid, current_piece["shape"], (current_piece["x"], current_piece["y"])):
                        score = tetris_score
                        game_over_reason = "LOSE"
                        state = "GAME_OVER"
                last_tetris_fall = current_time

            pygame.draw.rect(screen, COLOR_TEXT_LIGHT, pygame.Rect(TETRIS_X_OFFSET, TETRIS_Y_OFFSET, 200, 400), 2)
            for y in range(20):
                for x in range(10):
                    if tetris_grid[y][x]:
                        pygame.draw.rect(screen, tetris_grid[y][x],
                                         pygame.Rect(TETRIS_X_OFFSET + x * CELL_SIZE, TETRIS_Y_OFFSET + y * CELL_SIZE,
                                                     CELL_SIZE, CELL_SIZE))
                        pygame.draw.rect(screen, COLOR_PURPLE_BG,
                                         pygame.Rect(TETRIS_X_OFFSET + x * CELL_SIZE, TETRIS_Y_OFFSET + y * CELL_SIZE,
                                                     CELL_SIZE, CELL_SIZE), 1)

            for y, row in enumerate(current_piece["shape"]):
                for x, cell in enumerate(row):
                    if cell:
                        px = TETRIS_X_OFFSET + (current_piece["x"] + x) * CELL_SIZE
                        py = TETRIS_Y_OFFSET + (current_piece["y"] + y) * CELL_SIZE
                        if py >= 0:
                            pygame.draw.rect(screen, current_piece["color"], pygame.Rect(px, py, CELL_SIZE, CELL_SIZE))
                            pygame.draw.rect(screen, COLOR_PURPLE_BG, pygame.Rect(px, py, CELL_SIZE, CELL_SIZE), 1)

            draw_text(f"Рахунок: {tetris_score}", 20, 70, 20, COLOR_TEXT_LIGHT)
            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    main()