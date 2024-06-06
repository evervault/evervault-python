import requests
import urllib3
import evervault_attestation_bindings
from types import MethodType
from evervault.http.pcrManager import PcrManager
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
    def __init__(self, pcr_manager: PcrManager, cages_host: str, cache):
        self.pcr_manager = pcr_manager
        self.cages_host = cages_host
        self.cache = cache
        super().__init__()

    # Requests >= 2.32.2 recommends the use of get_connection_with_tls_context in place of get_connection.
    def get_connection_with_tls_context(self, request, verify, proxies=None, cert=None):
        conn = super().get_connection_with_tls_context(request, verify, proxies, cert)
        if self.cages_host in request.url:
            cage_name = get_cage_name_from_cage(request.url)
            # we patch the urllib3.connectionpool.HTTPSConnectionPool object to perform extra validation on its connection before transmitting any data
            conn = self.add_attestation_check_to_conn_validation(conn, cage_name)
        return conn

    def add_attestation_check_to_conn_validation(self, conn, cage_name):
        cache = self.cache

        pcrs_from_manager = self.pcr_manager.get(cage_name)
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
    def __init__(self, pcr_manager, cages_host, cache):
        super().__init__()
        self.mount("https://", CageHTTPAdapter(pcr_manager, cages_host, cache))

    def request(self, *args, headers={}, **kwargs):
        return super().request(*args, headers=headers, **kwargs)
