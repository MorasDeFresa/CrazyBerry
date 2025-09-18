import pygame
import sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

class Game:
        def __init__(self):
            pygame.init()
            pygame.display.set_caption('Crazy Berry')
            self.screen = pygame.display.set_mode((640,480))
            self.display = pygame.Surface((320,240))
            self.clock = pygame.time.Clock()

            self.movement = [False, False]
            self.assets = {
                 'fruit': load_images('/fruit'),
                 'machine': load_images('/machine'),
                 'store': load_images('/store'),
                 'tree': load_images('/tree'),
                 'player': load_image('/tard/base/bite/1_bite.png')
            }

            self.player = PhysicsEntity(self,'player',(0,80),(14,17))
            self.tilemap = Tilemap(self,tile_size=16)
        def run(self):
            while True:
                self.display.fill((14,219,248))
                self.tilemap.render(self.display)
                self.player.update(self.tilemap,(self.movement[1] - self.movement[0],0))
                self.player.render(self.display)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_LEFT:
                              self.movement[0] = True
                         if event.key == pygame.K_RIGHT:
                              self.movement[1] = True
                         if event.key == pygame.K_UP:
                              self.player.velocity[1] = -5
                    if event.type == pygame.KEYUP:
                         if event.key == pygame.K_LEFT:
                              self.movement[0] = False
                         if event.key == pygame.K_RIGHT:
                              self.movement[1] = False
                self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()))
                pygame.display.update()
                self.clock.tick(60)

Game().run()