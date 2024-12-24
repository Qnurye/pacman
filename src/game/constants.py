from src.entities.ghost import GhostPersonality

CELL_SIZE = 20
WINDOW_SIZE = (32 * CELL_SIZE, 32 * CELL_SIZE)
FPS = 30
PLAYER_SPEED = 5
GHOST_SPEED = 7
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GHOST_COLORS = {
    GhostPersonality.CHASER: (255, 0, 0),
    GhostPersonality.AMBUSHER: (255, 182, 255),
    GhostPersonality.RANDOM: (255, 182, 85),
    GhostPersonality.FLANKER: (0, 255, 255)
}
MENU_BG = (0, 0, 0)
MENU_TEXT = (255, 255, 255)
MENU_SELECT = (255, 255, 0)
LOSS_BG = (0, 0, 0)
LOSS_TEXT = (255, 0, 0)
LOSS_OPTION = (255, 255, 255)
