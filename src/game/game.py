import sys

import pygame

from src.entities.ghost import Ghost, GhostPersonality
from src.entities.player import Player
from src.game.constants import CELL_SIZE, FPS, PLAYER_SPEED, GHOST_SPEED, BLACK, BLUE, WHITE, YELLOW, GHOST_COLORS
from src.game.map import Map
from src.game.utils import find_player_start, find_ghost_starts
from src.ui.screens import LossScreen


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

    def draw_map(self, game_map, ghosts):
        ghost_positions = {(ghost.x, ghost.y): ghost.personality for ghost in ghosts}

        for y in range(len(game_map)):
            for x in range(len(game_map[y])):
                cell = game_map[y][x]
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                if cell == 1:  # Wall
                    pygame.draw.rect(self.screen, BLUE, rect)
                elif cell == 2:  # Dot
                    pygame.draw.rect(self.screen, BLACK, rect)
                    pygame.draw.circle(self.screen, WHITE,
                                       (x * CELL_SIZE + CELL_SIZE // 2,
                                        y * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 6)
                elif cell == 3:  # Player
                    pygame.draw.rect(self.screen, BLACK, rect)
                    pygame.draw.circle(self.screen, YELLOW,
                                       (x * CELL_SIZE + CELL_SIZE // 2,
                                        y * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 2)
                elif cell == 4:  # Ghost
                    pygame.draw.rect(self.screen, BLACK, rect)
                    ghost_color = GHOST_COLORS[ghost_positions[(x, y)]]
                    pygame.draw.circle(self.screen, ghost_color,
                                       (x * CELL_SIZE + CELL_SIZE // 2,
                                        y * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 2)
                else:  # Empty space
                    pygame.draw.rect(self.screen, BLACK, rect)

    def run(self):
        generator = Map()
        game_map = generator.predefined

        player_pos = find_player_start(game_map)
        if player_pos:
            player = Player(player_pos[0], player_pos[1])
        else:
            print("No player start position found!")
            return

        ghost_positions = find_ghost_starts(game_map)
        ghosts = []
        personalities = list(GhostPersonality)
        for i, pos in enumerate(ghost_positions):
            personality = personalities[i % len(personalities)]
            ghosts.append(Ghost(pos[0], pos[1], personality))

        running = True
        player_move_counter = 0
        ghost_move_counter = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        player.set_next_direction(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        player.set_next_direction(1, 0)
                    elif event.key == pygame.K_UP:
                        player.set_next_direction(0, -1)
                    elif event.key == pygame.K_DOWN:
                        player.set_next_direction(0, 1)
                    elif event.key == pygame.K_SPACE:  # Stop movement
                        player.set_next_direction(0, 0)

            player_move_counter += 1
            if player_move_counter >= PLAYER_SPEED:
                player_move_counter = 0
                player.update(game_map)

            ghost_move_counter += 1
            if ghost_move_counter >= GHOST_SPEED:
                ghost_move_counter = 0
                for ghost in ghosts:
                    dx, dy = ghost.calculate_move(player.x, player.y, game_map)
                    ghost.move(dx, dy, game_map)

                    if ghost.x == player.x and ghost.y == player.y:
                        loss_screen = LossScreen(self.screen)
                        while True:
                            loss_screen.draw()
                            pygame.display.flip()

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                                choice = loss_screen.handle_input(event)
                                if choice == 'Try Again':
                                    return 'retry'
                                elif choice == 'Main Menu':
                                    return 'menu'

                            self.clock.tick(FPS)

            self.screen.fill(BLACK)
            self.draw_map(game_map, ghosts)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
