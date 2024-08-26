import certifi
import requests
from requests.adapters import HTTPAdapter
from urllib3 import ProxyManager, make_headers
from urllib3.util.ssl_ import create_urllib3_context
import tempfile
import ssl
import asyncio
import aiohttp
from requests.auth import HTTPBasicAuth

class RelayHTTPSAdapter(HTTPAdapter):
    def __init__(self, proxy_url, proxy_auth, ca_cert_url, *args, **kwargs):
        self.proxy_url = proxy_url
        self.proxy_auth = proxy_auth
        self.ca_cert_url = ca_cert_url
        self.ca_file_path = get_cert_file(ca_cert_url=self.ca_cert_url)
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.load_verify_locations(cafile=self.ca_file_path)

        self.poolmanager = ProxyManager(
            proxy_url=self.proxy_url,
            proxy_headers=make_headers(proxy_basic_auth=self.proxy_auth),
            num_pools=self._pool_connections,
            maxsize=self._pool_maxsize,
            block=self._pool_block,
            ssl_context=context,
        )

    def proxy_headers(self, proxy):
        headers = super().proxy_headers(proxy)
        headers["Proxy-Authorization"] = self.proxy_auth
        return headers

class RelayInboundAdapter(requests.Session):
    def __init__(self,app_uuid,  api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        self.app_uuid = app_uuid
        self.relay_domains = self._get_relay_domains()

    def _get_relay_domains(self):
        basic = HTTPBasicAuth(self.app_uuid, self.api_key)
        response = requests.get(
            "https://api.evervault.com/relays",
            auth=(basic),
            headers={
                "Content-Type": "application/json",
            }
        )
        return response.json()

class RelayAsyncioSSLContext:
    def __init__(self, ca_cert_url):
        self.ca_file_path = get_cert_file(ca_cert_url=ca_cert_url)

    def asyncio_context(self):
        """
        asyncio runtime currently doesnt support CONNECT over TLS without this
        workaround https://github.com/aio-libs/aiohttp/discussions/6044
        """
        setattr(asyncio.sslproto._SSLProtocolTransport, "_start_tls_compatible", True)

        evervault_ssl_context = ssl.create_default_context(cafile=self.ca_file_path)
        return aiohttp.TCPConnector(ssl_context=evervault_ssl_context)


def get_cert_file(ca_cert_url):
    ca_content = download_ca_cert(ca_cert_url=ca_cert_url)

    try:
        with tempfile.NamedTemporaryFile(delete=False) as cert_file:
            cert_file.write(bytes(certifi.contents(), "ascii") + ca_content)
            return cert_file.name
    except Exception as e:
        raise e


def download_ca_cert(ca_cert_url):
    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(ca_cert_url, timeout=10)
            print(response)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            if attempt == max_attempts:
                raise RuntimeError(
                    f"Unable to download the CA certificate from {ca_cert_url} after {max_attempts} attempts. {e}"
                )
