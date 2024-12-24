from heapq import heappush, heappop
from dataclasses import dataclass, field
from typing import Tuple, List, Dict

@dataclass(order=True)
class PriorityNode:
    distance: float
    position: Tuple[int, int] = field(compare=False)
    
class PathFinder:
    def __init__(self, game_map):
        self.game_map = game_map
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions"""
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if (0 <= new_x < len(self.game_map[0]) and 
                0 <= new_y < len(self.game_map) and 
                self.game_map[new_y][new_x] != 1):
                neighbors.append((new_x, new_y))
        return neighbors
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Dijkstra's pathfinding algorithm"""
        open_set = []
        heappush(open_set, PriorityNode(0, start))
        
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        distance: Dict[Tuple[int, int], float] = {start: 0}
        
        while open_set:
            current = heappop(open_set).position
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            
            for neighbor in self.get_neighbors(current):
                tentative_distance = distance[current] + 1
                
                if tentative_distance < distance.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    distance[neighbor] = tentative_distance
                    heappush(open_set, PriorityNode(tentative_distance, neighbor))
        
        return []
