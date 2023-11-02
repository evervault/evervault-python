import logging
from evervault.threading.repeatedtimer import RepeatedTimer
import requests
import threading
import warnings


logger = logging.getLogger(__name__)


class AttestationDoc:
    def __init__(self, app_uuid, cage_names, cage_host, poll_interval=300):
        self.cage_host = cage_host
        self.app_uuid = app_uuid.replace("_", "-")
        self.cage_names = cage_names
        self.poll_interval = poll_interval
        self.lock = threading.Lock()
        self.cache = {}

        self.__get_attestation_docs()

        self.repeated_timer = RepeatedTimer(
            self.poll_interval,
            self.__get_attestation_docs,
        )

    def get(self, cage_name) -> str:
        with self.lock:
            try:
                return self.cache[cage_name]
            except KeyError:
                (_, doc) = self.__get_attestation_doc(cage_name)
                self.cache[cage_name] = doc
                return doc

    def get_poll_interval(self) -> list:
        return self.repeated_timer.get_interval()

    def disable_polling(self):
        if self.repeated_timer is not None:
            self.repeated_timer.stop()
            self.repeated_timer = None

    def clear_cache(self):
        with self.lock:
            self.cache = None

    def update_cache(self, docs):
        with self.lock:
            self.cache = docs

    def load_doc(self, cage_name):
        self.__get_attestation_doc(cage_name)

    def __get_attestation_docs(self):
        logger.debug("EVERVAULT :: Retrieving attestation doc from Cage")
        docs = dict(list(map(self.__get_attestation_doc, self.cage_names)))
        self.update_cache(docs)

    def __get_attestation_doc(self, cage_name):
        try:
            url = f"https://{cage_name}.{self.app_uuid}.{self.cage_host}/.well-known/attestation"
            res = requests.get(url)
            body = res.json()
            return (cage_name, body["attestation_doc"])
        except Exception as e:
            warnings.warn(f"Could not retrieve attestation doc from {url} {e}")
