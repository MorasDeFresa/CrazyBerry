import pygame
NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'store', 'machine', 'fruit'}
INTERACTION_TILES = {'tree'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.last_tree = set()

        # Create a more interesting level layout
        # Ground
        for i in range(20):
            self.tilemap[f'{i};14'] = {'type': 'store', 'variant': 1, 'pos': (i, 14)}
        
        # Platforms
        for i in range(5):
            self.tilemap[f'{2+i};9'] = {'type': 'machine', 'variant': 1, 'pos': (2+i, 10)}
        
        for i in range(4):
            self.tilemap[f'{10+i};8'] = {'type': 'machine', 'variant': 1, 'pos': (10+i, 8)}
        
        # Fruits
        for i in range(3):
            self.tilemap[f'{5+i};4'] = {'type': 'fruit', 'variant': 1, 'pos': (5+i, 4)}
        
        for i in range(3):
            self.tilemap[f'{13+i};2'] = {'type': 'fruit', 'variant': 1, 'pos': (13+i, 3)}
        
        # Trees (interactive)
        for i in range(2):
            self.tilemap[f'{1+(i*4)};7'] = {
                'type': 'tree', 
                'variant': 1, 
                'pos': (1+(i*4), 7), 
                'collected': False
            }
        for i in range(1):
            self.tilemap[f'{13+(i*4)};0'] = {
                'type': 'tree', 
                'variant': 1, 
                'pos': (13+(i*4), 0), 
                'collected': False
            }
    
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = f'{tile_loc[0] + offset[0]};{tile_loc[1] + offset[1]}'
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_reacts_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(
                    tile['pos'][0] * self.tile_size, 
                    tile['pos'][1] * self.tile_size,
                    self.tile_size, 
                    self.tile_size
                ))
        return rects 
    
    def interaction_reacts_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in INTERACTION_TILES:
                self.last_tree = f'{tile["pos"][0]};{tile["pos"][1]}'
                rects.append(pygame.Rect(
                    tile['pos'][0] * self.tile_size, 
                    tile['pos'][1] * self.tile_size,
                    48, 
                    48
                ))
        return rects 

    def render(self, surf):
        # Draw background tiles first
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['type'] in ['store', 'machine']:
                surf.blit(
                    self.game.assets[tile['type']][tile['variant']],
                    (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size)
                )
        
        # Draw interactive elements on top
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['type'] in ['fruit', 'tree']:
                if not (tile['type'] == 'tree' and tile['collected']):
                    surf.blit(
                        self.game.assets[tile['type']][tile['variant']],
                        (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size)
                    )
        
        # Draw off-grid tiles
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])