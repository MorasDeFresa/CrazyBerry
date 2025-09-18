import pygame
import sys
from scripts.entities import PhysicsEntity, Enemy
from scripts.utils import load_image, load_images, load_sound
from scripts.tilemap import Tilemap
from scripts.ui import Menu, GameOverMenu

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Crazy Berry')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        
        # Game states
        self.game_state = "menu"  # menu, playing, game_over
        self.score = 0
        self.lives = 3
        
        # Load assets
        self.assets = {
            'fruit': load_images('fruit'),
            'machine': load_images('machine'),
            'store': load_images('store'),
            'tree': load_images('tree'),
            'player': load_images('tard/base/bite'),  # Cambiado a load_images para animaciones
            'enemy': load_images('enemy'),
            'background': load_image('background.png'),
        }
        
        # Cargar sonidos si existen
        self.sounds = {}
        try:
            self.sounds['collect'] = load_sound('collect.wav')
            self.sounds['hurt'] = load_sound('hurt.wav')
            self.sounds['jump'] = load_sound('jump.wav')
        except:
            print("Note: Sound files not found. Game will run without sound.")
        
        # Initialize game objects
        self.reset_game()
        
        # Initialize menus
        self.main_menu = Menu(self, "Crazy Berry", ["Start Game", "Quit"])
        self.game_over_menu = GameOverMenu(self)
    
    def reset_game(self):
        self.movement = [False, False]
        self.player = PhysicsEntity(self, 'player', (50, 80), (14, 17))
        self.enemies = [
            Enemy(self, 'enemy', (100, 80), (14, 17), "patrol", (50, 150)),
            Enemy(self, 'enemy', (200, 80), (14, 17), "chase")
        ]
        self.tilemap = Tilemap(self, tile_size=16)
        self.score = 0
        self.lives = 3
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.game_state == "menu":
                action = self.main_menu.handle_event(event)
                if action == 0:  # Start Game
                    self.game_state = "playing"
                elif action == 1:  # Quit
                    pygame.quit()
                    sys.exit()
            
            elif self.game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                         self.player.velocity[1] = -5
                         if 'jump' in self.sounds:
                              self.sounds['jump'].play()
                    if event.key == pygame.K_DOWN:   
                        if self.player.interaction:
                            if self.tilemap.tilemap[self.tilemap.last_tree]['collected'] == False:
                                self.tilemap.tilemap[self.tilemap.last_tree]['collected'] = True
                                fruit_value = self.player.collect_fruit()
                                self.score += fruit_value
                                if 'collect' in self.sounds:
                                    self.sounds['collect'].play()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            
            elif self.game_state == "game_over":
                action = self.game_over_menu.handle_event(event)
                if action == 0:  # Restart
                    self.reset_game()
                    self.game_state = "playing"
                elif action == 1:  # Quit to Menu
                    self.game_state = "menu"
    
    def update(self):
        if self.game_state == "playing":
            # Update player
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            
            # Update enemies and check for collisions
            for enemy in self.enemies:
                enemy.update(self.tilemap, self.player.pos)
                if self.player.rect().colliderect(enemy.rect()):
                    self.lives -= 1
                    if 'hurt' in self.sounds:
                        self.sounds['hurt'].play()
                    # Reset player position
                    self.player.pos = [50, 80]
                    if self.lives <= 0:
                        self.game_state = "game_over"
    
    def render(self):
        # Draw background
        self.display.fill((14, 219, 248))  # Fondo azul claro si no hay imagen
        
        if self.game_state == "menu":
            self.main_menu.render(self.display)
        
        elif self.game_state == "playing":
            # Draw tilemap
            self.tilemap.render(self.display)
            
            # Draw player
            self.player.render(self.display)
            
            # Draw enemies
            for enemy in self.enemies:
                enemy.render(self.display)
            
            # Draw HUD
            self.draw_hud()
        
        elif self.game_state == "game_over":
            self.game_over_menu.render(self.display)
        
        # Scale to screen size
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()))
        pygame.display.update()
    
    def draw_hud(self):
        # Draw score
        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.display.blit(score_text, (10, 10))
        
        # Draw lives
        lives_text = font.render(f'Lives: {self.lives}', True, (0, 0, 0))
        self.display.blit(lives_text, (10, 30))
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()