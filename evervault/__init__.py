"""Package for the evervault SDK"""
from .client import Client
from .version import VERSION
from .errors.evervault_errors import AuthenticationError

__version__ = VERSION

ev_client = None
api_key = None
request_timeout = 30
base_url = "https://api.evervault.com/"
base_run_url = "https://cage.run/"


def run(cage_name, encrypted_data):
    return __client().run(cage_name, encrypted_data)


def encrypt(data):
    return __client().encrypt(data)


def encrypt_and_run(cage_name, data):
    return __client().encrypt_and_run(cage_name, data)


def cages():
    return __client().cages()


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
        )
        return ev_client
    else:
        return ev_client
