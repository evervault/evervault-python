"""Package for the evervault SDK"""
from .client import Client
from .errors.evervault_errors import AuthenticationError, UnsupportedCurveError
from .cages_v2 import CageRequestsSession
import os
import sys
from warnings import warn

__version__ = "3.0.0"

ev_client = None
_app_uuid = None
_api_key = None
request_timeout = 30
_retry = False
_curve = None

BASE_URL_DEFAULT = "https://api.evervault.com/"
BASE_RUN_URL_DEFAULT = "https://run.evervault.com/"
RELAY_URL_DEFAULT = "https://relay.evervault.com:443"
CA_HOST_DEFAULT = "https://ca.evervault.com"
CAGES_CA_HOST_DEFAULT = "https://cages-ca.evervault.com"
CAGES_HOST_DEFAULT = "cages.evervault.com"
MAX_FILE_SIZE_IN_MB_DEFAULT = 25

SUPPORTED_CURVES = ["SECP256K1", "SECP256R1"]


class Curves(object):
    SECP256K1 = "SECP256K1"
    SECP256R1 = "SECP256R1"


def init(
    app_id,
    api_key,
    decryption_domains=[],
    intercept=False,
    ignore_domains=[],
    retry=False,
    curve=Curves.SECP256K1,
    debug_requests=False,
    enable_outbound_relay=False,
):
    global _app_uuid
    global _api_key
    global _retry
    global _curve

    _app_uuid = app_id
    _api_key = api_key
    _retry = retry
    _curve = curve

    if intercept or len(ignore_domains) > 0 or len(decryption_domains) > 0:
        warn(
            """
                The `intercept`, `ignore_domains` & `decryption_domains` config options in the Evervault SDK are deprecated and slated for removal.\n
                You can now use the `enable_outbound_relay` method to enable Outbound Relay.\n
                For more details please see https://docs.evervault.com/reference/python-sdk#evervaultenable_outbound_relay
            """,
            DeprecationWarning,
            stacklevel=2,
        )

    if len(decryption_domains) > 0:
        __client().enable_outbound_relay(
            debug_requests, decryption_domains=decryption_domains
        )
    elif intercept or len(ignore_domains) > 0:
        __client().enable_outbound_relay(debug_requests, ignore_domains=ignore_domains)
    elif not intercept and enable_outbound_relay:
        __client().enable_outbound_relay(
            debug_requests,
            ignore_domains=ignore_domains,
            enable_outbound_relay=enable_outbound_relay,
        )


def run(function_name, data, options={"async": False, "version": None}):
    return __client().run(function_name, data, options)


def decrypt(data):
    return __client().decrypt(data)


def encrypt(data):
    return __client().encrypt(data)


def encrypt_and_run(cage_name, data, options={"async": False, "version": None}):
    warn(
        "The `encrypt_and_run` method is deprecated and slated for removal. Please use the `encrypt` and `run` methods instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return __client().encrypt_and_run(cage_name, data, options)


def cages():
    warn(
        "The `cages` method is deprecated and slated for removal. For more details please see https://docs.evervault.com/reference/python-sdk",
        DeprecationWarning,
        stacklevel=2,
    )
    return __client().cages()


def cage_requests_session(cage_attestation_data={}):
    return CageRequestsSession(
        cage_attestation_data,
        os.environ.get("EV_CAGES_CA_HOST", CAGES_CA_HOST_DEFAULT),
        os.environ.get("EV_CAGES_HOST", CAGES_HOST_DEFAULT),
    )


def create_run_token(function_name, data={}):
    return __client().create_run_token(function_name, data)


def enable_outbound_relay(
    decryption_domains=None, debug_requests=False, client_session=None
):
    if client_session is not None:
        _warn_if_python_version_unsupported_for_async()

    if decryption_domains is None:
        __client().enable_outbound_relay(
            debug_requests, enable_outbound_relay=True, client_session=client_session
        )
    else:
        __client().enable_outbound_relay(
            debug_requests, decryption_domains=decryption_domains
        )


def _warn_if_python_version_unsupported_for_async():
    if sys.version_info.minor < 11:
        warn(
            "Using Outbound Relay with Asynchronous Python is only supported in Python >= 3.11"
        )


def __client():
    if not _app_uuid:
        raise AuthenticationError(
            "Your App's App UUID must be entered using evervault.init('<APP-ID>', '<API-KEY>')"
        )
    if not _api_key:
        raise AuthenticationError(
            "Your App's API Key must be entered using evervault.init('<APP-ID>', '<API-KEY>')"
        )
    if _curve not in SUPPORTED_CURVES:
        raise UnsupportedCurveError(f"The {_curve} curve is not supported.")
    global ev_client
    if not ev_client:
        max_file_size_in_mb = int(
            os.environ.get("EV_MAX_FILE_SIZE_IN_MB", MAX_FILE_SIZE_IN_MB_DEFAULT)
        )
        ev_client = Client(
            api_key=_api_key,
            app_uuid=_app_uuid,
            request_timeout=request_timeout,
            base_url=os.environ.get("EV_API_URL", BASE_URL_DEFAULT),
            base_run_url=os.environ.get("EV_CAGE_RUN_URL", BASE_RUN_URL_DEFAULT),
            relay_url=os.environ.get("EV_TUNNEL_HOSTNAME", RELAY_URL_DEFAULT),
            ca_host=os.environ.get("EV_CERT_HOSTNAME", CA_HOST_DEFAULT),
            retry=_retry,
            curve=_curve,
            max_file_size_in_mb=max_file_size_in_mb,
        )
        return ev_client
    else:
        return ev_client
