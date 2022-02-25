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
                 "MIIDgTCCAmmgAwIBAgIUHswvxVNBQtximEK88HKyfvgFSvowDQYJKoZIhvcNAQEL\n"
                 "BQAwUDELMAkGA1UEBhMCSUUxEjAQBgNVBAgMCUR1YmxpbiBDbzEPMA0GA1UEBwwG\n"
                 "U3dvcmRzMRwwGgYDVQQKDBNEZWZhdWx0IENvbXBhbnkgTHRkMB4XDTA4MTIyNDA4\n"
                 "MTYwN1oXDTE4MTIyMjA4MTYwN1owUDELMAkGA1UEBhMCSUUxEjAQBgNVBAgMCUR1\n"
                 "YmxpbiBDbzEPMA0GA1UEBwwGU3dvcmRzMRwwGgYDVQQKDBNEZWZhdWx0IENvbXBh\n"
                 "bnkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv163bZj6G8BE\n"
                 "4uJYVOGWeOCmxjTuJVO0YSNvxF1AikosVPsFerlF4bXy88vQnW8Qc68rST5IXYpF\n"
                 "ooGo7DalQRjMXr1z3qImx57nLVR0DBKXgPYGf4GjpAmREi4rAngvZgBB8k8lyFi/\n"
                 "hFhRfohOOP2UOPSme7j62C7Q/t41U7UBvSGo67Y+k2dkQihKl8vCAF0Ucs5b+8Fp\n"
                 "c5auik4nEG80MDnf6FOQc7ky1fLAsfor9hCaCS4SMPXfum+zwQvruYNxdIaktsml\n"
                 "+SAi/ZUpEkRs2d3OXIUm9+es+ClEyJoLKwIcFvzXE1x49J5tc3J9svfbVGvtd4ts\n"
                 "opBTAdZFNQIDAQABo1MwUTAdBgNVHQ4EFgQU2wEr/gRENzOEg35T6Y/UKn2DTbgw\n"
                 "HwYDVR0jBBgwFoAU2wEr/gRENzOEg35T6Y/UKn2DTbgwDwYDVR0TAQH/BAUwAwEB\n"
                 "/zANBgkqhkiG9w0BAQsFAAOCAQEAFIvXtts3WDesK/wnI7U6vy4tjuukOIZ+Pzsy\n"
                 "rup848fhL92pmwr+2r1GRc5WFJ5R4utwk9zcQOvM2xII/JySPEj+hDPuutocG8cq\n"
                 "GEC2dq1HTF5USMhDM0uqqYr0zcONsg/O6/wzWJ8eHoLgYIrImyeo5znm97sA7CvO\n"
                 "gnt3YSfd6yYUD0sBBQy7TM5ZSWYoyJButlyTSPHWu7e+z91CenJ7e+IJgfHt8AzB\n"
                 "950mXtBjHPtGH1CkrvKvAtZAOVpeE9Jlb4vdI1fOROw3gV/7+5HMdW72SxHLXGIp\n"
                 "BplX3pdgL7YIyjBeYgCLuqWFsQOw18VeT1v/WMIZ6dx1b1GCtQ==\n"
                 "-----END CERTIFICATE-----\n"
        )

        base_url_default = "https://api.evervault.com/"
        base_run_url_default = "https://run.evervault.com/"
        ca_host_default = "https://ca.evervault.com"

        api_key = "testing"

        request = Request(api_key, 30, False)

        cert = Cert(request, ca_host_default, base_run_url_default, base_url_default, api_key, api_key)

        cert.setup()

        assert cert.is_certificate_expired()

    @requests_mock.Mocker()
    def test_not_available_cert_is_not_expired(self, mock_request):
        mock_request.get(
            "https://ca.evervault.com",
            text=""
        )
        base_url_default = "https://api.evervault.com/"
        base_run_url_default = "https://run.evervault.com/"
        ca_host_default = "https://ca.evervault.com"

        api_key = "testing"

        request = Request(api_key, 30, False)

        cert = Cert(request, ca_host_default, base_run_url_default, base_url_default, api_key, api_key)

        cert.setup()

        assert cert.is_certificate_expired() == False
