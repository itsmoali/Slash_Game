import random

class Cloud:
    def __init__(self, pos, img, speed, sky_pos):
        self.pos = list(pos)
        self.speed = speed
        self.sky_pos = sky_pos
        self.img = img

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset_pos=(0,0)):
        #The Position that the cloud would be created on, while taking into account camera offset. Sky_pos adds a randomized depth factor so all clouds aint same
        render_position = (self.pos[0] - offset_pos[0] * self.sky_pos , self.pos[1] - offset_pos[1] * self.sky_pos)
        #The x and y components for the clouds, to form a loop. Meaning that the clouds would move infinitley due to the modulo.
        x_comp = render_position[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width()
        y_comp = render_position[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()
        surf.blit(self.img, (x_comp, y_comp))

class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []
        for i in range(count):
            self.clouds.append(Cloud((random.random()*9999,random.random()*999),random.choice(cloud_images), random.random() * 0.05 + 0.05, random.random()*0.6+0.2))
        self.clouds.sort(key=lambda x: x.sky_pos)

    def update(self):
        #We are individually updating the position of each cloud. Each cloud is an Object of the "Cloud" class, and has the update method for it
        #Meaing that we are actually just using the update method defined above
        for cloud in self.clouds:
            cloud.update()

    def render(self,surf,camera_offset=(0,0)):
        #Again just looping over each cloud, and using the render method associated with the Cloud class.
        for cloud in self.clouds:
            cloud.render(surf,offset_pos=camera_offset)


            #Investigate why this is not working correctly
            # def render(self, surf, offset_pos=(0,0)):
            #     #The Position that the cloud would be created on. Sky_pos adds a depth factor
            #     render_position = (self.pos[0] - offset_pos[0] * self.sky_pos, self.pos[1] - offset_pos[1] * self.sky_pos)
            #     #The x and y components for the clouds, to form a loop. Meaning that the clouds would move infinitley due to the modulo.
            #
            #     x_comp =(surf.get_width() + self.img.get_width()) - self.img.get_width()
            #     y_comp = (surf.get_height() + self.img.get_height()) - self.img.get_height()
            #     print(x_comp, y_comp)
            #     print(render_position[0] % x_comp, render_position[1] % y_comp)
            #     surf.blit(self.img, (render_position[0] % x_comp, render_position[1] % y_comp))
            # surf.blit(self.img, (render_position[0] % (surf.get_width() +self.img.get_width()) - self.img.get_width(),render_position[1] % (surf.get_height() +self.img.get_height()) - self.img.get_height()))

