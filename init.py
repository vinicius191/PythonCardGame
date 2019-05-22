import pygame
from game import Game
from config import Config


def main():
    display = pygame.display.set_mode((Config["game"]["width"], Config["game"]["height"]))
    pygame.display.set_caption(Config["game"]["caption"])

    game = Game(display)
    game.loop()


if __name__ == "__main__":
    main()
