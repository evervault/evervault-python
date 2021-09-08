import atexit
import requests
import threading
import queue
import evervault
import os


class ReportingScheduler(object):
    def __init__(self, interval, function):
        self.interval = interval
        self.function = function
        self.running = False
        self._timer = None

    def __call__(self):
        self.running = False
        self.start()
        self.function()

    def start(self):
        if self.running:
            return

        self._timer = threading.Timer(self.interval, self)
        self._timer.start()
        self.running = True

    def stop(self):
        if self._timer:
            self._timer.cancel()
        self.running = False
        self._timer = None


metric_event_queue = queue.Queue()


def post_metric(api_key, count):
    api_url = os.environ.get("EV_API_URL", evervault.BASE_URL_DEFAULT)
    url = f"{api_url}metrics/sdkEncryptions?sdk=python&numEncryptions={count}"

    headers = {"Api-Key": api_key}
    return requests.post(url, headers=headers)


def metric_report_schedule_manager():
    scheduler = ReportingScheduler(1.5, worker)
    scheduler.start()


def worker():
    encrypt_metric_batches = []

    current_api_key = None
    encrypt_count = 0

    while not metric_event_queue.empty():
        data = metric_event_queue.get()

        if current_api_key is not None and current_api_key != data["api_key"]:
            encrypt_metric_batches.append((current_api_key, encrypt_count))

        if current_api_key != data["api_key"]:
            current_api_key = data["api_key"]
            encrypt_count = 0

        encrypt_count += 1
        metric_event_queue.task_done()

    encrypt_metric_batches.append((current_api_key, encrypt_count))

    for (api_key, count) in encrypt_metric_batches:
        if count > 0:
            try:
                post_metric(api_key, count)
            except:
                pass


threading.Thread(target=metric_report_schedule_manager, daemon=True).start()


def report_metric(api_key):
    metric_event_queue.put({"api_key": api_key})


@atexit.register
def end_metrics_reporting():
    worker()
