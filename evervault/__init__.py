"""Package for the evervault SDK"""
from .client import Client
from .errors.evervault_errors import AuthenticationError
import os

__version__ = "0.3.0"

ev_client = None
_api_key = None
request_timeout = 30

BASE_URL_DEFAULT = "https://api.evervault.com/"
BASE_RUN_URL_DEFAULT = "https://run.evervault.com/"
RELAY_URL_DEFAULT = "https://relay.evervault.com:443"
CA_HOST_DEFAULT = "https://ca.evervault.com"


def init(api_key, intercept=True, ignore_domains=[]):
    global _api_key
    _api_key = api_key
    if intercept:
        __client().relay(ignore_domains)


def run(cage_name, data, options={"async": False, "version": None}):
    return __client().run(cage_name, data, options)


def encrypt(data):
    return __client().encrypt(data)


def encrypt_and_run(cage_name, data, options={"async": False, "version": None}):
    return __client().encrypt_and_run(cage_name, data, options)


def cages():
    return __client().cages()


def __client():
    if not _api_key:
        raise AuthenticationError(
            "Your Team's API Key must be entered using evervault.init('<API-KEY>')"
        )
    global ev_client
    if not ev_client:
        ev_client = Client(
            api_key=_api_key,
            request_timeout=request_timeout,
            base_url=os.environ.get("EV_API_URL", BASE_URL_DEFAULT),
            base_run_url=os.environ.get("EV_CAGE_RUN_URL", BASE_RUN_URL_DEFAULT),
            relay_url=os.environ.get("EV_TUNNEL_HOSTNAME", RELAY_URL_DEFAULT),
            ca_host=os.environ.get("EV_CERT_HOSTNAME", CA_HOST_DEFAULT),
        )
        return ev_client
    else:
        return ev_client
