import unittest
from unittest.mock import patch

from evervault.http.requesthandler import RequestHandler


class TestHandlingRequests(unittest.TestCase):
    @patch('evervault.http.requestintercept.RequestIntercept')
    @patch('evervault.http.requesthandler.RequestHandler')
    def test_expired_cert_is_updated_for_gets(self, cert, request):
        request_handler = RequestHandler(request, "https://someaddress.io", "https://anotheraddress.io", cert)
        cert.is_certificate_expired.return_value = True
        request_handler.get("https://anyaddress.io")
        cert.setup.assert_called()

    @patch('evervault.http.requestintercept.RequestIntercept')
    @patch('evervault.http.requesthandler.RequestHandler')
    def test_expired_cert_is_updated_for_post(self, cert, request):
        request_handler = RequestHandler(request, "https://someaddress.io", "https://anotheraddress.io", cert)
        cert.is_certificate_expired.return_value = True
        request_handler.post("https://run.anyaddress.com/testing-cage",
                             {"status": "queued"},
                             {
                                 "Api-Key": "testing",
                                 "x-version-id": "2",
                                 "x-async": "true",
                             })
        cert.setup.assert_called()

    @patch('evervault.http.requestintercept.RequestIntercept')
    @patch('evervault.http.requesthandler.RequestHandler')
    def test_expired_cert_is_updated_for_put(self, cert, request):
        request_handler = RequestHandler(request, "https://someaddress.io", "https://anotheraddress.io", cert)
        cert.is_certificate_expired.return_value = True
        request_handler.put("https://anyaddress.io", {"status": "queued"})
        cert.setup.assert_called()

    @patch('evervault.http.requestintercept.RequestIntercept')
    @patch('evervault.http.requesthandler.RequestHandler')
    def test_expired_cert_is_updated_for_delete(self, cert, request):
        request_handler = RequestHandler(request, "https://someaddress.io", "https://anotheraddress.io", cert)
        cert.is_certificate_expired.return_value = True
        request_handler.delete("https://anyaddress.io", {"status": "queued"})
        cert.setup.assert_called()
