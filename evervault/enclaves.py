import requests
import urllib3
import evervault_attestation_bindings
from types import MethodType
from evervault.http.pcrManager import PcrManager
import base64


def get_enclave_name_from_enclave_url(enclave_url):
    requested_enclave_hostname = enclave_url
    if "https://" in requested_enclave_hostname:
        requested_enclave_hostname = enclave_url[len("https://") :]  # noqa: E203
    requested_enclave_hostname_tokens = requested_enclave_hostname.split(".")
    return requested_enclave_hostname_tokens[0]


class EnclaveVerificationException(Exception):
    def __init__(self, err):
        message = (
            f"An error occurred when attesting the connection to your Enclave: {err}"
        )
        super().__init__(message)


class EnclaveHTTPAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, pcr_manager: PcrManager, enclave_host: str, cache):
        self.pcr_manager = pcr_manager
        self.enclave_host = enclave_host
        self.cache = cache
        super().__init__()

    def get_connection(self, url, proxies=None):
        conn = super().get_connection(url, proxies)
        if self.enclave_host in url:
            enclave_name = get_enclave_name_from_enclave_url(url)
            # we patch the urllib3.connectionpool.HTTPSConnectionPool object to perform extra validation on its connection before transmitting any data
            conn = self.add_attestation_check_to_conn_validation(conn, enclave_name)
        return conn

    def add_attestation_check_to_conn_validation(self, conn, enclave_name):
        cache = self.cache

        pcrs_from_manager = self.pcr_manager.get(enclave_name)
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

        def attest_enclave(enclave_name, cache, cert, expected_pcrs):
            attestation_doc = cache.get(enclave_name)
            attestation_doc_bytes = base64.b64decode(attestation_doc)
            evervault_attestation_bindings.attest_cage(
                cert, expected_pcrs, attestation_doc_bytes
            )

        def _validate_conn_override(self, conn):
            conn.connect()
            cert = conn.sock.getpeercert(binary_form=True)
            try:
                attest_enclave(enclave_name, cache, cert, expected_pcrs)
            except Exception:
                try:
                    cache.load_doc(enclave_name)
                    attest_enclave(enclave_name, cache, cert, expected_pcrs)
                except Exception as err:
                    raise EnclaveVerificationException(err)
            return original_validate_conn(self, conn)

        conn._validate_conn = MethodType(_validate_conn_override, conn)
        return conn


class EnclaveRequestsSession(requests.Session):
    def __init__(self, pcr_manager, enclave_host, cache):
        super().__init__()
        self.mount("https://", EnclaveHTTPAdapter(pcr_manager, enclave_host, cache))

    def request(self, *args, headers={}, **kwargs):
        return super().request(*args, headers=headers, **kwargs)
