import os
import requests
from requests.adapters import HTTPAdapter
import http.client as http_client
from urllib3 import ProxyManager
from urllib3.util.ssl_ import create_urllib3_context

http_client.HTTPConnection.debuglevel = 1

class RelayHTTPSAdapter(HTTPAdapter):
    def __init__(self, proxy_auth, ca_cert_path, *args, **kwargs):
        # TODO this should support testing
        self.proxy_url = 'https://relay.evervault.com'
        self.proxy_auth = proxy_auth
        self.ca_cert_path = ca_cert_path
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.load_verify_locations(cafile=self.ca_cert_path)

        # Usually make_headers from urllib3 would be used but thats added Basic auth which
        # Relay does not support. So we need to manually add the Proxy-Authorization header.
        proxy_headers = {
            'Proxy-Authorization': self.proxy_auth
        }

        self.poolmanager = ProxyManager(
            proxy_url=self.proxy_url,
            proxy_headers=proxy_headers,
            num_pools=self._pool_connections,
            maxsize=self._pool_maxsize,
            block=self._pool_block,
            ssl_context=context,
        )

    def proxy_headers(self, proxy):
        headers = super().proxy_headers(proxy)
        headers['Proxy-Authorization'] = self.proxy_auth
        return headers

class RelayRequestsSession(requests.Session):
    def __init__(self, proxy_url, proxy_auth, ca_cert_path):
        super().__init__()
        self.mount("https://", RelayHTTPSAdapter(proxy_url=proxy_url, proxy_auth=proxy_auth, ca_cert_path=ca_cert_path))

    def request(self, *args, headers={}, **kwargs):
        return super().request(*args, headers=headers, **kwargs)

def main():
    proxy_url = 'https://relay.evervault.com'
    proxy_auth = 'KEY'
    ca_cert_path = os.path.join(os.path.dirname(__file__), 'evervault_ca.pem')

    session = requests.Session()
    adapter = RelayHTTPSAdapter(proxy_url=proxy_url, proxy_auth=proxy_auth, ca_cert_path=ca_cert_path)
    session.mount('https://', adapter)

    response = session.get('https://putsreq.com/wOgDjXar9a7gmpdM0Ulg')
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    main()
