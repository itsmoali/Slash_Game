class Animation:
    def __init__(self,images, animation_dur = 5, loop = True): 
        self.images = images
        self.animation_dur = animation_dur
        self.loop= loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.animation_dur, self.loop)

    def update(self):
        #The loop will see if the animation is still running
        if self.loop:
            self.frame = (self.frame + 1) % (self.animation_dur * len(self.images))
        else:
            #The last frame for the animations. Use -1 to account for counting from index 0
            self.frame = min(self.frame, self.animation_dur * len(self.images) - 1)
            #Just to make sure that all the images have been rendered and we dont break mid animation
            if self.frame == self.animation_dur * len(self.images) -1:
                self.done = True


    def current_image(self):
        #Get the current animation image depending on game frame and animation duration
        return self.images[int(self.frame / self.animation_dur)]

