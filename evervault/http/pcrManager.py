import logging
from evervault.threading.repeatedtimer import RepeatedTimer
import threading
import warnings
import time


logger = logging.getLogger(__name__)


class PcrManager:
    def __init__(self, attestation_data, poll_interval=300):
        self.attestation_data = attestation_data
        self.poll_interval = poll_interval
        self.lock = threading.Lock()
        self.store = {}

        self.__load_providers(attestation_data)
        self.__fetch_all_pcrs()

        logger.debug(
            "EVERVAULT :: PCR manager starting to poll for PCRs every {self.poll_interval} seconds"
        )

        self.repeated_timer = RepeatedTimer(
            self.poll_interval,
            self.__fetch_all_pcrs,
        )

    def get(self, cage_name) -> str:
        with self.lock:
            try:
                pcrs = self.store[cage_name]["pcrs"]
                if pcrs is None:
                    raise KeyError
                return pcrs
            except KeyError:
                pcrs = self.__fetch_pcrs(cage_name)
                self.store[cage_name]["pcrs"] = pcrs
                return pcrs

    def get_poll_interval(self) -> list:
        return self.repeated_timer.get_interval()

    def disable_polling(self):
        if self.repeated_timer is not None:
            self.repeated_timer.stop()
            self.repeated_timer = None

    def clear_store(self):
        with self.lock:
            self.store = {}

    def remove_pcrs_for_cage(self, cage_name):
        with self.lock:
            self.store[cage_name]["pcrs"] = None

    def __create_provider_from_static_pcrs(self, pcrs):
        def provider():
            return pcrs

        return provider

    def __load_providers(self, attestation_data):
        for cage_name, value in attestation_data.items():
            if callable(value):
                self.store[cage_name] = {"pcrs": None, "provider": value}
            elif isinstance(value, list):
                self.store[cage_name] = {
                    "pcrs": value,
                    "provider": self.__create_provider_from_static_pcrs(value),
                }
            elif isinstance(value, dict):
                self.store[cage_name] = {
                    "pcrs": [value],
                    "provider": self.__create_provider_from_static_pcrs([value]),
                }

            else:
                raise Exception("EVERVAULT :: Invalid PCR data. Cannot create provider")

    def __fetch_all_pcrs(self):
        logger.debug("EVERVAULT :: Retrieving PCRs from providers")
        for cage_name, provider in self.store.items():
            pcrs = self.__fetch_pcrs(cage_name)
            self.store[cage_name]["pcrs"] = pcrs

    def __fetch_pcrs(self, cage_name):
        try:
            provider = self.store[cage_name]["provider"]

            if provider is None:
                warnings.warn(
                    f"EVERVAULT :: No PCR provider registered for {cage_name}. Cannot fetch PCRs"
                )
                return None

            retries = 3
            delay = 0.5

            while retries > 0:
                try:
                    pcrs = provider()
                    logger.debug(
                        "EVERVAULT :: Retrieved PCRs from provider for {cage_name}"
                    )
                    return pcrs
                except Exception as e:
                    retries -= 1
                    if retries == 0:
                        raise e
                    else:
                        time.sleep(delay)
                        delay *= 2
                        warnings.warn(
                            f"EVERVAULT :: Could not get PCR for {cage_name} {e}"
                        )
                        continue
        except KeyError:
            warnings.warn(
                f"EVERVAULT :: No PCR provider registered for {cage_name}. Cannot fetch PCRs"
            )
            return None
