import pygame as pg
import random
import json

class Apple:
    def __init__(self, image_url, canvas_width, canvas_height, sounds):
        self.surf = pg.image.load(image_url).convert_alpha()
        self.size = self.surf.get_width()
        self.rect = None
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.sounds = sounds
        self.value = 10
        self.active = False

    def spawn(self):
        self.respawn(play_sound=False)

    def respawn(self, play_sound=True):
        x = random.randint(0, self.canvas_width//self.size - 1) * self.size
        y = random.randint(0, self.canvas_height//self.size - 1) * self.size
        self.rect = self.surf.get_rect(topleft=(x,y))

        if play_sound:
            self.play_sound()

    def reset(self):
        self.rect = None
        self.active = False
    
    def draw(self, canvas):
        if self.active:
            canvas.blit(self.surf, self.rect)

    def play_sound(self):
        sound = random.choice(self.sounds)
        sound.play()

    def send_json(self, network, play_sound=False):
        # ps: play_sound
        data = {
            "x": self.rect.x,
            "y": self.rect.y
        }
        if play_sound:
            data["ps"] = 1

        json_text = json.dumps(data, separators=(",", ":"))
        network.send(tag="apple", message=json_text)
        self.active = True

    def load_json(self, message):
        # ps: play_sound
        data = json.loads(message)
        x = data["x"]
        y = data["y"]
        self.rect = self.surf.get_rect(topleft=(x, y))
        if "ps" in data:
            self.play_sound()

        self.active = True
