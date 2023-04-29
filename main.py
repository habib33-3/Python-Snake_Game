import random
import time

import pygame
from pygame.locals import  *

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()

        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()

        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= SIZE

        if self.direction == "right":
            self.x[0] += SIZE

        if self.direction == "up":
            self.y[0] -= SIZE

        if self.direction == "down":
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()

        self.play_music_background()

        self.surface = pygame.display.set_mode(size=(1000, 800))
        self.surface.fill((95, 25, 84))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE and y2 <= y1 < y2 + SIZE:
            return True

        return False

    def display_score(self):
        font = pygame.font.SysFont('Arial', 36)
        score = font.render(
            f"Score : {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (800, 10))

    def play_music_background(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")

            self.apple.move()
            self.snake.increase_length()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)

        font = pygame.font.SysFont('Arial', 36)

        line1 = font.render(
            f"Game Over. Your Score is : {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(line1, (200, 200))

        line2 = font.render(
            "To play again press enter,To exit press escape", True, (200, 200, 200))
        self.surface.blit(line2, (200, 300))

        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    elif event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        elif event.key == K_DOWN:
                            self.snake.move_down()

                        elif event.key == K_LEFT:
                            self.snake.move_left()

                        elif event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()
