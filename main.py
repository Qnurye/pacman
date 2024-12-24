import sys

import pygame

from src.game.constants import WINDOW_SIZE, FPS
from src.game.game import Game
from src.ui.screens import Menu  # Updated import

pygame.init()


def main():
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()

    menu = Menu(screen)
    running = True

    while running:
        menu.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            choice = menu.handle_input(event)
            if choice == 'Start Game':
                game_loop = Game(screen, clock)
                result = game_loop.run()
                if result == 'retry':
                    continue
            elif choice == 'Quit':
                running = False

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
