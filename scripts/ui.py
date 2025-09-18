import pygame

class Menu:
    def __init__(self, game, title, options):
        self.game = game
        self.title = title
        self.options = options
        self.selected_option = 0
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 32)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected_option
        return None
    
    def render(self, surf):
        # Draw title
        title_text = self.font_large.render(self.title, True, (255, 255, 255))
        surf.blit(title_text, (surf.get_width()//2 - title_text.get_width()//2, 50))
        
        # Draw options
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_option else (255, 255, 255)
            option_text = self.font_small.render(option, True, color)
            surf.blit(option_text, (surf.get_width()//2 - option_text.get_width()//2, 120 + i*40))

class GameOverMenu(Menu):
    def __init__(self, game):
        super().__init__(game, "Game Over", ["Restart", "Quit to Menu"])
    
    def render(self, surf):
        # Draw title
        title_text = self.font_large.render(self.title, True, (255, 0, 0))
        surf.blit(title_text, (surf.get_width()//2 - title_text.get_width()//2, 50))
        
        # Draw score
        score_text = self.font_small.render(f"Final Score: {self.game.score}", True, (255, 255, 255))
        surf.blit(score_text, (surf.get_width()//2 - score_text.get_width()//2, 100))
        
        # Draw options
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_option else (255, 255, 255)
            option_text = self.font_small.render(option, True, color)
            surf.blit(option_text, (surf.get_width()//2 - option_text.get_width()//2, 150 + i*40))