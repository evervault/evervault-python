from ..errors import error_handler
import json
import requests
import certifi
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import base64
import re

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT"],
    backoff_factor=1,
)
adapter = HTTPAdapter(max_retries=retry_strategy)


class Request(object):
    auth_header_regexes = [
        ".*/decrypt.*",
        ".*/client-side-tokens.*",
        ".*/functions/.*/runs.*",
    ]

    def __init__(self, app_uuid, api_key, timeout=30, retry=False):
        self.http_session = requests.Session()
        self.timeout = timeout
        self.app_uuid = app_uuid
        self.api_key = api_key
        self.retry = retry

    def make_request(
        self,
        method,
        url,
        params=None,
        optional_headers={},
        error_handler=error_handler.raise_error_using_status_code,
        _is_ca=False,
    ):
        """
        Make a request.

        Keyword arguments:
        params -- The parameters of the request (default None)
        optional_headers -- Optional headers for the request (default {})
        error_handler -- The error handler to use (default error_handler.raise_error_using_status_code)
        _is_ca -- If the request is for a certificate don't parse the response body (default False)
        """
        from evervault import __version__

        req_params = self.__build_headers(
            method, params, url, optional_headers, __version__
        )

        request_object = requests if self.http_session is None else self.http_session
        if self.retry:
            request_object.mount("https://", adapter)
            request_object.mount("http://", adapter)
        resp = self.__execute_request(request_object, method, url, req_params)
        if _is_ca:
            error_handler(resp, resp.content)
            return resp
        else:
            should_parse = (
                req_params["headers"]
                and req_params["headers"]["Content-Type"] != "application/octet-stream"
            )
            parsed_body = self.__parse_body(resp, should_parse)
            error_handler(resp, parsed_body)
            resp.parsed_body = parsed_body
            return resp

    def __build_headers(self, method, params, url, optional_headers, version):
        req_params = {}

        headers = {
            "User-Agent": "evervault-python/" + version,
            "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Set correct auth header
        if any(re.match(regex, url) for regex in Request.auth_header_regexes):
            auth_value = f"{self.app_uuid}:{self.api_key}"
            encoded_auth_value_bytes = base64.b64encode(auth_value.encode("ascii"))
            basic_auth_str = f"Basic {encoded_auth_value_bytes.decode('utf-8')}"
            headers["Authorization"] = basic_auth_str
        else:
            headers["Api-Key"] = self.api_key

        headers.update(optional_headers)
        if method in ("POST", "PUT", "DELETE"):
            if type(params) == bytes:
                req_params["data"] = params
            else:
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

    def __parse_body(self, resp, should_parse=True):
        if resp.content and resp.content.strip():
            try:
                encoding = resp.encoding or resp.apparent_encoding
                if encoding is None:
                    return resp.content
                decoded_body = resp.content.decode(encoding)
                return json.loads(decoded_body) if should_parse else decoded_body
            except ValueError:
                error_handler(resp, resp.content)
