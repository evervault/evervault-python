import unittest
from unittest.mock import patch, MagicMock
from evervault.relay import RelayHTTPSAdapter


class TestRelayHTTPSAdapter(unittest.TestCase):

    @patch("evervault.relay.requests.get")
    def test_download_ca_cert_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"fake_certificate_content"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        proxy_url = "https://proxy.example.com"
        proxy_auth = "Basic someauthstring"
        ca_cert_url = "https://ca.example.com"

        RelayHTTPSAdapter(proxy_url, proxy_auth, ca_cert_url)

        mock_get.assert_called_once_with(ca_cert_url, timeout=10)

    @patch("evervault.relay.requests.get")
    @patch("evervault.relay.HTTPAdapter.proxy_headers")
    def test_proxy_headers(self, mock_super_proxy_headers, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"fake_certificate_content"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        mock_super_proxy_headers.return_value = {"Existing-Header": "existing_value"}

        proxy_url = "https://proxy.example.com"
        proxy_auth = "Basic someauthstring"
        ca_cert_url = "https://ca.example.com"

        adapter = RelayHTTPSAdapter(proxy_url, proxy_auth, ca_cert_url)
        proxy = {"some": "proxy"}

        headers = adapter.proxy_headers(proxy)

        self.assertIn("Proxy-Authorization", headers)
        self.assertEqual(headers["Proxy-Authorization"], proxy_auth)
        self.assertIn("Existing-Header", headers)
        self.assertEqual(headers["Existing-Header"], "existing_value")
