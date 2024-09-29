# Hack Nerd Font Mono Regular
import pygame
import os
from scripts.utils import  load_images
from scripts.tilemap import Tiles
RENDER_SCALE = 2
class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Level Editor')
        self.screen = pygame.display.set_mode((640,480))
        self.display = pygame.Surface((320,240))
        self.clock = pygame.time.Clock()
        self.movement = [False, False, False, False]
        self.assets = {
            'decor': load_images('tiles/decor'),
            'stone': load_images('tiles/stone'),
            'large_decor': load_images('tiles/large_decor'),
            'grass': load_images('tiles/grass'),
        }
        self.tilemap = Tiles(self, tile_size=16)
        self.scroll = [0,0]
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.clicking = False
        self.rightclicking = False
        self.onscreen = True
#FIX: fix this
#HACK:
#TODO: what is rwerw
#WARN:
#OPTIM:
#NOTE:
#TEST:
#PASSED: what is wring
#FAILED: what is wrong
#INFO: what is happeing
    def run(self):
        running = True
        while running:
            self.scroll[0]+= (self.movement[1] - self.movement[0])*3
            self.scroll[1]+= (self.movement[3] - self.movement[2])*3
            self.display.fill((0,0,0))
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, render_scroll)
            current_tile = self.assets[self.tile_list[self.tile_group]][self.tile_variant]
            current_tile.set_alpha(100)
            self.display.blit(current_tile, (0,0))

            mouse_pos = pygame.mouse.get_pos()
            #Rescaling mouse position
            mouse_pos = (mouse_pos[0] / RENDER_SCALE , mouse_pos[1] / RENDER_SCALE)
            #Calculating the position of the tile, relative to the mouse
            tile_pos = (int(mouse_pos[0] + render_scroll[0])// self.tilemap.tile_size),(int(mouse_pos[1] + render_scroll[1])// self.tilemap.tile_size)
            if self.onscreen:
                #Calculating the positiong of where the tile is placed, relative to the mouse
                #Just taking the tile position from tile_pos and converting it back to pixel co-ordinates
                self.display.blit(current_tile, (tile_pos[0] * self.tilemap.tile_size - render_scroll[0], tile_pos[1] * self.tilemap.tile_size -   render_scroll[1]))
            else:
                self.display.blit(current_tile, mouse_pos)

            if self.clicking and self.onscreen:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type' : self.tile_list[self.tile_group], 'variant': self.tile_variant , 'pos': tile_pos}
            if self.rightclicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button ==1:
                        self.clicking = True
                        if not self.onscreen:
                            self.tilemap.offscreen_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant,
                                                                 'pos' : (mouse_pos[0] + self.scroll[0], mouse_pos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.rightclicking = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_a:
                        self.tile_group = (self.tile_group -1) % len(self.tile_list)
                        self.tile_variant= 0 #some tile_groups have different number of varaints
                    if event.key == pygame.K_s:
                        self.tile_variant = (self.tile_variant -1) % len(self.assets[self.tile_list[self.tile_group]])
                    if event.key == pygame.K_g:
                        self.onscreen = not self.onscreen

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button ==3:
                        self.rightclicking = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)  # limits FPS to 60
        pygame.quit()
Editor().run()

