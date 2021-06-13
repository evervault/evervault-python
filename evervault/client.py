from .http.request import Request
from .crypto.client import Client as CryptoClient
from .models.cage_list import CageList
from .datatypes.map import ensure_is_integer
import requests
import pkg_resources

class Client(object):
    def __init__(
        self,
        api_key=None,
        request_timeout=30,
        base_url="https://api.evervault.com/",
        base_run_url="https://cage.run/",
        outbound_relay_url="https://relay.evervault.com:443",
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.base_run_url = base_run_url
        self.outbound_relay_url = outbound_relay_url
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

    def outbound_relay(client_self):
        old_request_func = requests.Session.request
        cert_path = pkg_resources.resource_filename(__name__, 'certs/rootCA.crt')
        api_key = client_self.api_key
        outbound_relay_url = client_self.outbound_relay_url
        def new_req_func(self, method, url,
                params=None, data=None, headers={}, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies={},
                hooks=None, stream=None, verify=None, cert=None, json=None):
            headers["Proxy-Authorization"] = api_key
            proxies["https"] = outbound_relay_url
            verify = cert_path
            return old_request_func(self, method, url,
                params, data, headers, cookies, files,
                auth, timeout, allow_redirects, proxies,
                hooks, stream, verify, cert, json)
        requests.Session.request = new_req_func

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
        if 'async' in options:
            if options['async']:
                cage_run_headers['x-async'] = 'true'
            options.pop('async', None)
        if 'version' in options:
            if ensure_is_integer(options['version']):
                cage_run_headers['x-version-id'] = str(int(float(options['version'])))
            options.pop('version', None)
        cage_run_headers.update(options)
        return cage_run_headers