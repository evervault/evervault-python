from evervault.errors import error_handler


class RequestHandler(object):
    def __init__(self, request, base_url, cert):
        self.cert = cert
        self.base_url = base_url
        self.request = request

    def get(self, path, params={}):
        if self.cert.is_certificate_expired():
            self.cert.setup()
        return self.request.make_request("GET", self.__url(path), params)

    def post(
        self,
        path,
        params,
        optional_headers,
        error_handler=error_handler.raise_error_using_status_code,
    ):
        if self.cert.is_certificate_expired():
            self.cert.setup()
        return self.request.make_request(
            "POST", self.__url(path), params, optional_headers, error_handler
        )

    def put(self, path, params):
        if self.cert.is_certificate_expired():
            self.cert.setup()
        return self.request.make_request("PUT", self.__url(path), params)

    def delete(self, path, params):
        if self.cert.is_certificate_expired():
            self.cert.setup()
        return self.request.make_request("DELETE", self.__url(path), params)

    def __url(self, path):
        return self.base_url + path
