import pygame

from src.game.constants import WINDOW_SIZE, MENU_BG, MENU_TEXT, MENU_SELECT, LOSS_BG, LOSS_TEXT, LOSS_OPTION


class Screen:
    def __init__(self, screen, title, options, bg_color, text_color, select_color):
        self.screen = screen
        self.title = title
        self.options = options
        self.bg_color = bg_color
        self.text_color = text_color
        self.select_color = select_color
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 50)
        self.selected = 0

    def draw(self):
        self.screen.fill(self.bg_color)
        title = self.font_big.render(self.title, True, self.text_color)
        title_rect = title.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 4))
        self.screen.blit(title, title_rect)
        for i, opt in enumerate(self.options):
            color = self.select_color if i == self.selected else self.text_color
            text = self.font_small.render(opt, True, color)
            rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + i * 60))
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


class Menu(Screen):
    def __init__(self, screen):
        super().__init__(screen, 'PACMAN', ['Start Game', 'Quit'], MENU_BG, MENU_TEXT, MENU_SELECT)


class LossScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen, 'GAME OVER', ['Try Again', 'Main Menu'], LOSS_BG, LOSS_TEXT, LOSS_OPTION)
