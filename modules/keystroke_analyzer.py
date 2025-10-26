import time

class KeystrokeAnalyzer:
    def __init__(self):
        self.start_time = None

    def record_start(self):
        self.start_time = time.time()

    def analyze(self, message: str) -> str:
        if not self.start_time:
            return "normal"
        elapsed = time.time() - self.start_time
        if elapsed <= 0:
            return "normal"
        cps = len(message) / elapsed  # characters per second
        if cps < 2:
            return "stressed"
        if cps > 8:
            return "bored"
        return "normal"


