import pygame
import sys
from map_generator import PacmanMapGenerator
from ghost import Ghost, GhostPersonality

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 20
WINDOW_SIZE = (32 * CELL_SIZE, 32 * CELL_SIZE)
FPS = 30  # Increase frame rate for smoother animation
PLAYER_SPEED = 5  # Player moves every 5 frames
GHOST_SPEED = 7   # Ghosts move every 7 frames

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
# Ghost colors
GHOST_COLORS = {
    GhostPersonality.CHASER: (255, 0, 0),     # Red for chaser
    GhostPersonality.AMBUSHER: (255, 182, 255),  # Pink for ambusher
    GhostPersonality.RANDOM: (255, 182, 85),   # Orange for random
    GhostPersonality.FLANKER: (0, 255, 255)    # Cyan for flanker
}

# Add new colors for menu
MENU_BG = (0, 0, 0)
MENU_TEXT = (255, 255, 255)
MENU_SELECT = (255, 255, 0)

# Add new colors for loss screen
LOSS_BG = (0, 0, 0)
LOSS_TEXT = (255, 0, 0)
LOSS_OPTION = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pacman")
clock = pygame.time.Clock()

def draw_map(game_map, ghosts):
    """Draw the map on the screen"""
    # Create ghost position to personality mapping
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
                                (x * CELL_SIZE + CELL_SIZE//2, 
                                 y * CELL_SIZE + CELL_SIZE//2), 
                                 CELL_SIZE//6)
            elif cell == 3:  # Player
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.circle(screen, YELLOW, 
                                (x * CELL_SIZE + CELL_SIZE//2, 
                                 y * CELL_SIZE + CELL_SIZE//2), 
                                 CELL_SIZE//2)
            elif cell == 4:  # Ghost
                pygame.draw.rect(screen, BLACK, rect)
                ghost_color = GHOST_COLORS[ghost_positions[(x, y)]]
                pygame.draw.circle(screen, ghost_color, 
                                (x * CELL_SIZE + CELL_SIZE//2, 
                                 y * CELL_SIZE + CELL_SIZE//2), 
                                 CELL_SIZE//2)
            else:  # Empty space
                pygame.draw.rect(screen, BLACK, rect)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)  # (dx, dy) - default no movement
        self.next_direction = (0, 0)  # Store next direction change
        
    def can_move(self, dx, dy, game_map):
        """Check if movement in direction is possible"""
        new_x = self.x + dx
        new_y = self.y + dy
        return (0 <= new_x < len(game_map[0]) and 
                0 <= new_y < len(game_map) and 
                game_map[new_y][new_x] != 1)

    def update(self, game_map):
        """Update player position based on current direction"""
        # Try to apply queued direction change
        if self.next_direction != (0, 0) and self.can_move(*self.next_direction, game_map):
            self.direction = self.next_direction
            self.next_direction = (0, 0)
        
        # Move in current direction if possible
        if self.direction != (0, 0) and self.can_move(*self.direction, game_map):
            self.move(*self.direction, game_map)
            return True
        return False

    def set_next_direction(self, dx, dy):
        """Queue next direction change"""
        self.next_direction = (dx, dy)

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check if the new position is within bounds and not a wall
        if (0 <= new_x < len(game_map[0]) and 
            0 <= new_y < len(game_map) and 
            game_map[new_y][new_x] != 1):
            # Clear current position
            game_map[self.y][self.x] = 0
            # Update position
            self.x = new_x
            self.y = new_y
            # Set new position
            game_map[self.y][self.x] = 3

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

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 50)
        self.options = ['Start Game', 'Quit']
        self.selected = 0
        
    def draw(self):
        self.screen.fill(MENU_BG)
        
        # Draw title
        title = self.font_big.render('PACMAN', True, MENU_TEXT)
        title_rect = title.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//4))
        self.screen.blit(title, title_rect)
        
        # Draw menu options
        for i, opt in enumerate(self.options):
            color = MENU_SELECT if i == self.selected else MENU_TEXT
            text = self.font_small.render(opt, True, color)
            rect = text.get_rect(center=(WINDOW_SIZE[0]//2, 
                                       WINDOW_SIZE[1]//2 + i * 60))
            self.screen.blit(text, rect)
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None

class LossScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 50)
        self.options = ['Try Again', 'Main Menu']
        self.selected = 0
        
    def draw(self):
        self.screen.fill(LOSS_BG)
        
        # Draw game over text
        title = self.font_big.render('GAME OVER', True, LOSS_TEXT)
        title_rect = title.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//3))
        self.screen.blit(title, title_rect)
        
        # Draw options
        for i, opt in enumerate(self.options):
            color = MENU_SELECT if i == self.selected else LOSS_OPTION
            text = self.font_small.render(opt, True, color)
            rect = text.get_rect(center=(WINDOW_SIZE[0]//2, 
                                       WINDOW_SIZE[1]//2 + i * 60))
            self.screen.blit(text, rect)
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None

def game_loop(screen, clock):
    # Generate the map
    generator = PacmanMapGenerator()
    game_map = generator.predefined_map
    
    # Initialize player
    player_pos = find_player_start(game_map)
    if player_pos:
        player = Player(player_pos[0], player_pos[1])
    else:
        print("No player start position found!")
        return

    # Initialize ghosts
    ghost_positions = find_ghost_starts(game_map)
    ghosts = []
    personalities = list(GhostPersonality)
    for i, pos in enumerate(ghost_positions):
        personality = personalities[i % len(personalities)]
        ghosts.append(Ghost(pos[0], pos[1], personality))
    
    # Main game loop
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

        # Update player position every PLAYER_SPEED frames
        player_move_counter += 1
        if player_move_counter >= PLAYER_SPEED:
            player_move_counter = 0
            player.update(game_map)

        # Move ghosts every GHOST_SPEED frames
        ghost_move_counter += 1
        if ghost_move_counter >= GHOST_SPEED:
            ghost_move_counter = 0
            for ghost in ghosts:
                dx, dy = ghost.calculate_move(player.x, player.y, game_map)
                ghost.move(dx, dy, game_map)

                # Check for collision with player
                if ghost.x == player.x and ghost.y == player.y:
                    # Show loss screen instead of immediately ending
                    loss_screen = LossScreen(screen)
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
                    
                        clock.tick(FPS)

        # Clear screen
        screen.fill(BLACK)
        
        # Draw map
        draw_map(game_map, ghosts)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

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
                # Handle game loop return value
                result = game_loop(screen, clock)
                if result == 'retry':
                    continue  # Start new game
                # Return to menu for 'menu' or any other result
            elif choice == 'Quit':
                running = False
        
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
