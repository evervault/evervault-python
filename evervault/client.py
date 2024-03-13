from datetime import datetime

from evervault.errors.error_handler import (
    raise_error_using_status_code,
    raise_errors_on_function_run_failure,
    raise_errors_on_api_error,
)
from .http.requestintercept import RequestIntercept
from .http.requesthandler import RequestHandler
from .http.request import Request
from .crypto.client import Client as CryptoClient
from .services.timeservice import TimeService
from .errors.evervault_errors import EvervaultError


class Client(object):
    def __init__(
        self,
        app_uuid=None,
        api_key=None,
        request_timeout=30,
        base_url="https://api.evervault.com/",
        relay_url="https://relay.evervault.com:443",
        ca_host="https://ca.evervault.com",
        retry=False,
        curve="SECP256K1",
        max_file_size_in_mb=25,
    ):
        self.app_uuid = app_uuid
        self.api_key = api_key
        self.base_url = base_url
        self.relay_url = relay_url
        self.ca_host = ca_host
        request = Request(self.app_uuid, self.api_key, request_timeout, retry)
        time_service = TimeService()
        self.cert = RequestIntercept(
            request, ca_host, base_url, api_key, relay_url, time_service
        )
        self.request_handler = RequestHandler(request, base_url, self.cert)
        self.crypto_client = CryptoClient(api_key, curve, max_file_size_in_mb)

    @property
    def _auth(self):
        return (self.api_key, "")

    def encrypt(self, data, role):
        return self.crypto_client.encrypt_data(self, data, role)

    def decrypt(self, data):
        if data is None:
            raise EvervaultError("Data is not defined")
        elif not isinstance(data, (str, dict, list, bytes)):
            raise EvervaultError(
                "data must be of type `str`, `dict`, `list` or `bytes`"
            )
        headers = self.__build_decrypt_headers(type(data))

        if type(data) == bytes:
            return self.post("decrypt", data, headers, raise_errors_on_api_error)
        else:
            payload = {"data": data}
            response = self.post(
                "decrypt",
                payload,
                headers,
                raise_errors_on_api_error,
            )
            return response["data"]

    def create_token(self, action, payload, expiry=None):
        if payload is None:
            raise EvervaultError(
                "Payload must be defined. It ensures that the generated token will only be able to be used to decrypt this specific payload"
            )
        if expiry and not isinstance(expiry, datetime):
            raise EvervaultError("expiry must be an instance of `datetime`")
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
        return self.post(
            "client-side-tokens",
            data,
            headers,
            error_handler=raise_errors_on_api_error,
        )

    def run(self, function_name, data, run_async):
        response = self.post(
            f"functions/{function_name}/runs",
            {"payload": data, "async": run_async},
            error_handler=raise_errors_on_api_error,
        )

        if response.get("status") == "success" or response.get("status") == "scheduled":
            return response
        raise_errors_on_function_run_failure(response)

    def enable_outbound_relay(
        self,
        debug_requests,
        decryption_domains=[],
        enable_outbound_relay=False,
        client_session=None,
    ):
        if len(decryption_domains) > 0:
            self.cert.setup_decryption_domains(decryption_domains, debug_requests)
        elif enable_outbound_relay:
            self.cert.set_relay_outbound_config(debug_requests)
        self.cert.setup()
        if client_session:
            self.cert.setup_aiohttp(client_session)

    def create_run_token(self, function_name, data):
        return self.post(f"v2/functions/{function_name}/run-token", data, {})

    def get(self, path, params={}):
        return self.request_handler.get(path, params).parsed_body

    def post(
        self,
        path,
        params,
        optional_headers={},
        error_handler=raise_error_using_status_code,
    ):
        return self.request_handler.post(
            path, params, optional_headers, error_handler
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
