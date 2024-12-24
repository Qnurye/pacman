import math
from enum import Enum
import random
from pathfinder import PathFinder

class GhostPersonality(Enum):
    CHASER = 1    # Directly chases Pacman (Red ghost - Blinky)
    AMBUSHER = 2  # Aims ahead of Pacman (Pink ghost - Pinky)
    RANDOM = 3    # Moves randomly (Orange ghost - Clyde)
    FLANKER = 4   # Tries to cut off Pacman (Blue ghost - Inky)

class Ghost:
    def __init__(self, x, y, personality):
        self.x = x
        self.y = y
        self.personality = personality
        self.target_x = 0
        self.target_y = 0
        self.current_path = []
        self.path_update_counter = 0
        self.current_cell = 2  # Track what's underneath the ghost (initially a dot)
        self.stuck_counter = 0  # Add counter to detect when ghost is stuck
        self.last_position = (x, y)  # Track last position
        
    def calculate_move(self, player_x, player_y, game_map):
        # Check if ghost is stuck
        current_pos = (self.x, self.y)
        if current_pos == self.last_position:
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0
            self.last_position = current_pos

        # Force new target if stuck for too long
        if self.stuck_counter > 5:
            self.current_path = []
            self.stuck_counter = 0
            if self.personality != GhostPersonality.RANDOM:
                # Try to move to a random adjacent corridor
                neighbors = []
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_x, new_y = self.x + dx, self.y + dy
                    if (0 <= new_x < len(game_map[0]) and 
                        0 <= new_y < len(game_map) and 
                        game_map[new_y][new_x] != 1):
                        neighbors.append((new_x, new_y))
                if neighbors:
                    self.target_x, self.target_y = random.choice(neighbors)

        # Update target based on personality
        if self.personality == GhostPersonality.CHASER:
            self.target_x, self.target_y = player_x, player_y
        
        elif self.personality == GhostPersonality.AMBUSHER:
            # More aggressive ambusher behavior
            dx = player_x - self.x
            dy = player_y - self.y
            # Target 4 tiles ahead in player's general direction
            self.target_x = min(max(0, player_x + (2 if dx > 0 else -2)), len(game_map[0])-1)
            self.target_y = min(max(0, player_y + (2 if dy > 0 else -2)), len(game_map)-1)
        
        elif self.personality == GhostPersonality.RANDOM:
            if not self.current_path or random.random() < 0.2:  # Increased chance to change direction
                self.target_x = random.randint(0, len(game_map[0])-1)
                self.target_y = random.randint(0, len(game_map)-1)
        
        elif self.personality == GhostPersonality.FLANKER:
            # More dynamic flanking behavior
            dx = player_x - self.x
            dy = player_y - self.y
            # Try to cut off player by moving perpendicular to their position
            if abs(dx) > abs(dy):
                self.target_x = player_x
                self.target_y = player_y + (-5 if dy > 0 else 5)
            else:
                self.target_x = player_x + (-5 if dx > 0 else 5)
                self.target_y = player_y
            # Ensure target is within bounds
            self.target_x = min(max(0, self.target_x), len(game_map[0])-1)
            self.target_y = min(max(0, self.target_y), len(game_map)-1)

        # Force more frequent path recalculation
        self.path_update_counter += 1
        if self.path_update_counter >= 5 or not self.current_path:  # Reduced from 10 to 5
            self.path_update_counter = 0
            pathfinder = PathFinder(game_map)
            start = (self.x, self.y)
            goal = (self.target_x, self.target_y)
            self.current_path = pathfinder.find_path(start, goal)
            
            # If no path found, try moving directly towards target
            if not self.current_path:
                dx = max(min(self.target_x - self.x, 1), -1)
                dy = max(min(self.target_y - self.y, 1), -1)
                return (dx, dy)
        
        # Get next move from path
        if len(self.current_path) > 1:
            next_pos = self.current_path[1]
            self.current_path = self.current_path[1:]
            return (next_pos[0] - self.x, next_pos[1] - self.y)
            
        # If path is exhausted, force recalculation on next update
        self.current_path = []
        return (0, 0)

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        
        if (0 <= new_x < len(game_map[0]) and 
            0 <= new_y < len(game_map) and 
            game_map[new_y][new_x] != 1):
            # Store what's in the new cell (dot or empty)
            next_cell = game_map[new_y][new_x]
            if next_cell != 4:  # Don't store if it's another ghost
                self.current_cell = next_cell
            
            # Restore the previous cell's content
            game_map[self.y][self.x] = self.current_cell
            
            # Update position
            self.x = new_x
            self.y = new_y
            
            # Set new position to ghost
            game_map[self.y][self.x] = 4
