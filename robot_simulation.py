
import pygame
import random
import sys

# Ustawienia
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
ROBOT_SIZE = 50
TARGET_SIZE = 20
SAVE_FILE = "robot_progress.txt"

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Robot:
    def __init__(self):
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 2
        self.speed = 5

    def move_towards_target(self, target_x, target_y):
        if self.x < target_x:
            self.x += self.speed
        elif self.x > target_x:
            self.x -= self.speed
        if self.y < target_y:
            self.y += self.speed
        elif self.y > target_y:
            self.y -= self.speed

    def draw(self, screen):
        # Noga robota
        pygame.draw.rect(screen, GREEN, (self.x, self.y, ROBOT_SIZE, ROBOT_SIZE))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Robot Simulator")
        self.clock = pygame.time.Clock()
        self.robot = Robot()
        self.target_x = SCREEN_WIDTH - 100
        self.target_y = SCREEN_HEIGHT // 2
        self.last_update_time = pygame.time.get_ticks()

    def save_progress(self):
        with open(SAVE_FILE, "w") as f:
            f.write(f"{self.robot.x},{self.robot.y}")

    def load_progress(self):
        try:
            with open(SAVE_FILE, "r") as f:
                data = f.read().split(',')
                self.robot.x = int(data[0])
                self.robot.y = int(data[1])
        except FileNotFoundError:
            print("Save file not found. Starting from default position.")

    def run(self):
        self.load_progress()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # Zapisz progres
                        self.save_progress()
                    if event.key == pygame.K_l:  # Wczytaj progres
                        self.load_progress()

            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time > 30000:  # Odświeżanie co 30 sekund
                self.last_update_time = current_time
                self.robot.x = SCREEN_WIDTH // 4  # Resetuj pozycję
                self.robot.y = SCREEN_HEIGHT // 2

            # Ruch robota
            self.robot.move_towards_target(self.target_x, self.target_y)

            # Rysowanie
            self.screen.fill(BLACK)
            self.robot.draw(self.screen)
            pygame.draw.rect(self.screen, RED, (self.target_x, self.target_y, TARGET_SIZE, TARGET_SIZE))  # Kostka

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
