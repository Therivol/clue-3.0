import time


class Timer:
    timers = {}

    def __init__(self, name):
        self.start = time.time()
        self.end = 0
        self.runtime = 0
        self.timers[name] = self

    def stop(self):
        self.end = time.time()
        self.runtime = self.end - self.start
        return self.runtime

    @classmethod
    def get(cls, name):
        return cls.timers[name]
