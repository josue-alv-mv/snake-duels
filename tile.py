import pygame as pg

class Tile:
    def __init__(self, image_url):
        self.surf = pg.image.load(image_url).convert()
        self.size = self.surf.get_width()

    def draw(self, canvas):
        for x in range(canvas.width // self.size + 1):
            for y in range(canvas.height // self.size + 1):
                canvas.blit(self.surf, (x*self.size, y*self.size))