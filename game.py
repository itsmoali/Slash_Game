import pygame
import os
from scripts.Physics import Physics , Player
from scripts.utils import load_image, load_images
from scripts.tilemap import Tiles
from scripts.Clouds import Clouds
from scripts.Animations import Animation
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))
        self.display = pygame.Surface((320,240))
        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        self.assets = {
                'player' : load_image('entities/player.png'),
            'decor': load_images('tiles/decor'),
            'stone': load_images('tiles/stone'),
            'large_decor': load_images('tiles/large_decor'),
            'grass': load_images('tiles/grass'),
            'background' : load_image('background.png'),
            'clouds' : load_images('clouds'),
            'player/idle' : Animation(load_images('entities/player/idle'), animation_dur = 6),
            'player/run' : Animation(load_images('entities/player/run'), animation_dur = 6),
            'player/jump' : Animation(load_images('entities/player/jump'), animation_dur = 6),
            'player/slide' : Animation(load_images('entities/player/slide'), animation_dur = 6),
            'player/wall_slide' : Animation(load_images('entities/player/wall_slide'), animation_dur = 6),
        }
        self.clouds = Clouds(self.assets['clouds'],count=16)
        self.tilemap = Tiles(self, tile_size=16)
        self.player = Player(self, (50,50), (8,15))
        # self.player = Physics(self, 'player' , (50,50) , (8,15))
        self.scroll = [0,0]

    def run(self):
        running = True
        while running:
            #The camera would move according to the positon of the player, in a smoothing manner
            self.scroll[0] += (self.player.create_rect().centerx - self.display.get_width() / 2 - self.scroll[0]) 
            self.scroll[1] += (self.player.create_rect().centery - self.display.get_height()/2 - self.scroll[1] )
            # The Scroll values are floats sometimes, and cause the character to jitter. To avoid this, we use ints
            rendered_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.display.blit(self.assets['background'], (0,0))
            self.clouds.update()
            self.clouds.render(self.display, camera_offset=rendered_scroll)
            self.player.update(self.tilemap,(self.movement[1]-self.movement[0],0))
            self.tilemap.render(self.display, camera_offset = rendered_scroll)
            self.player.render(self.display, camera_offset = rendered_scroll )
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)  # limits FPS to 60
        pygame.quit()
Game().run()
