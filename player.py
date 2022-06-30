from snake import Snake
import pygame as pg
import json
import time
import threading

class Player(Snake):
    def __init__(self, images_urls, sounds):
        super().__init__(images_urls, sounds)
        self.keys = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_a, pg.K_d, pg.K_w, pg.K_s]
        self.spawn_data = {"length": 15}
        self.time_of_last_change_of_dir = -1

    def spawn(self, x, y, direction):
        self.spawn_data["x"] = x
        self.spawn_data["y"] = y
        self.spawn_data["direction"] = direction
        self.respawn(protected=False, play_sound=False)

    def respawn(self, protected=True, play_sound=True):
        self.body.clear()
        x,y = self.spawn_data["x"], self.spawn_data["y"]
        self.rect = self.surfaces["body"].get_rect(center=(x,y))
        self.x, self.y = self.rect.topleft
        self.direction = self.spawn_data["direction"]
        self.length = self.spawn_data["length"]
        self.protected = protected

        if play_sound:
            self.play_sound()

    def set_direction(self, key):
        min_distance = self.surfaces["body"].get_width()
        elapsed_time = time.time() - self.time_of_last_change_of_dir
        travelled_distance = self.velocity * elapsed_time

        if travelled_distance >= min_distance:
            new_direction = self.get_direction_by_key(key)

            if new_direction not in [self.direction, self.get_opposite_direction(self.direction)]:
                self.direction = new_direction
                self.time_of_last_change_of_dir = time.time()

    def get_direction_by_key(self, key):
        return {
            pg.K_LEFT: "left",
            pg.K_RIGHT: "right",
            pg.K_UP: "up",
            pg.K_DOWN: "down",
            pg.K_a: "left",
            pg.K_d: "right",
            pg.K_w: "up",
            pg.K_s: "down"
        }[key]

    def get_opposite_direction(self, direction):
        return {
            "left": "right",
            "right": "left",
            "up": "down",
            "down": "up"
        }[direction]
        
    def collide_itself(self):
        # collidelist returns the index of the first collision found
        # if no collisions are found an index of -1 is returned
        # -12 is the number where this function apparently does'nt returns false positive
        # so -18 is a good number (+50%) to avoid false collisions
        if self.active and not self.protected:
            return self.rect.collidelist(self.body[:-18]) != -1

    def timer_callback(self, network):
        self.protected = False
        self.send_json(network, False)
        
    def send_json(self, network, respawned=False):
        """
        h: head
        d: direction
        l: length
        p: protected
        r: respawned (clear body and play sound)
        """
        data = {
            "h": self.rect.topleft,
            "d": self.direction,
            "l": self.length,
            "p": int(self.protected)
        }
        if respawned:
            data["r"] = 1
            timer = threading.Timer(5, self.timer_callback, args=(network,))
            timer.start()

        json_text = json.dumps(data, separators=(',', ':'))
        network.send(tag="player", message=json_text)
        self.active = True