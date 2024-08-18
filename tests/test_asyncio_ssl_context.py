import unittest
from unittest.mock import patch, MagicMock
from evervault.relay import RelayAsyncioSSLContext
import asyncio


class TestRelayAsyncioSSLContext(unittest.TestCase):

    @patch("evervault.relay.get_cert_file")
    def test_init(self, mock_get_cert_file):
        mock_get_cert_file.return_value = "/path/to/certfile"

        ca_cert_url = "https://ca.example.com"
        relay_context = RelayAsyncioSSLContext(ca_cert_url)

        self.assertEqual(relay_context.ca_file_path, "/path/to/certfile")
        mock_get_cert_file.assert_called_once_with(ca_cert_url=ca_cert_url)

    @patch("evervault.relay.get_cert_file")
    @patch("evervault.relay.ssl.create_default_context")
    @patch("evervault.relay.aiohttp.TCPConnector")
    @patch("evervault.relay.setattr")
    def test_asyncio_context(
        self,
        mock_setattr,
        mock_tcp_connector,
        mock_create_default_context,
        mock_get_cert_file,
    ):
        mock_ssl_context = MagicMock()
        mock_create_default_context.return_value = mock_ssl_context
        mock_get_cert_file.return_value = "/path/to/certfile"

        ca_cert_url = "https://ca.example.com"
        ca_file_path = "/path/to/certfile"

        relay_context = RelayAsyncioSSLContext(ca_cert_url)
        relay_context.ca_file_path = ca_file_path

        connector = relay_context.asyncio_context()

        mock_setattr.assert_called_once_with(
            asyncio.sslproto._SSLProtocolTransport, "_start_tls_compatible", True
        )
        mock_create_default_context.assert_called_once_with(cafile=ca_file_path)
        mock_tcp_connector.assert_called_once_with(ssl_context=mock_ssl_context)
        self.assertEqual(connector, mock_tcp_connector.return_value)


if __name__ == "__main__":
    unittest.main()
