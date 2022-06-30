import pygame as pg
from sys import exit
from network import Client, Server
from canvas import Canvas
from image import Image
from tile import Tile
from player import Player
from opponent import Opponent
from apple import Apple
from button import Button
from text import Text
from text_field import TextField
from score_board import ScoreBoard
from result_board import ResultBoard
from bg_animation import BgAnimation

class Game:
    def __init__(self):
        pg.init()
        self.canvas = Canvas(width=1152, height=640, caption="Snake Duels", icon_url="./images/icon.png")
        self.images = {
            "title": Image("./images/title.png", "center", self.canvas.centerx, self.canvas.centery - 128)
        }
        self.backgrounds = {
            "grass": Tile("./images/grass.png")
        }
        self.bg_animation = BgAnimation(
            canvas_width=self.canvas.width, canvas_height=self.canvas.height, rect_alpha=150
        )
        self.sounds = {
            "button": pg.mixer.Sound("./sounds/button.ogg"),
            "key": pg.mixer.Sound("./sounds/key.ogg"),
            "connection_error": pg.mixer.Sound("./sounds/connection_error.ogg"),
            "apple": [
                pg.mixer.Sound("./sounds/apple_1.ogg"),
                pg.mixer.Sound("./sounds/apple_2.ogg")
            ],
            "snake_death": [
                pg.mixer.Sound("./sounds/snake_death_1.ogg"),
                pg.mixer.Sound("./sounds/snake_death_2.ogg")
            ],
            "time_up": pg.mixer.Sound("./sounds/time_up.ogg")
        }
        self.player = Player(
            images_urls={
                "head": {
                    "left": "./images/player_head_left.png",
                    "right": "./images/player_head_right.png",
                    "up": "./images/player_head_up.png",
                    "down": "./images/player_head_down.png"
                },
                "body": "./images/player_body.png"
            }, sounds=self.sounds["snake_death"]
        )
        self.opponent = Opponent(
            images_urls={
                "head": {
                    "left": "./images/opponent_head_left.png",
                    "right": "./images/opponent_head_right.png",
                    "up": "./images/opponent_head_up.png",
                    "down": "./images/opponent_head_down.png"
                },
                "body": "./images/opponent_body.png"
            }, sounds=self.sounds["snake_death"]
        )
        self.apple = Apple(
            image_url="./images/apple.png", canvas_width=self.canvas.width,
            canvas_height=self.canvas.height, sounds=self.sounds["apple"]
        )
        self.score_board = ScoreBoard(
            width=self.canvas.width, height=64, rect_alpha=96, player_text_color=(64,255,255),
            opponent_text_color=(255,160,80), timer_color="white"
        )
        self.result_board = ResultBoard(
            center_x=self.canvas.centerx, center_y=self.canvas.centery, width=448, height=256,
            rect_alpha=96, font_size=72, font_colors={
                "win": (64,255,255), "loss": (255,160,80), "draw": (255,255,255)
            }
        )
        self.texts = {
            "credits_1_left": Text(
                hotspot="midright", x=self.canvas.centerx - 8, y=self.canvas.height - 48,
                text="Made by:", font_name="Consolas", font_color=(255,160,80)
            ),
            "credits_1_right": Text(
                hotspot="midleft", x=self.canvas.centerx + 8, y=self.canvas.height - 48,
                text="Nordss", font_name="Consolas", font_color=(64,255,255)
            ),
            "credits_2_left": Text(
                hotspot="midright", x=self.canvas.centerx - 8, y=self.canvas.height - 16,
                text="Special thanks to:", font_name="Consolas", font_color=(255,160,80)
            ),
            "credits_2_right": Text(
                hotspot="midleft", x=self.canvas.centerx + 8, y=self.canvas.height - 16,
                text="Daniel & Tharcy", font_name="Consolas", font_color=(64,255,255)
            ),
            "waiting": Text(
                hotspot="center", x=self.canvas.centerx, y=self.canvas.centery - 32,
                text="Waiting for opponent...", font_name="Consolas", font_size=36, bold=True
            ),
            "ip_address": Text(
                hotspot="center", x=self.canvas.centerx, y=self.canvas.centery - 64,
                text="",font_name="Consolas", font_size=32, bold=True
            ),
            "player_status": Text(
                hotspot="center", x=self.canvas.centerx, y=self.canvas.centery - 32,
                text="", font_size=48, font_color=(64,255,255)
            ),
            "opponent_status": Text(
                hotspot="center", x=self.canvas.centerx, y=self.canvas.centery + 32,
                text="", font_size=48, font_color=(255,160,80)
            ),
            "controls": Text(
                hotspot="center", x=self.canvas.centerx, y=self.canvas.height - 16,
                text="Use WASD or Arrow keys to move your snake", font_name="Consolas"
            )
        }
        self.text_field = TextField(
            hotspot="center", x=self.canvas.centerx, y=self.canvas.centery,
            width=300, height=50, font_size=24, max_text_length=15, rect_alpha=64,
            keys=['0','1','2','3','4','5','6','7','8','9','.']
        )
        self.buttons = {
            "host_game": Button(
                hotspot="center", x=self.canvas.centerx, y=self.canvas.centery,
                width=180, height=60, text="Host Game"
            ),
            "join_game": Button(
                hotspot="center", x=self.canvas.centerx, y=self.canvas.centery + 96,
                width=180, height=60, text="Join Game"
            ),
            "join": Button(
                hotspot="midleft", x=self.canvas.centerx + 16, y=self.canvas.centery + 80,
                width=96, height=40, text="Join"
            ),
            "back_host": Button(
                hotspot="center", x=self.canvas.centerx, y=self.canvas.centery + 32,
                width=96, height=40, text="Back"
            ),
            "back_join": Button(
                hotspot="midright", x=self.canvas.centerx - 16, y=self.canvas.centery + 80,
                width=96, height=40, text="Back"
            ),
            "back_waiting": Button(
                hotspot="midright", x=self.canvas.centerx - 16, y=self.canvas.centery + 96,
                width=96, height=40, text="Back"
            ),
            "ready": Button(
                hotspot="midleft", x=self.canvas.centerx + 16, y=self.canvas.centery + 96,
                width=96, height=40, text="Ready"
            )
        }
        self.events = {
            "send_player_json": pg.USEREVENT + 1,
        }
        pg.time.set_timer(self.events["send_player_json"], 500)

    def run(self):
        self.canvas.set_caption("Snake Duels")

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                elif event.type == pg.MOUSEMOTION:
                    self.buttons["host_game"].update()
                    self.buttons["join_game"].update()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.buttons["host_game"].focused:
                        self.sounds["button"].play()
                        self.run_host_room()

                    elif self.buttons["join_game"].focused:
                        self.sounds["button"].play()
                        self.run_client_room()

            self.bg_animation.draw(self.canvas)
            self.images["title"].draw(self.canvas)
            self.buttons["host_game"].draw(self.canvas)
            self.buttons["join_game"].draw(self.canvas)
            self.texts["credits_1_left"].draw(self.canvas)
            self.texts["credits_1_right"].draw(self.canvas)
            self.texts["credits_2_left"].draw(self.canvas)
            self.texts["credits_2_right"].draw(self.canvas)
            self.canvas.update()

    def run_host_room(self):
        self.network = Server()
        self.network.bind()
        self.canvas.set_caption("Snake Duels (Host)")

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                elif event.type == pg.MOUSEMOTION:
                    self.buttons["back_host"].update()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.buttons["back_host"].focused:
                        self.sounds["button"].play()
                        self.network.close()
                        self.run()

            if self.network.get():
                self.run_waiting_room()

            self.bg_animation.draw(self.canvas)
            self.texts["waiting"].draw(self.canvas)
            self.buttons["back_host"].draw(self.canvas)
            self.canvas.update()

    def run_client_room(self):
        self.network = Client()
        self.canvas.set_caption("Snake Duels")
        self.texts["ip_address"].text = "IP Address"
        pg.key.set_repeat(500, 70)
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                elif event.type == pg.MOUSEMOTION:
                    self.buttons["back_join"].update()
                    self.buttons["join"].update()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.buttons["back_join"].focused:
                        self.sounds["button"].play()
                        self.run()

                    elif self.buttons["join"].focused:
                        self.sounds["button"].play()
                        try:
                            if self.text_field.text == "":
                                self.text_field.text = "127.0.0.1"

                            self.network.connect(self.text_field.text)
                            self.network.send(tag="", message="")
                            self.run_waiting_room()

                        except Exception as e:
                            print(e)
                            self.sounds["connection_error"].play()
                            self.texts["ip_address"].text = "Couldn't connect to server!"
                            self.text_field.text = ""
                        
                elif event.type == pg.KEYDOWN:
                    if event.unicode in self.text_field.keys:
                        self.text_field.old_text = self.text_field.text
                        self.text_field.on_press(event.unicode)

                        if self.text_field.text != self.text_field.old_text:
                            self.sounds["key"].play()

            self.bg_animation.draw(self.canvas)
            self.texts["ip_address"].draw(self.canvas)
            self.text_field.draw(self.canvas)
            self.buttons["back_join"].draw(self.canvas)
            self.buttons["join"].draw(self.canvas)
            self.canvas.update()

    def run_waiting_room(self):
        if not self.network.is_host:
            self.canvas.set_caption("Snake Duels (Client)")

        self.player.ready = False
        self.opponent.ready = False
        self.network.send(tag="get", message="ready_state")

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                elif event.type == pg.MOUSEMOTION:
                    self.buttons["back_waiting"].update()
                    self.buttons["ready"].update()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.buttons["back_waiting"].focused:
                        self.sounds["button"].play()
                        self.network.close()
                        self.run()

                    elif self.buttons["ready"].focused:
                        self.sounds["button"].play()
                        self.player.ready = True
                        self.network.send(tag="ready", message="1")

            for tag, message in self.network.get():
                if tag == "get" and message == "ready_state":
                    self.network.send(tag="ready", message=str(int(self.player.ready)))

                elif tag == "ready":    
                    self.opponent.ready = bool(int(message))

            if not self.network.active:
                if self.network.is_host:
                    self.run_host_room()
                else:
                    self.run_client_room()

            if self.player.ready and self.opponent.ready:
                self.run_match()

            self.texts["player_status"].text = "You: ready!" if self.player.ready else "You: waiting..."
            self.texts["opponent_status"].text = "Opponent: ready!" if self.opponent.ready else "Opponent: waiting..."

            self.bg_animation.draw(self.canvas)
            self.texts["player_status"].draw(self.canvas)
            self.texts["opponent_status"].draw(self.canvas)
            self.buttons["back_waiting"].draw(self.canvas)
            self.buttons["ready"].draw(self.canvas)
            self.texts["controls"].draw(self.canvas)
            self.canvas.update()

    def run_match(self):
        self.opponent.reset()
        self.apple.reset()
        self.score_board.reset()
        self.result_board.reset()
        pg.key.set_repeat(0, 0)

        if self.network.is_host:
            self.player.spawn(x=48, y=48 + self.score_board.rect.height, direction="right")
            self.apple.spawn()
            self.score_board.timer.start()

        else:
            self.player.spawn(x=self.canvas.width - 48, y=self.canvas.height - 48, direction="left")

        while True:
            for event in pg.event.get(eventtype=pg.KEYDOWN):
                if event.key in self.player.keys:
                    self.player.set_direction(event.key)
                    self.player.send_json(self.network)
                    break

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                elif event.type == self.events["send_player_json"]:
                    self.player.send_json(self.network)

                elif self.result_board.active:
                    if event.type == pg.MOUSEMOTION:
                        self.result_board.button_back.update()

                    elif event.type == pg.MOUSEBUTTONDOWN and self.result_board.button_back.focused:
                        self.sounds["button"].play()
                        self.run_waiting_room()

            # network
            for tag, message in self.network.get():
                # network common events
                if tag == "player":
                    self.opponent.load_json(message)

                # network host events
                if self.network.is_host:
                    if tag == "get" and message == "apple":
                        self.apple.send_json(self.network)

                    elif tag == "increase" and message == "host_score":
                        self.score_board.player_score += 1
                        self.score_board.send_json(self.network)
                        
                # network client events
                else:
                    if tag == "apple":
                        self.apple.load_json(message)

                    elif tag == "respawn":
                        self.player.respawn()
                        self.player.send_json(self.network, respawned=True)

                    elif tag == "increase" and message == "length":
                        self.player.length += self.apple.value
                        self.player.send_json(self.network)

                    elif tag == "score":
                        self.score_board.load_json(message)

                    elif tag == "timer":
                        self.score_board.timer.load(message)

            if not self.network.active:
                if self.network.is_host:
                    self.run_host_room()
                else:
                    self.run_client_room()

            if not self.network.is_host and not self.apple.active:
                self.network.send(tag="get", message="apple")

            # logic
            if self.score_board.timer.remaining_time > 0:
                self.player.move()
                self.player.get_inside_canvas(self.canvas)
                self.opponent.move()
                self.opponent.get_inside_canvas(self.canvas)

                # logic (host)
                if self.network.is_host:
                    # timer update
                    self.score_board.timer.update()

                    if not self.score_board.timer.synced:
                        self.score_board.timer.send_json(self.network)

                    # snake collisions
                    if self.player.collide_snake(self.opponent) and self.opponent.collide_snake(self.player):
                        self.player.respawn()
                        self.opponent.active = False
                        self.score_board.player_score += 1
                        self.score_board.opponent_score += 1
                        self.network.send(tag="respawn", message="client")
                        self.player.send_json(self.network, respawned=True)
                        self.score_board.send_json(self.network)

                    elif self.player.collide_itself() or self.player.collide_snake(self.opponent):
                        self.player.respawn()
                        self.score_board.opponent_score += 1
                        self.player.send_json(self.network, respawned=True)
                        self.score_board.send_json(self.network)

                    elif self.opponent.collide_snake(self.player):
                        self.opponent.active = False
                        self.score_board.player_score += 1
                        self.network.send(tag="respawn", message="client")
                        self.score_board.send_json(self.network)

                    # apple collisions
                    if self.player.collide_apple(self.apple):
                        self.player.length += self.apple.value
                        self.apple.respawn()
                        self.player.send_json(self.network)
                        self.apple.send_json(self.network, play_sound=True)

                    elif self.opponent.collide_apple(self.apple):
                        self.apple.respawn()
                        self.network.send(tag="increase", message="length")
                        self.apple.send_json(self.network, play_sound=True)

                # logic (client)
                else:
                    if self.player.collide_itself():
                        self.player.respawn()
                        self.player.send_json(self.network, respawned=True)
                        self.network.send(tag="increase", message="host_score")

            elif not self.result_board.active:
                self.result_board.load(self.score_board)
                self.sounds["time_up"].play()

            # canvas
            self.backgrounds["grass"].draw(self.canvas)
            self.player.draw(self.canvas)
            self.opponent.draw(self.canvas)
            self.apple.draw(self.canvas)
            self.score_board.draw(self.canvas)
            self.result_board.draw(self.canvas)
            self.canvas.update()

game = Game()
game.run()