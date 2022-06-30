from snake import Snake
import json

class Opponent(Snake):
    def __init__(self, images_urls, sounds):
        super().__init__(images_urls, sounds)

    def load_json(self, message):
        """
        h: head
        d: direction
        l: length
        p: protected
        r: respawned (clear body and play sound)
        """
        data = json.loads(message)
        self.rect = self.surfaces["body"].get_rect(topleft=data["h"])
        self.x, self.y = data["h"]
        self.direction = data["d"]
        self.length = data["l"]
        self.protected = bool(data["p"])
        if "r" in data:
            self.body.clear()
            self.play_sound()
            
        self.active = True

    def reset(self):
        self.active = False
        self.rect = None
        self.x = None
        self.y = None
        self.direction = None
        self.length = None
        self.body.clear()