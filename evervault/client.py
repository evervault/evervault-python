from .http.request import Request
from .crypto.client import Client as CryptoClient
from .models.cage import Cage


class Client(object):
    def __init__(
        self,
        api_key="your_teams_api_key",
        request_timeout=30,
        base_url="https://api.evervault.com/",
        base_run_url="https://cage.run/",
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.base_run_url = base_run_url
        self.request = Request(api_key, request_timeout)
        self.crypto_client = CryptoClient()

    @property
    def _auth(self):
        return (self.api_key, "")

    def encrypt(self, data):
        return self.crypto_client.encrypt_data(self, data)

    def run(self, cage_name, encrypted_data, cage_run=True):
        path = cage_name if cage_run else f"cages/{cage_name}"
        return self.post(path, encrypted_data, cage_run)

    def encrypt_and_run(self, cage_name, data, cage_run=True):
        encrypted_data = self.encrypt(data)
        return self.run(cage_name, encrypted_data, cage_run)

    def cages(self):
        cages = self.get("cages")["cages"]
        return [*map(lambda cage: Cage(cage["name"], cage["uuid"], self), cages)]

    def get(self, path, params={}):
        return self.request.make_request("GET", self.__url(path), params)

    def post(self, path, params, cage_run=False):
        return self.request.make_request("POST", self.__url(path, cage_run), params)

    def put(self, path, params):
        return self.request.make_request("PUT", self.__url(path), params)

    def delete(self, path, params):
        return self.request.make_request("DELETE", self.__url(path), params)

    def __url(self, path, cage_run=False):
        base_url = self.base_run_url if cage_run else self.base_url
        return base_url + path
