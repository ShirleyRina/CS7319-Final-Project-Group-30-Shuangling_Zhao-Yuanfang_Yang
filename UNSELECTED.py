import pygame
import sys
import random

from pygame.examples.moveit import WIDTH, HEIGHT

WIDTH, HEIGHT = 600, 600


class Snake:
    def __init__(self, x, y):
        self.snake_speed = 5
        self.speed_increase = 5
        self.snake_head = (x, y)
        self.direction = 0
        self.snake_body = [self.snake_head]

    def move(self):
        x, y = self.snake_head
        if self.direction == 1:
            y -= 10
        elif self.direction == 2:
            y += 10
        elif self.direction == 3:
            x -= 10
        elif self.direction == 4:
            x += 10

        self.snake_head = (x, y)

        if len(self.snake_body) > 1:
            self.snake_body = [self.snake_head] + self.snake_body[:-1]
        else:
            self.snake_body = [self.snake_head]

    def check_collision(self, game):
        x, y = self.snake_head
        if x < 0 or x >= game.WIDTH or y < 0 or y >= game.HEIGHT:
            game.game_over()

        for segment in self.snake_body[1:]:
            if self.snake_head == segment:
                game.game_over()

    def check_eat(self, food, poison, game):
        if self.snake_head == food.position:
            self.snake_body.append(food.position)
            self.speed_up()
            game.score += 1
            food.initialize()

        if self.snake_head == poison.position:
            self.snake_body.pop()
            game.score -= 1
            poison.initialize()

    def draw(self, screen):
        for i, segment in enumerate(self.snake_body):
            if i == len(self.snake_body) - 1:
                pygame.draw.rect(screen, (92, 121, 135), (segment[0], segment[1], 10, 10))
            else:
                pygame.draw.rect(screen, (217, 227, 229), (segment[0], segment[1], 10, 10))

    def speed_up(self):
        if len(self.snake_body) % 5 == 0:
            self.snake_speed += self.speed_increase

    def reset(self, x, y):
        self.snake_head = (x, y)
        self.direction = 0
        self.snake_body = [self.snake_head]

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.radius = 5

    def initialize(self):
        self.position = (random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10)

    def draw(self, screen):
        pygame.draw.circle(screen, (176, 117, 99), self.position, self.radius)

class Poison:
    def __init__(self):
        self.position = (0, 0)
        self.radius = 5

    def initialize(self):
        self.position = (random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10)

    def draw(self, screen):
        vertices = [(self.position[0], self.position[1] - self.radius),
                    (self.position[0] - self.radius, self.position[1] + self.radius),
                    (self.position[0] + self.radius, self.position[1] + self.radius)]
        pygame.draw.polygon(screen, (255, 0, 0), vertices)

class SnakeGame:
    def __init__(self, width, height):
        pygame.init()

        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("SNAKE GAME PRO")

        self.clock = pygame.time.Clock()

        self.snake = Snake(self.WIDTH // 2, self.HEIGHT // 2)
        self.food = Food()
        self.poison = Poison()

        self.paused = False
        self.is_game_started = False
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != 2:
                    self.snake.direction = 1
                if event.key == pygame.K_DOWN and self.snake.direction != 1:
                    self.snake.direction = 2
                if event.key == pygame.K_LEFT and self.snake.direction != 4:
                    self.snake.direction = 3
                if event.key == pygame.K_RIGHT and self.snake.direction != 3:
                    self.snake.direction = 4
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

    def initialize_game(self):
        self.snake.reset(self.WIDTH // 2, self.HEIGHT // 2)
        self.food.initialize()
        self.poison.initialize()
        self.score = 0

    def game_over(self):
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_text_rect = game_over_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(game_over_text, game_over_text_rect)
        pygame.display.update()
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.handle_events()

            self.screen.fill((255, 255, 255))

            if self.is_game_started:
                if not self.paused:
                    self.snake.move()
                    self.snake.check_collision(self)
                    self.snake.check_eat(self.food, self.poison, self)

                self.snake.draw(self.screen)
                self.food.draw(self.screen)
                self.poison.draw(self.screen)

                self.score_display()
                pygame.display.update()
                self.clock.tick(self.snake.snake_speed)
            else:
                self.start_screen()


    def score_display(self):
        score_font = pygame.font.Font(None, 24)
        score_text = score_font.render(f"POINT: {self.score}", True, (180, 156, 169))
        self.screen.blit(score_text, (10, 10))

        speed_text = score_font.render(f"SPEED: {self.snake.snake_speed}", True, (180, 156, 169))
        self.screen.blit(speed_text, (self.WIDTH - 150, 10))

    def start_screen(self):
        button_font = pygame.font.Font(None, 25)
        button_text = "GAME START"
        start_button = pygame.Rect(self.WIDTH // 2 - 60, self.HEIGHT // 2, 120, 50)

        pygame.draw.rect(self.screen, (238, 204, 159), start_button)
        start_text = button_font.render(button_text, True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=start_button.center)
        self.screen.blit(start_text, start_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not self.is_game_started and event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    self.is_game_started = True
                    self.initialize_game()

# 游戏主循环
if __name__ == "__main__":
    snake_game = SnakeGame(WIDTH, HEIGHT)
    snake_game.run()
