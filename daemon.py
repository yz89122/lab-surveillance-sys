from threading import Thread
from time import sleep

class Daemon:
    def __init__(self, target, args=(), kwargs=None):
        self.thread = Thread(target=target, daemon=True, args=args, kwargs=kwargs)

    def start(self):
        self.thread.start()

class ClockedRunner:
    def __init__(self, loop, frequency, args=(), kwargs=None):
        self.loop = loop
        self.frequency = frequency
        self.args = args
        self.kwargs = kwargs
        self.thread = Thread(target=self.__job)

    def __job(self):
        if self.kwargs is None:
            self.kwargs = {}
        while True:
            self.loop(*self.args, **self.kwargs)
            sleep(1 / self.frequency)

    def start(self):
        self.thread.start()
