import unittest
from unittest.mock import patch

from evervault.http.requesthandler import RequestHandler


class TestHandlingRequests(unittest.TestCase):
    @patch('evervault.http.cert.Cert')
    @patch('evervault.http.requesthandler.RequestHandler')
    def test_expired_cert_is_updated(self, cert, request):
        request_handler = RequestHandler(request, "https://someaddress.io", "https://anotheraddress.io", cert)
        cert.is_certificate_expired.return_value = True
        request_handler.get("https://anyaddress.io")
        cert.update_certificate.assert_called()
