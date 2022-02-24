import unittest

from evervault.http.cert import Cert


class TestHandlingCerts(unittest.TestCase):
    def test_cert_is_expired(self):
        abc = "oi"