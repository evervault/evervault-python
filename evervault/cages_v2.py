import requests
import urllib3
import evervault_attestation_bindings
from types import MethodType
from evervault.http.cagePcrManager import CagePcrManager
import base64


def get_cage_name_from_cage(cage_url):
    requested_cage_hostname = cage_url
    if "https://" in requested_cage_hostname:
        requested_cage_hostname = cage_url[len("https://") :]  # noqa: E203
    requested_cage_hostname_tokens = requested_cage_hostname.split(".")
    if requested_cage_hostname_tokens[1] == "attest":
        return requested_cage_hostname_tokens[2]
    else:
        return requested_cage_hostname_tokens[0]


class CageVerificationException(Exception):
    def __init__(self, err):
        message = f"An error occurred when attesting the connection to your Cage: {err}"
        super().__init__(message)


class CageHTTPAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, cage_pcr_manager: CagePcrManager, cages_host: str, cache):
        self.cage_pcr_manager = cage_pcr_manager
        self.cages_host = cages_host
        self.cache = cache
        super().__init__()

    def get_connection(self, url, proxies=None):
        conn = super().get_connection(url, proxies)
        if self.cages_host in url:
            cage_name = get_cage_name_from_cage(url)
            # we patch the urllib3.connectionpool.HTTPSConnectionPool object to perform extra validation on its connection before transmitting any data
            conn = self.add_attestation_check_to_conn_validation(conn, cage_name)
        return conn

    def add_attestation_check_to_conn_validation(self, conn, cage_name):
        cache = self.cache

        pcrs_from_manager = self.cage_pcr_manager.get(cage_name)
        expected_pcrs = []

        if pcrs_from_manager is not None:
            for pcrs in pcrs_from_manager:
                expected_pcrs.append(
                    evervault_attestation_bindings.PCRs(
                        pcrs.get("pcr_0"),
                        pcrs.get("pcr_1"),
                        pcrs.get("pcr_2"),
                        pcrs.get("pcr_8"),
                    )
                )

        original_validate_conn = (
            urllib3.connectionpool.HTTPSConnectionPool._validate_conn
        )

        def attest_cage(cage_name, cache, cert, expected_pcrs):
            attestation_doc = cache.get(cage_name)
            attestation_doc_bytes = base64.b64decode(attestation_doc)
            evervault_attestation_bindings.attest_cage(
                cert, expected_pcrs, attestation_doc_bytes
            )

        def _validate_conn_override(self, conn):
            conn.connect()
            cert = conn.sock.getpeercert(binary_form=True)
            try:
                attest_cage(cage_name, cache, cert, expected_pcrs)
            except Exception:
                try:
                    cache.load_doc(cage_name)
                    attest_cage(cage_name, cache, cert, expected_pcrs)
                except Exception as err:
                    raise CageVerificationException(err)
            return original_validate_conn(self, conn)

        conn._validate_conn = MethodType(_validate_conn_override, conn)
        return conn


class CageRequestsSession(requests.Session):
    def __init__(self, cage_pcr_manager, cages_host, cache):
        super().__init__()
        self.mount("https://", CageHTTPAdapter(cage_pcr_manager, cages_host, cache))

    def request(self, *args, headers={}, **kwargs):
        return super().request(*args, headers=headers, **kwargs)
