class RequestHandler(object):
    def __init__(self, request, base_run_url, base_url, request_intercept):
        self.request_intercept = request_intercept
        self.base_url = base_url
        self.base_run_url = base_run_url
        self.request = request
        self.requires_certificate = False

    def setup_certificate(self, ignore_domains=[]):
        self.requires_certificate = True
        self.request_intercept.setup_domains(ignore_domains)
        self.request_intercept.setup()

    def get(self, path, params={}):
        self.__validate_cert_if_needed()
        return self.request.make_request("GET", self.__url(path), params)

    def post(self, path, params, optional_headers, cage_run=False):
        self.__validate_cert_if_needed()
        return self.request.make_request(
            "POST", self.__url(path, cage_run), params, optional_headers
        )

    def put(self, path, params):
        self.__validate_cert_if_needed()
        return self.request.make_request("PUT", self.__url(path), params)

    def delete(self, path, params):
        self.__validate_cert_if_needed()
        return self.request.make_request("DELETE", self.__url(path), params)

    def __validate_cert_if_needed(self):
        if self.requires_certificate:
            if self.request_intercept.is_certificate_expired():
                self.request_intercept.setup()
            if self.request_intercept.certificate_not_available():
                raise Exception("Certificate not available")

    def __url(self, path, cage_run=False):
        base_url = self.base_run_url if cage_run else self.base_url
        return base_url + path
