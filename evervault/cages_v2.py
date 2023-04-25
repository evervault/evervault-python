import requests
import urllib3
import evervault_attestation_bindings
from types import MethodType
from evervault.errors.evervault_errors import CertDownloadError
import tempfile


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
    def __init__(self, cage_attestation_data, cages_host):
        self.attestation_data = cage_attestation_data
        self.cages_host = cages_host
        super().__init__()

    def get_connection(self, url, proxies=None):
        conn = super().get_connection(url, proxies)
        if self.cages_host in url:
            cage_name = get_cage_name_from_cage(url)
            # we patch the urllib3.connectionpool.HTTPSConnectionPool object to perform extra validation on its connection before transmitting any data
            conn = self.add_attestation_check_to_conn_validation(conn, cage_name)
        return conn

    def add_attestation_check_to_conn_validation(self, conn, cage_name):
        expected_pcrs = []
        if cage_name in self.attestation_data:
            given_pcrs = self.attestation_data[cage_name]
            # if the user only supplied a single set of PCRs, convert it to a list
            if not isinstance(given_pcrs, list):
                given_pcrs = [given_pcrs]

            for pcrs in given_pcrs:
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

        def _validate_conn_override(self, conn):
            conn.connect()
            cert = conn.sock.getpeercert(binary_form=True)
            try:
                evervault_attestation_bindings.attest_connection(cert, expected_pcrs)
            except Exception as err:
                raise CageVerificationException(err)
            return original_validate_conn(self, conn)

        conn._validate_conn = MethodType(_validate_conn_override, conn)
        return conn


class CageRequestsSession(requests.Session):
    def __init__(self, cage_attestation_data, cage_ca_host, cages_host):
        super().__init__()
        self.mount("https://", CageHTTPAdapter(cage_attestation_data, cages_host))
        self.ca_host = cage_ca_host

        ca_content = None
        i = 0
        while ca_content is None and i < 2:
            i += 1
            try:
                ca_content = requests.get(self.ca_host).content
            except:  # noqa: E722
                pass

        if ca_content is None:
            raise CertDownloadError(
                f"Unable to install the Evervault Cages CA cert from {self.ca_host}. "
            )

        # todo add expiry
        # self.__set_cert_expire_date(ca_content)

        try:
            with tempfile.NamedTemporaryFile(delete=False) as cert_file:
                cert_file.write(ca_content)
                self.cert_path = cert_file.name
        except:
            raise CertDownloadError(
                f"Unable to install the Evervault Cages CA cert from {self.ca_host}. "
                "Likely a permissions error when attempting to write to the /tmp/ directory."
            )

    def request(self, *args, headers={}, **kwargs):
        return super().request(*args, headers=headers, **kwargs, verify=self.cert_path)
