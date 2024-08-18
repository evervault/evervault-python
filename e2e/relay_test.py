from .e2e_test_case import EndToEndTestCase


class RelayProxyConnectTest(EndToEndTestCase):
    def test_relay_requests_adapter(self):

        https_adapter = self.evervault.relay_requests_adapter()

        payload = {
            "string": self.evervault.encrypt("some_string"),
            "number": self.evervault.encrypt(1234567890),
            "boolean": self.evervault.encrypt(True),
        }
        headers = {"Content-Type": "application/json"}

        synthetic_endpoint = (
            self.syntheticEndpointurl + "?syntheticUuid=python-e2e&mode=outbound"
        )

        response = self.make_request(
            synthetic_endpoint, headers, payload, https_adapter
        )

        print(response)
        self.assertEqual(response["request"]["string"], False)
        self.assertEqual(response["request"]["number"], False)
        self.assertEqual(response["request"]["boolean"], False)
