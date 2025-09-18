import pygame
import random

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down' : False, 'right': False, 'left': False}
        self.bag = []
        self.interaction = False

    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])

    def update(self, tilemap,movement=(0,0)):
        self.collisions = {'up': False, 'down' : False, 'right': False, 'left': False}
        self.interaction= False
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_reacts_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right 
                    self.collisions['left'] = True  
                self.pos[0] = entity_rect.x
       
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_reacts_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom  
                    self.collisions['up'] = True 
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5,self.velocity[1] + 0.1)
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        for rect in tilemap.interaction_reacts_around(self.pos):
            if entity_rect.colliderect(rect):
                self.interaction=True
                    
                    
                

    def render(self,surf):
        surf.blit(self.game.assets['player'], self.pos)

    def collect_fruit(self):
        new_fruit = FruitEntity(self).assign_value()
        self.bag.append(new_fruit)

    def get_points(self):
        resume = 0
        for fruit in self.bag:
            resume+= fruit.value
        return resume

class FruitEntity:
    def __init__(self,game):
        self.game = game
        self.value = 0

    def assign_value(self):
        list_values = [5,10,15]
        self.value= random.choice(list_values)
        return self
    

    
    
    
        