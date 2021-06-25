"""Package for the evervault SDK"""
from .client import Client
from .version import VERSION
from .errors.evervault_errors import AuthenticationError

__version__ = VERSION

ev_client = None
api_key = None
request_timeout = 30
base_url = "https://api.evervault.com/"
base_run_url = "https://run.evervault.com/"
relay_url="https://relay.evervault.com:443"


def run(cage_name, encrypted_data, options = { "async": False, "version": None }):
    return __client().run(cage_name, encrypted_data, options)


def encrypt(data):
    return __client().encrypt(data)


def encrypt_and_run(cage_name, data, options = { "async": False, "version": None }):
    return __client().encrypt_and_run(cage_name, data, options)


def cages():
    return __client().cages()

def relay(ignore_domains=[]):
    __client().relay(ignore_domains)


def __client():
    if not api_key:
        raise AuthenticationError("Please enter your team's API Key")
    global ev_client
    if not ev_client:
        ev_client = Client(
            api_key=api_key,
            request_timeout=request_timeout,
            base_url=base_url,
            base_run_url=base_run_url,
            relay_url=relay_url,
        )
        return ev_client
    else:
        return ev_client
