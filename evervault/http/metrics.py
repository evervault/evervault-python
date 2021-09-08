import requests
import threading
import queue
import evervault
import os


def post_metric(api_key, count):
    # api_url = os.environ.get("EV_API_URL", evervault.BASE_URL_DEFAULT)
    api_url = 'https://api.evervault.io/' # During development use the staging server
    url = f'{api_url}metrics/sdkEncryptions?sdk=python&numEncryptions={count}'

    headers = { 'Api-Key': api_key }
    return requests.post(url, headers=headers)
        

metric_event_queue = queue.Queue()

def worker():
    while True:
        # try:
        data = metric_event_queue.get()

        a = post_metric(data['api_key'], 1)
        
        metric_event_queue.task_done()
        # except:
        #     pass

# Thread to post metrics without blocking
threading.Thread(target=worker, daemon=True).start()

def report_metric(api_key):
    metric_event_queue.put({"data": "Data Encrypted", "api_key": api_key})
