from .http.request import Request
from .crypto.client import Client as CryptoClient
from .errors.evervault_errors import CertDownloadError
from urllib.parse import urlparse
import requests
import certifi
import warnings
import tempfile

class RelayClient(object):
    def __init__(
        self,
        api_key=None,
        request_timeout=30,
        relay_url="https://relay.evervault.com:443",
        ca_host="https://ca.evervault.com",
    ):
        self.api_key = api_key
        self.relay_url = relay_url
        self.ca_host = ca_host
        self.request = Request(self.api_key, request_timeout)
        self.crypto_client = CryptoClient(api_key)


    def relay(client_self, ignore_domains=[]):
        ignore_if_exact = []
        ignore_if_endswith = ()
        for domain in ignore_domains:
            if domain.startswith("www."):
                domain = domain[4:]
            ignore_if_exact.append(domain)
            ignore_if_endswith += ("." + domain, "@" + domain)
        old_request_func = requests.Session.request

        ca_content = None
        i = 0

        while ca_content is None and i < 2:
            i += 1
            try:
                ca_content = requests.get(client_self.ca_host).content
            except:  # noqa: E722
                pass

        if ca_content is None:
            raise CertDownloadError(
                f"Unable to install the Evervault root certificate from {client_self.ca_host}. "
            )

        try:
            with tempfile.NamedTemporaryFile(delete=False) as cert_file:
                cert_file.write(bytes(certifi.contents(), "ascii") + ca_content)
                cert_path = cert_file.name
        except:  # noqa: 722
            raise CertDownloadError(
                f"Unable to install the Evervault root certficate from {client_self.ca_host}. "
                "Likely a permissions error when attempting to write to the /tmp/ directory."
            )
        api_key = client_self.api_key
        relay_url = client_self.relay_url

        # We override this method to stop the requests library from
        # removing the API token from the Proxy-Authorization header
        def rebuild_proxies(self, prepared_request, proxies):
            pass

        requests.sessions.SessionRedirectMixin.rebuild_proxies = rebuild_proxies

        def new_req_func(
            self,
            method,
            url,
            params=None,
            data=None,
            headers={},
            cookies=None,
            files=None,
            auth=None,
            timeout=None,
            allow_redirects=True,
            proxies={},
            hooks=None,
            stream=None,
            verify=None,
            cert=None,
            json=None,
        ):
            if headers is None:
                headers = {}
            if proxies is None:
                proxies = {}
            headers["Proxy-Authorization"] = api_key
            proxies["https"] = relay_url
            verify = cert_path
            try:
                domain = urlparse(url).netloc
                if domain in ignore_if_exact or domain.endswith(ignore_if_endswith):
                    del headers["Proxy-Authorization"]
                    del proxies["https"]
            except Exception:
                warnings.warn(
                    f"Unable to parse {url} when attempting to check "
                    "if it is an ignore_domain."
                )
                pass
            return old_request_func(
                self,
                method,
                url,
                params,
                data,
                headers,
                cookies,
                files,
                auth,
                timeout,
                allow_redirects,
                proxies,
                hooks,
                stream,
                verify,
                cert,
                json,
            )

        requests.Session.request = new_req_func