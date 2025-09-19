import pygame
import random
import math

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.bag = []
        self.interaction = False
        self.direction = 1  
        self.animation_frame = 0
        self.animation_speed = 0.1

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.interaction = False
        
        
        if isinstance(self.game.assets[self.type], list) and len(self.game.assets[self.type]) > 1:
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.game.assets[self.type]):
                self.animation_frame = 0
        
        
        if movement[0] > 0:
            self.direction = 1
        elif movement[0] < 0:
            self.direction = -1
        
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
    
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

        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        
        for rect in tilemap.interaction_reacts_around(self.pos):
            if entity_rect.colliderect(rect):
                self.interaction = True

    def render(self, surf):
        if isinstance(self.game.assets[self.type], list):
            image = self.game.assets[self.type][int(self.animation_frame) % len(self.game.assets[self.type])]
        else:
            image = self.game.assets[self.type]
            
        
        if self.direction < 0:
            image = pygame.transform.flip(image, True, False)
        surf.blit(image, self.pos)

    def collect_fruit(self):
        new_fruit = FruitEntity(self.game).assign_value()
        self.bag.append(new_fruit)
        return new_fruit.value

    def get_points(self):
        resume = 0
        for fruit in self.bag:
            resume += fruit.value
        return resume
    
    def get_last_fruit_value(self):
        if self.bag:
            return self.bag[-1].value
        return 0

class Enemy(PhysicsEntity):
    def __init__(self, game, e_type, pos, size, behavior, patrol_range=None):
        super().__init__(game, e_type, pos, size)
        self.behavior = behavior  
        self.patrol_range = patrol_range
        self.patrol_direction = 1
        self.chase_range = 100
        self.speed = 1
    
    def update(self, tilemap, player_pos=None):
        movement = [0, 0]
        
        if self.behavior == "patrol" and self.patrol_range:
            
            if self.pos[0] <= self.patrol_range[0]:
                self.patrol_direction = 1
            elif self.pos[0] >= self.patrol_range[1]:
                self.patrol_direction = -1
            movement[0] = self.patrol_direction * self.speed
        
        elif self.behavior == "chase" and player_pos:
            distance = math.sqrt((player_pos[0] - self.pos[0])**2 + (player_pos[1] - self.pos[1])**2)
            if distance < self.chase_range:
                if player_pos[0] < self.pos[0]:
                    movement[0] = -self.speed
                else:
                    movement[0] = self.speed
        
        super().update(tilemap, movement)

class FruitEntity:
    def __init__(self, game):
        self.game = game
        self.value = 0

    def assign_value(self):
        list_values = [5, 10, 15]
        self.value = random.choice(list_values)
        return self