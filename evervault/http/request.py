from ..errors import error_handler
import json
import requests
import certifi
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT"],
    backoff_factor=1,
)
adapter = HTTPAdapter(max_retries=retry_strategy)


class Request(object):
    def __init__(self, api_key, timeout=30, retry=False):
        self.http_session = requests.Session()
        self.timeout = timeout
        self.api_key = api_key
        self.retry = retry

    def make_request(self, method, url, params=None, optional_headers={}, _is_ca=False):
        """
        Make a request.

        Keyword arguments:
        params -- The parameters of the request (default None)
        optional_headers -- Optional headers for the request (default {})
        _is_ca -- If the request is for a certificate don't parse the response body (default False)
        """
        from evervault import __version__

        req_params = self.__build_headers(method, params, optional_headers, __version__)

        request_object = requests if self.http_session is None else self.http_session
        if self.retry:
            request_object.mount("https://", adapter)
            request_object.mount("http://", adapter)
        resp = self.__execute_request(request_object, method, url, req_params)
        if _is_ca:
            error_handler.raise_errors_on_failure(resp, resp.content)
            return resp
        else:
            parsed_body = self.__parse_body(resp)
            error_handler.raise_errors_on_failure(resp, parsed_body)
            resp.parsed_body = parsed_body
            return resp

    def __build_headers(self, method, params, optional_headers, version):
        req_params = {}
        headers = {
            "User-Agent": "evervault-python/" + version,
            "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }
        headers.update(optional_headers)
        if method in ("POST", "PUT", "DELETE"):
            req_params["data"] = json.dumps(params, cls=json.JSONEncoder)
        elif method == "GET":
            req_params["params"] = params

        req_params["headers"] = headers
        return req_params

    def __execute_request(self, request_object, method, url, req_params):
        return request_object.request(
            method,
            url,
            timeout=self.timeout,
            verify=certifi.where(),
            allow_redirects=False,
            **req_params,
        )

    def __parse_body(self, resp):
        if resp.content and resp.content.strip():
            try:
                decoded_body = resp.content.decode(
                    resp.encoding or resp.apparent_encoding
                )
                return json.loads(decoded_body)
            except ValueError:
                error_handler.raise_errors_on_failure(resp)
