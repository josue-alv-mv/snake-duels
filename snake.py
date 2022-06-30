import pygame as pg
import time
import random
import threading

class Snake:
    def __init__(self, images_urls, sounds):
        self.surfaces = {
            "head": {
                "left": pg.image.load(images_urls["head"]["left"]).convert_alpha(),
                "right": pg.image.load(images_urls["head"]["right"]).convert_alpha(),
                "up": pg.image.load(images_urls["head"]["up"]).convert_alpha(),
                "down": pg.image.load(images_urls["head"]["down"]).convert_alpha()
            },
            "body": pg.image.load(images_urls["body"])
        }
        self.sounds = sounds
        self.rect = None
        self.x = None
        self.y = None
        self.body = []
        self.direction = None
        self.velocity = 350
        self.time_of_last_movement = None
        self.body_update_interval = 1/60
        self.protected = False
        self.ready = False
        self.active = False
        self.start_thread()

    def start_thread(self):
        thread = threading.Thread(target=self.update_body, daemon=True)
        thread.start()

    def move(self):
        if self.active:
            if self.time_of_last_movement is None:
                self.time_of_last_movement = time.time()
            
            elapsed_time = time.time() - self.time_of_last_movement
            step_distance = self.velocity * elapsed_time

            if self.direction == "left":
                self.x -= step_distance

            elif self.direction == "right":
                self.x += step_distance

            elif self.direction == "up":
                self.y -= step_distance

            elif self.direction == "down":
                self.y += step_distance

            self.rect.topleft = self.x, self.y
            self.time_of_last_movement = time.time()

    def get_inside_canvas(self, canvas):
        if self.active:
            if self.rect.centerx < 0:
                self.rect.centerx = canvas.width
                self.x, self.y = self.rect.topleft

            elif self.rect.centerx > canvas.width:
                self.rect.centerx = 0
                self.x, self.y = self.rect.topleft

            if self.rect.centery < 0:
                self.rect.centery = canvas.height
                self.x, self.y = self.rect.topleft

            elif self.rect.centery > canvas.height:
                self.rect.centery = 0
                self.x, self.y = self.rect.topleft

    def update_body(self):
        while True:
            if self.active:
                self.body.append(self.rect.copy())
                self.body = self.body[-self.length:]
            
            time.sleep(self.body_update_interval)
            

    def collide_snake(self, snake):
        if self.active and snake.active and not self.protected:
            return self.rect.colliderect(snake.rect) or self.rect.collidelist(snake.body) != -1

    def collide_apple(self, apple):
        if self.active and apple.active:
            return self.rect.colliderect(apple.rect)

    def play_sound(self):
        sound = random.choice(self.sounds)
        sound.play()

    def draw(self, canvas):
        if self.active:
            draw = not self.protected or (self.protected and time.time() % 0.3 < 0.15)
            if draw:
                for rect in self.body:
                    canvas.blit(self.surfaces["body"], rect)
                canvas.blit(self.surfaces["head"][self.direction], self.rect)
