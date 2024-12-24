import pygame

from src.game.constants import CELL_SIZE, BLUE, BLACK, WHITE, YELLOW, GHOST_COLORS


def draw_map(screen, game_map, ghosts):
    ghost_positions = {(ghost.x, ghost.y): ghost.personality for ghost in ghosts}

    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            cell = game_map[y][x]
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if cell == 1:  # Wall
                pygame.draw.rect(screen, BLUE, rect)
            elif cell == 2:  # Dot
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.circle(screen, WHITE,
                                   (x * CELL_SIZE + CELL_SIZE // 2,
                                    y * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 6)
            elif cell == 3:  # Player
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.circle(screen, YELLOW,
                                   (x * CELL_SIZE + CELL_SIZE // 2,
                                    y * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2)
            elif cell == 4:  # Ghost
                pygame.draw.rect(screen, BLACK, rect)
                ghost_color = GHOST_COLORS[ghost_positions[(x, y)]]
                pygame.draw.circle(screen, ghost_color,
                                   (x * CELL_SIZE + CELL_SIZE // 2,
                                    y * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2)
            else:  # Empty space
                pygame.draw.rect(screen, BLACK, rect)


def find_player_start(game_map):
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            if game_map[y][x] == 3:
                return x, y
    return None


def find_ghost_starts(game_map):
    ghost_positions = []
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            if game_map[y][x] == 4:
                ghost_positions.append((x, y))
    return ghost_positions
