class RequestHandler(object):
    def __init__(self, request, base_run_url, base_url, cert):
        self.cert = cert
        self.base_url = base_url
        self.base_run_url = base_run_url
        self.request = request

    def setup_relay(self, ignore_domains=[]):
        self.cert.setup(ignore_domains)

    def get(self, path, params={}):
        if self.cert.is_certificate_expired():
            self.cert.update_certificate()
        return self.request.make_request("GET", self.__url(path), params)

    def post(self, path, params, optional_headers, cage_run=False):
        return self.request.make_request(
            "POST", self.__url(path, cage_run), params, optional_headers
        )

    def put(self, path, params):
        return self.request.make_request("PUT", self.__url(path), params)

    def delete(self, path, params):
        return self.request.make_request("DELETE", self.__url(path), params)

    def __url(self, path, cage_run=False):
        base_url = self.base_run_url if cage_run else self.base_url
        return base_url + path
