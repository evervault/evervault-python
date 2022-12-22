from datetime import datetime
from urllib.parse import urlparse
from cryptography import x509
import requests
import warnings
import certifi
import tempfile
import ssl
from evervault.errors.evervault_errors import CertDownloadError
from evervault.http.outboundrelayconfig import RelayOutboundConfig

EVERVAULT_DOMAINS = ["evervault.com", "evervault.io", "evervault.test"]

old_request_func = requests.Session.request


def is_ignore_domain(domain, decryption_domains, always_ignore_domains):
    if domain in always_ignore_domains:
        return False
    return any(
        domain == decryption_domain
        or (decryption_domain[0] == "*" and domain.endswith(decryption_domain[1:]))
        for decryption_domain in decryption_domains
    )


def hostname_from_str_or_url(str_or_url):
    if hasattr(str_or_url, "host"):
        return str_or_url.host

    return urlparse(str_or_url).netloc


class RequestIntercept(object):
    def __init__(
        self,
        request,
        ca_host,
        base_run_url,
        base_url,
        api_key,
        relay_url,
        datetime_service,
    ):
        self.datetime_service = datetime_service
        self.relay_url = relay_url
        self.api_key = api_key
        self.base_url = base_url
        self.base_run_url = base_run_url
        self.request = request
        self.ca_host = ca_host
        self.expire_date = None
        self.initial_date = None
        self.cert_path = None
        self.should_proxy_domain = lambda host: False
        self.debug_requests = False
        self.relay_outbound_config = None

    def is_certificate_expired(self):
        if self.expire_date is not None:
            now = self.datetime_service.get_datetime_now()
            if now > self.expire_date or now < self.initial_date:
                return True
        return False

    def get_always_ignore_domains(self):
        return [
            urlparse(self.base_run_url).netloc,
            urlparse(self.base_url).netloc,
            urlparse(self.ca_host).netloc,
        ]

    def setup_decryption_domains(self, decryption_domains, debug_requests=False):
        self.debug_requests = debug_requests
        always_ignore_domains = self.get_always_ignore_domains()
        self.should_proxy_domain = lambda host: is_ignore_domain(
            host, decryption_domains, always_ignore_domains
        )

    def setup_ignore_domains(self, ignore_domains, debug_requests=False):
        self.debug_requests = debug_requests
        ignore_domains.extend(self.get_always_ignore_domains())

        ignore_if_exact = []
        ignore_if_endswith = ()
        for domain in ignore_domains:
            if domain.startswith("www."):
                domain = domain[4:]
            ignore_if_exact.append(domain)
            ignore_if_endswith += ("." + domain, "@" + domain)

        self.should_proxy_domain = lambda host: not (
            host in ignore_if_exact or host.endswith(ignore_if_endswith)
        )

    def set_relay_outbound_config(self, debug_requests=False):
        self.debug_requests = debug_requests
        RelayOutboundConfig.init(self.request, self.base_url, self.debug_requests)
        always_ignore_domains = self.get_always_ignore_domains()
        self.should_proxy_domain = lambda host: is_ignore_domain(
            host, RelayOutboundConfig.get_decryption_domains(), always_ignore_domains
        )

    def setup_aiohttp(self, client_session):
        self.__get_cert()
        default_ssl_context = ssl.create_default_context(cafile=certifi.where())
        evervault_ssl_context = ssl.create_default_context(cafile=self.cert_path)
        api_key = self.api_key
        relay_url = self.relay_url

        old_request = client_session._request

        def new_req_func(method, str_or_url, **kwargs):
            domain = hostname_from_str_or_url(str_or_url)
            should_proxy = self.should_proxy_domain(domain)

            if "headers" not in kwargs:
                kwargs["headers"] = {}

            if self.debug_requests and not any(
                map(
                    lambda evervault_domain: domain.endswith(evervault_domain),
                    EVERVAULT_DOMAINS,
                )
            ):
                print(
                    f"Request to domain: {domain}, Outbound Proxy enabled: {should_proxy}"
                )
            if should_proxy:
                kwargs["proxy"] = relay_url
                kwargs["headers"]["Proxy-Authorization"] = api_key
                kwargs["ssl"] = evervault_ssl_context
            else:
                kwargs["ssl"] = default_ssl_context

            return old_request(method, str_or_url, **kwargs)

        client_session._request = new_req_func

    def setup(client_self):
        client_self.__get_cert()

        cert_path = client_self.cert_path
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
            proxies = {}

            try:
                domain = urlparse(url).netloc
                should_proxy = client_self.should_proxy_domain(domain)
                if client_self.debug_requests and not any(
                    map(
                        lambda evervault_domain: domain.endswith(evervault_domain),
                        EVERVAULT_DOMAINS,
                    )
                ):
                    print(
                        f"Request to domain: {domain}, Outbound Proxy enabled: {should_proxy}"
                    )
                if should_proxy:
                    headers["Proxy-Authorization"] = api_key
                    proxies["https"] = relay_url
                    verify = cert_path
            except Exception as e:
                warnings.warn(
                    f"EVERVAULT :: Unable to parse {url} when attempting to check if it should be proxied. {e}"
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

    def __get_cert(self):
        ca_content = None
        i = 0

        while ca_content is None and i < 2:
            i += 1
            try:
                ca_content = self.request.make_request(
                    "GET", self.ca_host, {}, _is_ca=True
                ).content
            except:  # noqa: E722
                pass

        if ca_content is None:
            raise CertDownloadError(
                f"Unable to install the Evervault root certificate from {self.ca_host}. "
            )

        self.__set_cert_expire_date(ca_content)

        try:
            with tempfile.NamedTemporaryFile(delete=False) as cert_file:
                cert_file.write(bytes(certifi.contents(), "ascii") + ca_content)
                self.cert_path = cert_file.name
        except:
            raise CertDownloadError(
                f"Unable to install the Evervault root certficate from {self.ca_host}. "
                "Likely a permissions error when attempting to write to the /tmp/ directory."
            )

    def __set_cert_expire_date(self, ca_content):
        try:
            cert_info = x509.load_pem_x509_certificate(ca_content)

            self.expire_date = datetime.timestamp(cert_info.not_valid_after)
            self.initial_date = datetime.timestamp(cert_info.not_valid_before)
        except:
            self.expire_date = None
