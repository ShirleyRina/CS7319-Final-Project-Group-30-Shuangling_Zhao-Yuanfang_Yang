import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 定义窗口尺寸和颜色
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MORANDI1 = (244, 229, 20)
MORANDI2 = (194, 135, 121)
MORANDI3 = (180, 156, 169)
MORANDI4 = (176, 117, 99)
SNAKEHEAD = (92, 121, 135)
SNAKEBODY = (217, 227, 229)
PAUSECOLOR = (167, 121, 121)

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE GAME PRO")

# 创建按钮
button_font = pygame.font.Font(None, 25)
button_text = "GAME START"
start_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2, 120, 50)
button_color = (238, 204, 159)

# 食物相关变量
food_x, food_y = 0, 0
food_radius = 5

# 毒药相关变量
poison_x, poison_y = 0, 0
poison_radius = 5

# 计分
score = 0
score_font = pygame.font.Font(None, 24)

# 暂停状态
paused = False

# 游戏状态
is_game_started = False

# 蛇速度相关变量
snake_speed = 5
speed_increase = 5

# 蛇的初始位置
snake_x, snake_y = WIDTH // 2, HEIGHT // 2
snake_direction = 0
snake_length = 1
snake_body = [(snake_x, snake_y)]

# 运行状态
running = True

# 初始化食物位置
def initialize_food():
    global food_x, food_y
    food_x, food_y = random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10

# 初始化毒药的位置
def initialize_poison():
    global poison_x, poison_y
    poison_x, poison_y = random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10

# 处理键盘按下事件
def handle_keydown_event(event):
    global snake_direction, paused
    if event.key == pygame.K_UP and snake_direction != 2:
        snake_direction = 1
    elif event.key == pygame.K_DOWN and snake_direction != 1:
        snake_direction = 2
    elif event.key == pygame.K_LEFT and snake_direction != 4:
        snake_direction = 3
    elif event.key == pygame.K_RIGHT and snake_direction != 3:
        snake_direction = 4
    elif event.key == pygame.K_SPACE:
        paused = not paused

# 处理鼠标点击事件
def handle_mouse_click_event(event):
    global is_game_started
    if not is_game_started and start_button.collidepoint(event.pos):
        is_game_started = True

# 更新贪吃蛇位置
def update_snake_position(direction):
    global snake_x, snake_y
    if direction == 1:
        snake_y -= 10
    elif direction == 2:
        snake_y += 10
    elif direction == 3:
        snake_x -= 10
    elif direction == 4:
        snake_x += 10

# 检查是否与边界发生碰撞
def check_collision_with_border(x, y):
    global running
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        running = False
        game_over()

# 检查是否与毒药发生碰撞
def check_collision_with_poison(x, y):
    global score
    if ((poison_x - x) ** 2 + (poison_y - y) ** 2 <= poison_radius ** 2):
        score -= 1
        initialize_poison()

# 检查是否与食物发生碰撞
def check_collision_with_food(x, y, length):
    global snake_length, snake_speed, score
    if ((food_x - x) ** 2 + (food_y - y) ** 2 <= food_radius ** 2):
        snake_length += 1
        score += 1
        initialize_food()

        if snake_length % 5 == 0:
            snake_speed += speed_increase

# 绘制贪吃蛇
def draw_snake(snake_body):
    for i, segment in enumerate(snake_body):
        if i == len(snake_body) - 1:
            pygame.draw.rect(screen, SNAKEHEAD, (segment[0], segment[1], 10, 10))
        else:
            pygame.draw.rect(screen, SNAKEBODY, (segment[0], segment[1], 10, 10))

# 绘制食物
def draw_food():
    pygame.draw.circle(screen, MORANDI4, (food_x, food_y), food_radius)

# 绘制毒药
def draw_poison():
    poison_vertices = [(poison_x, poison_y - poison_radius),
                       (poison_x - poison_radius, poison_y + poison_radius),
                       (poison_x + poison_radius, poison_y + poison_radius)]
    pygame.draw.polygon(screen, RED, poison_vertices)

# 显示分数和速度
def display_score_and_speed():
    score_text = score_font.render(f"POINT: {score}", True, MORANDI3)
    screen.blit(score_text, (10, 10))

    speed_text = score_font.render(f"SPEED: {snake_speed}", True, MORANDI3)
    screen.blit(speed_text, (WIDTH - 150, 10))

# 游戏结束函数
def game_over():
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, RED)
    game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, game_over_text_rect)
    pygame.display.update()
    pygame.time.delay(1000)
    pygame.quit()
    sys.exit()

# 游戏主题
def game_theme():
    global score, paused, snake_speed, snake_direction, snake_x, snake_y, snake_length, snake_body, running

    # 初始化游戏主题
    screen.fill(WHITE)

    # 贪吃蛇,毒药以及毒药刷新时间相关变量
    poison_refresh_timer = pygame.time.get_ticks()

    # 初始化食物和毒药的位置
    initialize_food()
    initialize_poison()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                handle_keydown_event(event)

        if paused:
            pause_font = pygame.font.Font(None, 35)
            pause_text = pause_font.render("Tap to Continue", True, PAUSECOLOR)
            pause_text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(pause_text, pause_text_rect)
            pygame.display.update()

        else:
            update_snake_position(snake_direction)

            check_collision_with_border(snake_x, snake_y)
            check_collision_with_poison(snake_x, snake_y)
            check_collision_with_food(snake_x, snake_y, snake_length)

            current_time = pygame.time.get_ticks()

            if current_time - poison_refresh_timer >= 5000:
                initialize_poison()
                poison_refresh_timer = current_time

            snake_body.append((snake_x, snake_y))
            if len(snake_body) > snake_length:
                del snake_body[0]

            screen.fill(WHITE)

            draw_snake(snake_body)
            draw_food()
            draw_poison()

            display_score_and_speed()

            pygame.display.update()
            pygame.time.Clock().tick(snake_speed)

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif is_game_started and event.type == pygame.KEYDOWN:
            handle_keydown_event(event)
        elif not is_game_started and event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click_event(event)

    screen.fill(WHITE)

    if is_game_started:
        game_theme()
        pygame.display.update()
    else:
        pygame.draw.rect(screen, button_color, start_button)
        start_text = button_font.render(button_text, True, WHITE)
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)

        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("SNAKE GAME PRO", True, MORANDI2)
        title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title_text, title_text_rect)

    pygame.display.update()
