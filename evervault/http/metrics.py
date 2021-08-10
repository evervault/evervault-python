import requests
import json
import time
import threading
import queue

METRICS_URL = 'https://metrics.evervault.com'

metric_event_queue = queue.Queue()


def worker():
    while True:
        data = metric_send_queue.get()
        requests.post(METRICS_URL, data=json.dumps(data))
        metric_send_queue.task_done()


# Thread to post metrics without blocking
threading.Thread(target=worker, daemon=True).start()


def report_metric():
    metric_event_queue.put({"data": "Data Encrypted"})
