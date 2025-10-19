import pygame

class Display:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Connect 4")
        self.bg_color = (0, 0, 0)  # Black background
        self.grid_color = (0, 0, 255)  # Blue grid
        self.piece_colors = {
            1: (255, 0, 0),  # Red
            2: (255, 255, 0)  # Yellow
        }

    def draw_grid(self, rows, cols):
        for row in range(rows):
            for col in range(cols):
                pygame.draw.rect(self.screen, self.grid_color, (col * (self.width // cols), row * (self.height // rows), self.width // cols, self.height // rows), 1)

    def draw_piece(self, row, col, player):
        color = self.piece_colors[player]
        pygame.draw.circle(self.screen, color, (col * (self.width // 7) + (self.width // 7) // 2, row * (self.height // 6) + (self.height // 6) // 2), (self.width // 7) // 2 - 5)

    def update_display(self):
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(self.bg_color)