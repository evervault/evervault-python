"""Package for the evervault SDK"""
from .client import Client
from .errors.evervault_errors import EvervaultError
from .cages_v2 import CageRequestsSessionBeta, CageRequestsSession
import os
import sys
from warnings import warn
import warnings
from evervault.http.attestationdoc import AttestationDoc
from importlib import metadata

__version__ = metadata.version(__package__ or __name__)

ev_client = None
_app_uuid = None
_api_key = None
request_timeout = 30
_retry = False
_curve = None

BASE_URL_DEFAULT = "https://api.evervault.com/"
RELAY_URL_DEFAULT = "https://relay.evervault.com:443"
CA_HOST_DEFAULT = "https://ca.evervault.com"
CAGES_CA_HOST_DEFAULT = "https://cages-ca.evervault.com"
CAGES_BETA_HOST_DEFAULT = "cages.evervault.com"
CAGES_GA_HOST_DEFAULT = "cage.evervault.com"
MAX_FILE_SIZE_IN_MB_DEFAULT = 25

SUPPORTED_CURVES = ["SECP256K1", "SECP256R1"]


class Curves(object):
    SECP256K1 = "SECP256K1"
    SECP256R1 = "SECP256R1"


def init(
    app_id,
    api_key,
    decryption_domains=[],
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

    if len(decryption_domains) > 0:
        __client().enable_outbound_relay(
            debug_requests, decryption_domains=decryption_domains
        )
    elif enable_outbound_relay:
        __client().enable_outbound_relay(
            debug_requests,
            enable_outbound_relay=enable_outbound_relay,
        )
    else:
        __client()


def run(function_name, data):
    return __client().run(function_name, data)


def decrypt(data):
    return __client().decrypt(data)


def create_client_side_decrypt_token(payload, expiry=None):
    return __client().create_token("api:decrypt", payload, expiry)


def encrypt(data, metadata={}):
    return __client().encrypt(data, metadata)


def cage_requests_session(cage_attestation_data={}):
    warnings.warn(
        "cage_requests_session() is deprecated and will be removed in future versions. Use cage_attestable_session() instead.",
        DeprecationWarning,
    )
    return CageRequestsSessionBeta(
        cage_attestation_data,
        os.environ.get("EV_CAGES_CA_HOST", CAGES_CA_HOST_DEFAULT),
        os.environ.get("EV_CAGES_HOST", CAGES_BETA_HOST_DEFAULT),
    )


def attestable_cage_session(cage_attestation_data={}):
    cage_host = os.environ.get("EV_CAGES_HOST_GA", CAGES_GA_HOST_DEFAULT)
    cache = AttestationDoc(_app_uuid, cage_attestation_data.keys(), cage_host)
    return CageRequestsSession(cage_attestation_data, cage_host, cache)


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
        raise EvervaultError(
            "Your App's App UUID must be entered using evervault.init('<APP-ID>', '<API-KEY>')"
        )
    if not _api_key:
        raise EvervaultError(
            "Your App's API Key must be entered using evervault.init('<APP-ID>', '<API-KEY>')"
        )
    if _curve not in SUPPORTED_CURVES:
        raise EvervaultError(f"The {_curve} curve is not supported.")
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
            relay_url=os.environ.get("EV_TUNNEL_HOSTNAME", RELAY_URL_DEFAULT),
            ca_host=os.environ.get("EV_CERT_HOSTNAME", CA_HOST_DEFAULT),
            retry=_retry,
            curve=_curve,
            max_file_size_in_mb=max_file_size_in_mb,
        )
        return ev_client
    else:
        return ev_client
