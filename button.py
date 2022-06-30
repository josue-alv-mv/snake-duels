import pygame as pg
import aa_rounded_rect

class Button:
    def __init__(
            self, hotspot, x, y, width, height, text, font_size=32,
            color = (0, 120, 240), color_focused=(0, 96, 192), border_radius=1, font_name = None,
            font_color = "white", bold = False, anti_aliasing = True):

        self.hotspot = hotspot
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.color_focused = color_focused
        self.border_radius = border_radius
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color
        self.bold = bold
        self.anti_aliasing = anti_aliasing
        self.focused = False

    def get_rect(self):
        rect = pg.Rect(0, 0, self.width, self.height)
        setattr(rect, self.hotspot, (self.x, self.y))
        return rect

    def draw(self, canvas):
        rect = self.get_rect()

        # draw rectangles
        color = self.color_focused if self.focused else self.color
        aa_rounded_rect.draw_rect(canvas, rect, color, self.border_radius)

        # draw text
        font = pg.font.SysFont(self.font_name, self.font_size, self.bold)
        text_surf = font.render(self.text, self.anti_aliasing, self.font_color)
        text_rect = text_surf.get_rect(center=rect.center)
        canvas.blit(text_surf, text_rect)
        
    def update(self):
        self.focused = self.get_rect().collidepoint(pg.mouse.get_pos())
