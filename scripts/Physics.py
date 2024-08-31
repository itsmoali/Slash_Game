# Class For Implementing Physics related things, like movement and stuff
import pygame


class Physics:
    
    def __init__(self, game, e_type, pos, size):
        # Game: Game object
        # e_type: Entity Type
        # pos: Position of Entity -- Should be a list so that individual entities can be accessed
        # size: Size of Entity
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size= size
        self.velocity = [0,0]
        self.collisions = {"left":False,"right":False,"top":False, "bottom":False}

    def create_rect(self):
        #created a rect around the player
        return pygame.Rect(self.pos[0] , self.pos[1], self.size[0], self.size[1])

    def update(self,tilemap, movement=(0,0)):
        self.collisions = {"left":False,"right":False,"top":False, "bottom":False}
        frame_movement = (movement[0] + self.velocity[0] , movement[1] + self.velocity[1]) 

        #X-axis
        self.pos[0] += frame_movement[0]
        #Loops over the tilemap, which have collision rects, and sees which tiles are colliding with the player
        entity_rect = self.create_rect() # Player collison rect
        for rect in tilemap.physics_rects(self.pos):
            if entity_rect.colliderect(rect): #Checks if the player rect and tile rect intersect
                if frame_movement[0] > 0: #Player is moving to the right
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if frame_movement[0] < 0: #Player is moving to the left
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                #We are moving the rect, instead of the player, to calculate collisions. So we can set the x-coordinate of the entity_rect
                #to the x-coordinate of the player, to determine the final position of the player.
                self.pos[0] = entity_rect.x 
                # We should not use the rect to represent the position of the player because rects can not be floats, which can cause prolems.
                #So instead we use the rect as a reference to the position of the player. 

        #Y-axis
        self.pos[1] += frame_movement[1]
        entity_rect = self.create_rect()
        for rect in tilemap.physics_rects(self.pos):
            if entity_rect.colliderect(rect): 
                if frame_movement[1] > 0: #Player is moving down 
                    entity_rect.bottom = rect.top
                    self.collisions["bottom"] = True
                if frame_movement[1] < 0: #Player is moving up 
                    entity_rect.top = rect.bottom   
                    self.collisions["top"] = True
                self.pos[1] = entity_rect.y 

        #Gravity -- If the player jumps, it should come down
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        #If we hit the top or bottom part the velocity would be 0
        if self.collisions["bottom"] or self.collisions["top"]:
            self.velocity[1] = 0
    def render(self, surf, camera_offset = (0,0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - camera_offset[0] , self.pos[1] - camera_offset[1]))
