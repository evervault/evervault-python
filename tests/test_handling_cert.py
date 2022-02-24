import unittest

import requests_mock

from evervault.http.cert import Cert
from evervault.http.request import Request

class TestHandlingCerts(unittest.TestCase):
    @requests_mock.Mocker()
    def test_cert_is_expired(self, mock_request):
        mock_request.get(
            "https://ca.evervault.com",
            text="-----BEGIN CERTIFICATE-----\n"
                 "MIIDrDCCApQCCQDr4C3xZruyADANBgkqhkiG9w0BAQsFADCBlzELMAkGA1UEBhMC\n"
                 "SVIxEzARBgNVBAgMCkR1YmxpbiBDby4xDzANBgNVBAcMBkR1YmxpbjESMBAGA1UE\n"
                 "CgwJRXZlcnZhdWx0MRIwEAYDVQQLDAlFdmVydmF1bHQxEjAQBgNVBAMMCUV2ZXJ2\n"
                 "YXVsdDEmMCQGCSqGSIb3DQEJARYXZXZlcnZhdWx0QGV2ZXJ2YXVsdC5jb20wHhcN\n"
                 "MjIwMjIyMTYwNjU1WhcNMjIwMzI0MTYwNjU1WjCBlzELMAkGA1UEBhMCSVIxEzAR\n"
                 "BgNVBAgMCkR1YmxpbiBDby4xDzANBgNVBAcMBkR1YmxpbjESMBAGA1UECgwJRXZl\n"
                 "cnZhdWx0MRIwEAYDVQQLDAlFdmVydmF1bHQxEjAQBgNVBAMMCUV2ZXJ2YXVsdDEm\n"
                 "MCQGCSqGSIb3DQEJARYXZXZlcnZhdWx0QGV2ZXJ2YXVsdC5jb20wggEiMA0GCSqG\n"
                 "SIb3DQEBAQUAA4IBDwAwggEKAoIBAQCy6jFXCBInR8wFaalqInx7AUePoidY8Q6Q\n"
                 "XGOSEykap/d2gTo5HV2UjHZb80IrDVm5jkO1yEnpPdSCUGxchrbktFujFHG0oNgI\n"
                 "BuFUzF4tdEictj/YgeAA4XjUosbINYXfDv/8HXUHsfwKyjnUVwxMcSAEkMWLec7d\n"
                 "pa5WYkNSnp+npsIMmkSgh6VkbsIu+HZJHJlrripvylqVBCLBLAjcHHbetwFAzg0q\n"
                 "hAPfXnO7oOn5dNwJ4uEOCLsCspruaZnys5ssCchQ9FhLS6zrVNx1jpY/G4S5K9Ii\n"
                 "DHyJvKaFj6UAPiupq2FMG1WAm0jpPD20QaEE9RlvSlNZ7McMFcMlAgMBAAEwDQYJ\n"
                 "KoZIhvcNAQELBQADggEBAF8fo8FH02rohgBB2bJO56g/Skti6UftusEMjmWMkHCA\n"
                 "uq7ErCcMwtl3z756Ygn89bTl89NFMt6aWoXHWMlZBCHGEIR2In2SY4cEWzW17VZJ\n"
                 "J6NbbPC8qFuZJtyDv2fNsYMS2rEqfgKWUVNIoBJS18fET+H28vrHVjcio8uPYFNh\n"
                 "Mh98YDkmaZDtgBZgQQLoGicn13m8KlT7AwtHx4q35qTvvcuECX6i1C5PJ987Hhzb\n"
                 "eMEIDjfeQE81XWiClf2Ax8oh3p0JEz5pq89G1HyORgLBerS8uPrVQ8kNXlJpV/Ss\n"
                 "+qHLABDIkCNZtJP+zzM2gTK/bflXi1do9AFB3J0E+DY=\n"
                 "-----END CERTIFICATE-----"
        )

        base_url_default = "https://api.evervault.com/"
        base_run_url_default = "https://run.evervault.com/"
        ca_host_default = "https://ca.evervault.com"

        api_key = "testing"

        request = Request(api_key, 30, False)

        cert = Cert(request, ca_host_default, base_run_url_default, base_url_default, api_key, api_key)

        assert cert.is_certificate_expired()
