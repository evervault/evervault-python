from datetime import datetime
from .http.requestintercept import RequestIntercept
from .http.requesthandler import RequestHandler
from .http.request import Request
from .crypto.client import Client as CryptoClient
from .models.cage_list import CageList
from .datatypes.map import ensure_is_integer
from .services.timeservice import TimeService
from .errors.evervault_errors import UndefinedDataError, DecryptionError


class Client(object):
    def __init__(
        self,
        app_uuid=None,
        api_key=None,
        request_timeout=30,
        base_url="https://api.evervault.com/",
        base_run_url="https://run.evervault.com/",
        relay_url="https://relay.evervault.com:443",
        ca_host="https://ca.evervault.com",
        retry=False,
        curve="SECP256K1",
        max_file_size_in_mb=25,
    ):
        self.app_uuid = app_uuid
        self.api_key = api_key
        self.base_url = base_url
        self.base_run_url = base_run_url
        self.relay_url = relay_url
        self.ca_host = ca_host
        request = Request(self.app_uuid, self.api_key, request_timeout, retry)
        time_service = TimeService()
        self.cert = RequestIntercept(
            request, ca_host, base_run_url, base_url, api_key, relay_url, time_service
        )
        self.request_handler = RequestHandler(
            request, base_run_url, base_url, self.cert
        )
        self.crypto_client = CryptoClient(api_key, curve, max_file_size_in_mb)

    @property
    def _auth(self):
        return (self.api_key, "")

    def encrypt(self, data):
        return self.crypto_client.encrypt_data(self, data)

    def decrypt(self, data):
        if data is None:
            raise UndefinedDataError("Data is not defined")
        elif not isinstance(data, (str, dict, list, bytes)):
            raise DecryptionError(
                "data must be of type `str`, `dict`, `list` or `bytes`"
            )
        headers = self.__build_decrypt_headers(type(data))

        if type(data) == bytes:
            return self.post("decrypt", data, headers, False)
        else:
            payload = {"data": data}
            response = self.post("decrypt", payload, headers, False)
            return response["data"]

    def create_token(self, action, payload, expiry=None):
        if payload is None:
            raise UndefinedDataError(
                "Payload must be defined. It ensures that the generated token will only be able to be used to decrypt this specific payload"
            )
        if expiry and not isinstance(expiry, datetime):
            raise UndefinedDataError("expiry must be an instance of `datetime`")
        if expiry and isinstance(expiry, datetime):
            expiry = int(expiry.timestamp() * 1000)
        data = {
            "payload": payload,
            "expiry": expiry,
            "action": action,
        }
        headers = {
            "Content-Type": "application/json",
        }
        return self.post("client-side-tokens", data, headers, False)

    def run(self, cage_name, data, options={"async": False, "version": None}):
        optional_headers = self.__build_cage_run_headers(options)
        return self.post(cage_name, data, optional_headers, True)

    def encrypt_and_run(
        self, cage_name, data, options={"async": False, "version": None}
    ):
        encrypted_data = self.encrypt(data)
        return self.run(cage_name, encrypted_data, options)

    def cages(self):
        cages = self.get("cages")["cages"]
        return CageList(cages, self).cages

    def enable_outbound_relay(
        self,
        debug_requests,
        ignore_domains=[],
        decryption_domains=[],
        enable_outbound_relay=False,
        client_session=None,
    ):
        if len(decryption_domains) > 0:
            self.cert.setup_decryption_domains(decryption_domains, debug_requests)
        elif enable_outbound_relay:
            self.cert.set_relay_outbound_config(debug_requests)
        else:
            self.cert.setup_ignore_domains(ignore_domains, debug_requests)
        self.cert.setup()
        if client_session:
            self.cert.setup_aiohttp(client_session)

    def create_run_token(self, cage_name, data):
        return self.post(f"v2/functions/{cage_name}/run-token", data, {})

    def get(self, path, params={}):
        return self.request_handler.get(path, params).parsed_body

    def post(self, path, params, optional_headers, cage_run=False):
        return self.request_handler.post(
            path, params, optional_headers, cage_run
        ).parsed_body

    def put(self, path, params):
        return self.request_handler.put(path, params).parsed_body

    def delete(self, path, params):
        return self.request_handler.delete(path, params).parsed_body

    def __build_decrypt_headers(self, data_type):
        headers = {}
        headers["Content-Type"] = "application/json"
        if data_type == bytes:
            headers["Content-Type"] = "application/octet-stream"
        return headers

    def __build_cage_run_headers(self, options):
        if options is None:
            return {}
        cage_run_headers = {}
        if "async" in options:
            if options["async"]:
                cage_run_headers["x-async"] = "true"
            options.pop("async", None)
        if "version" in options:
            if ensure_is_integer(options["version"]):
                cage_run_headers["x-version-id"] = str(int(float(options["version"])))
            options.pop("version", None)
        cage_run_headers.update(options)
        return cage_run_headers
