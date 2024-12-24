class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.next_direction = (0, 0)

    def can_move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        return (0 <= new_x < len(game_map[0]) and
                0 <= new_y < len(game_map) and
                game_map[new_y][new_x] != 1)

    def update(self, game_map):
        if self.next_direction != (0, 0) and self.can_move(*self.next_direction, game_map):
            self.direction = self.next_direction
            self.next_direction = (0, 0)

        if self.direction != (0, 0) and self.can_move(*self.direction, game_map):
            self.move(*self.direction, game_map)
            return True
        return False

    def set_next_direction(self, dx, dy):
        self.next_direction = (dx, dy)

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy

        if (0 <= new_x < len(game_map[0]) and
                0 <= new_y < len(game_map) and
                game_map[new_y][new_x] != 1):
            game_map[self.y][self.x] = 0
            self.x = new_x
            self.y = new_y
            game_map[self.y][self.x] = 3
