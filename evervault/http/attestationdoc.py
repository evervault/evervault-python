import logging
from evervault.threading.repeatedtimer import RepeatedTimer
import requests
import threading
import warnings


logger = logging.getLogger(__name__)


class AttestationDoc:
    def __init__(self, app_uuid, names, cage_host, enclave_host, poll_interval=300):
        self.cage_host = cage_host
        self.enclave_host = enclave_host
        self.app_uuid = app_uuid.replace("_", "-")
        self.names = names
        self.poll_interval = poll_interval
        self.lock = threading.Lock()
        self.cache = {}

        self.__get_attestation_docs()

        self.repeated_timer = RepeatedTimer(
            self.poll_interval,
            self.__get_attestation_docs,
        )

    def get(self, name) -> str:
        with self.lock:
            try:
                return self.cache[name]
            except KeyError:
                (_, doc) = self.__get_attestation_doc(name)
                self.cache[name] = doc
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

    def load_doc(self, name):
        self.__get_attestation_doc(name)

    def __get_attestation_docs(self):
        logger.debug("EVERVAULT :: Retrieving attestation doc from Cage")
        docs = dict(list(map(self.__get_attestation_doc, self.names)))
        self.update_cache(docs)

    def __get_url(self, name, host):
        return f"https://{name}.{self.app_uuid}.{host}/.well-known/attestation"

    # While supporting both cage and enclave, we should attempt to get the attestation docs
    # from both the cage and enclave hosts.
    def __get_attestation_doc(self, name):
        try:
            cage_url = self.__get_url(name, self.cage_host)
            res = requests.get(cage_url)
            body = res.json()
            return (name, body["attestation_doc"])
        except Exception as cage_err:
            try:
                enclave_url = self.__get_url(name, self.enclave_host)
                res = requests.get(enclave_url)
                body = res.json()
                return (name, body["attestation_doc"])
            except Exception as enclave_err:
                warnings.warn(
                    f"Could not retrieve attestation doc from {cage_url}: {cage_err}. Or {enclave_url}: {enclave_err}"
                )
