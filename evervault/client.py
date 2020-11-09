from .http.request import Request
from .crypto.client import Client as CryptoClient
from .models.cage_list import CageList
from .datatypes.map import ensure_is_integer

class Client(object):
    def __init__(
        self,
        api_key=None,
        request_timeout=30,
        base_url="https://api.evervault.com/",
        base_run_url="https://cage.run/",
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.base_run_url = base_run_url
        self.request = Request(self.api_key, request_timeout)
        self.crypto_client = CryptoClient()

    @property
    def _auth(self):
        return (self.api_key, "")

    def encrypt(self, data):
        return self.crypto_client.encrypt_data(self, data)

    def run(self, cage_name, encrypted_data, options = { "async": False, "version": None }):
        optional_headers = self.__build_cage_run_headers(options)
        return self.post(cage_name, encrypted_data, optional_headers, True)

    def encrypt_and_run(self, cage_name, data, options = { "async": False, "version": None }):
        encrypted_data = self.encrypt(data)
        return self.run(cage_name, encrypted_data, options)

    def cages(self):
        cages = self.get("cages")["cages"]
        return CageList(cages, self).cages

    def get(self, path, params={}):
        return self.request.make_request("GET", self.__url(path), params)

    def post(self, path, params, optional_headers, cage_run=False):
        return self.request.make_request("POST", self.__url(path, cage_run), params, optional_headers)

    def put(self, path, params):
        return self.request.make_request("PUT", self.__url(path), params)

    def delete(self, path, params):
        return self.request.make_request("DELETE", self.__url(path), params)

    def __url(self, path, cage_run=False):
        base_url = self.base_run_url if cage_run else self.base_url
        return base_url + path

    def __build_cage_run_headers(self, options):
        if options is None:
            return {}
        cage_run_headers = {}
        if 'async' in options and options['async']:
            cage_run_headers['x-async'] = 'true'
        if 'version' in options and ensure_is_integer(options['version']):
            cage_run_headers['x-version-id'] = str(int(float(options['version'])))
        return cage_run_headers