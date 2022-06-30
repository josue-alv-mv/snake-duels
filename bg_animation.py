from tile import Tile
from player import Player
import pygame as pg
import time
import random

class BgAnimation:
    def __init__(self, canvas_width, canvas_height, rect_alpha):
        self.bg = Tile("./images/grass.png")
        self.snake_1 = Player(
            images_urls={
                "head": {
                    "left": "./images/player_head_left.png",
                    "right": "./images/player_head_right.png",
                    "up": "./images/player_head_up.png",
                    "down": "./images/player_head_down.png"
                },
                "body": "./images/player_body.png"
            }, sounds=None
        )
        self.snake_1.spawn(x=96, y=96, direction="right")
        self.snake_1.length = random.randint(80, 120)
        self.snake_1.interval_of_change_of_dir = random.uniform(0.5, 1)
        self.snake_1.active = True

        self.snake_2 = Player(
            images_urls={
                "head": {
                    "left": "./images/opponent_head_left.png",
                    "right": "./images/opponent_head_right.png",
                    "up": "./images/opponent_head_up.png",
                    "down": "./images/opponent_head_down.png"
                },
                "body": "./images/opponent_body.png"
            }, sounds=None
        )
        self.snake_2.spawn(x=canvas_width-96, y=canvas_height-96, direction="left")
        self.snake_2.length = random.randint(80, 120)
        self.snake_2.interval_of_change_of_dir = random.uniform(0.5, 1)
        self.snake_2.active = True

        self.transparent_rect = pg.Surface((canvas_width, canvas_height))
        self.transparent_rect.set_alpha(rect_alpha)
        
    def draw(self, canvas):
        # update
        if time.time() - self.snake_1.time_of_last_change_of_dir > self.snake_1.interval_of_change_of_dir:
            new_direction = random.choice([pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN])
            self.snake_1.set_direction(new_direction)
            self.snake_1.interval_of_change_of_dir = random.uniform(0.5, 1)

        if time.time() - self.snake_2.time_of_last_change_of_dir > self.snake_2.interval_of_change_of_dir:
            new_direction = random.choice([pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN])
            self.snake_2.set_direction(new_direction)
            self.snake_2.interval_of_change_of_dir = random.uniform(0.5, 1)

        self.snake_1.move()
        self.snake_1.get_inside_canvas(canvas)

        self.snake_2.move()
        self.snake_2.get_inside_canvas(canvas)

        # draw
        self.bg.draw(canvas)
        self.snake_1.draw(canvas)
        self.snake_2.draw(canvas)
        canvas.blit(self.transparent_rect, (0,0))