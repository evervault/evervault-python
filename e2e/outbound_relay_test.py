from .e2e_test_case import EndToEndTestCase


class OutboundRelayTest(EndToEndTestCase):
    def test_enable_outbound_relay(self):
        self.evervault.enable_outbound_relay()

        payload = {
            "string": self.evervault.encrypt("some_string"),
            "number": self.evervault.encrypt(1234567890),
            "boolean": self.evervault.encrypt(True),
        }
        headers = {"Content-Type": "application/json"}

        synthetic_endpoint = (
            self.syntheticEndpointurl + "/syntheticUuid=python-e2e&mode=outbound"
        )
        response = self.make_request(synthetic_endpoint, headers, payload)
        print(response)
        self.assertEqual(response["request"]["string"], False)
        self.assertEqual(response["request"]["number"], False)
        self.assertEqual(response["request"]["boolean"], False)
