from .e2e_test_case import EndToEndTestCase


class OutboundRelayTest(EndToEndTestCase):
    SYNTHETIC_ENDPOINT_URL = "https://o54dbmzbcj.execute-api.us-east-2.amazonaws.com/production?uuid=php-sdk-run&mode=outbound"

    def test_enable_outbound_relay(self):
        self.evervault.enable_outbound_relay(
            decryption_domains=[OutboundRelayTest.SYNTHETIC_ENDPOINT_URL]
        )

        payload = {
            "string": self.evervault.encrypt("some_string"),
            "number": self.evervault.encrypt(1234567890),
            "boolean": self.evervault.encrypt(True),
        }
        headers = {"Content-Type": "application/json"}

        response = self.make_request(
            OutboundRelayTest.SYNTHETIC_ENDPOINT_URL, headers, payload
        )
        print(response)
        self.assertEqual(response["request"]["string"], True)
        self.assertEqual(response["request"]["number"], True)
        self.assertEqual(response["request"]["boolean"], True)
