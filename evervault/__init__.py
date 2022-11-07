"""Package for the evervault SDK"""
from .client import Client
from .errors.evervault_errors import AuthenticationError, UnsupportedCurveError
import os

__version__ = "1.3.2"

ev_client = None
_api_key = None
request_timeout = 30
_retry = False
_curve = None

BASE_URL_DEFAULT = "https://api.evervault.com/"
BASE_RUN_URL_DEFAULT = "https://run.evervault.com/"
RELAY_URL_DEFAULT = "https://relay.evervault.com:443"
CA_HOST_DEFAULT = "https://ca.evervault.com"

SUPPORTED_CURVES = ["SECP256K1", "SECP256R1"]


class Curves(object):
    SECP256K1 = "SECP256K1"
    SECP256R1 = "SECP256R1"


def init(
    api_key,
    decryption_domains=[],
    intercept=False,
    ignore_domains=[],
    retry=False,
    curve=Curves.SECP256K1,
    debugRequests=False,
    enable_outbound_relay=False,
):
    global _api_key
    global _retry
    global _curve

    _api_key = api_key
    _retry = retry
    _curve = curve

    if intercept or len(ignore_domains) > 0 or len(decryption_domains) > 0:
        print(
            "The `intercept`,`ignore_domains` and `decryption_domains` config options in Evervault SDK are deprecated and slated for removal"
        )
        print("Please switch to the `enable_outbound_relay` config option.")
        print(
            "For more details please see https://docs.evervault.com/reference/python-sdk#evervaultinit"
        )

    if len(decryption_domains) > 0:
        __client().relay(debugRequests, decryption_domains=decryption_domains)
    elif intercept or len(ignore_domains) > 0:
        __client().relay(debugRequests, ignore_domains=ignore_domains)
    elif not intercept and enable_outbound_relay:
        __client().relay(
            debugRequests,
            ignore_domains=ignore_domains,
            enable_outbound_relay=enable_outbound_relay,
        )


def run(cage_name, data, options={"async": False, "version": None}):
    return __client().run(cage_name, data, options)


def encrypt(data):
    return __client().encrypt(data)


def encrypt_and_run(cage_name, data, options={"async": False, "version": None}):
    return __client().encrypt_and_run(cage_name, data, options)


def cages():
    return __client().cages()


def create_run_token(cage_name, data):
    return __client().create_run_token(cage_name, data)


def __client():
    if not _api_key:
        raise AuthenticationError(
            "Your Team's API Key must be entered using evervault.init('<API-KEY>')"
        )
    if _curve not in SUPPORTED_CURVES:
        raise UnsupportedCurveError(f"The {_curve} curve is not supported.")
    global ev_client
    if not ev_client:
        ev_client = Client(
            api_key=_api_key,
            request_timeout=request_timeout,
            base_url=os.environ.get("EV_API_URL", BASE_URL_DEFAULT),
            base_run_url=os.environ.get("EV_CAGE_RUN_URL", BASE_RUN_URL_DEFAULT),
            relay_url=os.environ.get("EV_TUNNEL_HOSTNAME", RELAY_URL_DEFAULT),
            ca_host=os.environ.get("EV_CERT_HOSTNAME", CA_HOST_DEFAULT),
            retry=_retry,
            curve=_curve,
        )
        return ev_client
    else:
        return ev_client
