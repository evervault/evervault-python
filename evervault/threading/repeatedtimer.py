import logging
import threading

logger = logging.getLogger(__name__)


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        try:
            self.function(*self.args, **self.kwargs)
            self._create_and_start_timer()
        except Exception as e:
            logger.error("EVERVAULT :: An error occurred while polling - (%s)", e)

    def _create_and_start_timer(self):
        self.timer = threading.Timer(self.interval, self._run)
        self.timer.daemon = True
        self.timer.start()

    def start(self):
        if not self.is_running:
            self.is_running = True
            self._create_and_start_timer()

    def stop(self):
        self.timer.cancel()
        self.is_running = False

    def running(self):
        return self.is_running

    def get_interval(self):
        return self.interval

    def update_interval(self, interval):
        self.interval = interval
