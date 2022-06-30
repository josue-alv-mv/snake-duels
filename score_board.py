import pygame as pg
from text import Text
from timer import Timer
import json

class ScoreBoard:
    def __init__(self, width, height, rect_alpha, player_text_color, opponent_text_color, timer_color):
        self.rect_surf = pg.Surface((width, height))
        self.rect_surf.set_alpha(rect_alpha)
        self.rect = self.rect_surf.get_rect()
        self.texts = {
            "player_score": Text(
                hotspot="center", x=width//4, y=self.rect.centery,
                text="", font_name="Consolas", font_size=28, font_color=player_text_color,
            ),
            "opponent_score": Text(
                hotspot="center", x=width-(width//4), y=self.rect.centery,
                text="", font_name="Consolas", font_size=28, font_color=opponent_text_color
            ),
            "timer": Text(
                hotspot="center", x=self.rect.centerx, y=self.rect.centery,
                text="3:00", font_name="Consolas", font_size=36, font_color=timer_color
            )
        }
        self.player_score = 0
        self.opponent_score = 0
        self.timer = Timer()

    def draw(self, canvas):
        self.texts["player_score"].text = f"You: {self.player_score} kills"
        self.texts["opponent_score"].text = f"They: {self.opponent_score} kills"
        self.texts["timer"].text = self.timer.get_text()

        canvas.blit(self.rect_surf, (0,0))
        for text in self.texts.values():
            text.draw(canvas)

    def send_json(self, network):
        data = {
            "host": self.player_score,
            "client": self.opponent_score
        }
        json_text = json.dumps(data, separators=(",", ":"))
        network.send(tag="score", message=json_text)

    def load_json(self, message):
        data = json.loads(message)
        self.player_score = data["client"]
        self.opponent_score = data["host"]

    def reset(self):
        self.player_score = 0
        self.opponent_score = 0
        self.timer.reset()