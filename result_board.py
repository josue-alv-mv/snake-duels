import pygame as pg
from text import Text
from button import Button

class ResultBoard:
    def __init__(
        self, center_x, center_y, width, height, rect_alpha,
        font_size, font_colors
    ):
        self.rect_surf = pg.Surface((width, height))
        self.rect_surf.set_alpha(rect_alpha)
        self.rect = self.rect_surf.get_rect(center=(center_x, center_y))
        self.text_result = Text(
            hotspot="center", x=self.rect.centerx, y=self.rect.y + self.rect.height//3,
            text="", font_size=font_size
        )
        self.button_back = Button(
            hotspot="center", x=self.rect.centerx, y=self.rect.y + (self.rect.height - self.rect.height//3),
            width=96, height=40, text="Back", font_size=32, color=(0, 120, 240),
            color_focused=(0, 96, 192)
        )
        self.font_colors = {
            "win": font_colors["win"],
            "loss": font_colors["loss"],
            "draw": font_colors["draw"]
        }
        self.active = False

    def draw(self, canvas):
        if self.active:
            canvas.blit(self.rect_surf, self.rect)
            self.text_result.draw(canvas)
            self.button_back.draw(canvas)

    def load(self, score_board):
        if score_board.player_score > score_board.opponent_score:
            self.text_result.text = "You won!"
            self.text_result.font_color = self.font_colors["win"]

        elif score_board.player_score < score_board.opponent_score:
            self.text_result.text = "You lost!"
            self.text_result.font_color = self.font_colors["loss"]

        else:
            self.text_result.text = "Draw!"
            self.text_result.font_color = self.font_colors["draw"]

        self.active = True

    def reset(self):
        self.text_result.text = ""
        self.text_result.font_color = (255,255,255)
        self.active = False