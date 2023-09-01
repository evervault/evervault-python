from .e2e_test_case import EndToEndTestCase
import os


class OutboundRelayTest(EndToEndTestCase):
    SYNTHETIC_ENDPOINT_URL = os.getenv("EV_SYNTHETIC_ENDPOINT_URL")

    def test_enable_outbound_relay(self):
        self.evervault.enable_outbound_relay()

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
        self.assertEqual(response["request"]["string"], False)
        self.assertEqual(response["request"]["number"], False)
        self.assertEqual(response["request"]["boolean"], False)
