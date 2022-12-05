import threading
import time


class RepeatedTimer(threading.Thread):
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        while not self.stopEvent.wait(self.interval):
            self.function(*self.args, **self.kwargs)

    def running(self):
        return self.is_running

    def update_interval(self, interval):
        self.interval = interval
        self.stop()
        self.start()

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.stopEvent = threading.Event()
            thread = threading.Thread(target = self._run)
            thread.start()

    def stop(self):
        self.stopEvent.set()
        self.is_running = False
