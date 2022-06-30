import time

class Timer:
    def __init__(self):
        self.match_duration = 120
        self.start_time = None
        self.remaining_time = self.match_duration
        self.last_value_sent = -1
        self.synced = False

    def start(self):
        self.start_time = time.time()

    def update(self):
        self.remaining_time = self.match_duration - int(time.time() - self.start_time)

        if self.remaining_time < 0:
            self.remaining_time = 0

        self.synced = self.last_value_sent == self.remaining_time

    def get_text(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        return "%02d:%02d"%(minutes, seconds)

    def send_json(self, network):
        network.send(tag="timer", message=str(self.remaining_time))
        self.last_value_sent = self.remaining_time

    def load(self, message):
        self.remaining_time = int(message)

    def reset(self):
        self.start_time = None
        self.remaining_time = self.match_duration
        self.last_value_sent = -1
        self.synced = False