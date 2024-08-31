# class for making tiles 
import pygame
surrounding_tiles = [(0,0),(0,1),(0,-1),(1,0),(1,1),(1,-1),(-1,-1),(-1,1),(-1,0)]
collision_tiles = {"grass","stone"}

class Tiles:
    def __init__(self, game, tile_size = 16):
        self.tile_size = tile_size
        self.tilemap = {}
        self.offscreen_tiles = []
        self.game = game
        for i in range(10):
            self.tilemap[str(3+i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3+i, 10)}
            self.tilemap['10;'+ str(5+i) ] = {'type': 'stone', 'variant': 1, 'pos': (10, 5+i)}

    def tiles_around(self, pos):
        #Checks which tiles are around the player, based on the player position
        tiles = []
        current_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for surrounding in surrounding_tiles:
            check_location = str(current_pos[0] + surrounding[0]) + ';' + str(current_pos[1] + surrounding[1])
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles

    def physics_rects(self, pos):
        #Adds collision rects to the tiles that the player is surrounded by
        rect_tiles = []
        for tile in self.tiles_around(pos):
            if tile['type'] in collision_tiles:
                rect_tiles.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rect_tiles

    def render(self, surf, camera_offset = (0,0)):
        for tile in self.offscreen_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0] - camera_offset[0], tile['pos'][1] - camera_offset[1]))
        #Initially we were just creating all tiles, but now we only create tiles that are on the screen
        # Checking from the left-most point to right-most point on the current screen
        for x in range(camera_offset[0] // self.tile_size  , (camera_offset[0] + surf.get_width()) // self.tile_size +1):
            #Checking from top to bottom of the current screen
            for y in range(camera_offset[1] // self.tile_size  , (camera_offset[1] + surf.get_height()) // self.tile_size +1):
                location = str(x) + ';' + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0] * self.tile_size - camera_offset[0], tile['pos'][1] * self.tile_size - camera_offset[1]))
        # for location in self.tilemap:
        #     tile = self.tilemap[location]
        #     surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0] * self.tile_size - camera_offset[0], tile['pos'][1] * self.tile_size - camera_offset[1]))

