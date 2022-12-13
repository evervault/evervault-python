import time
import unittest
import requests_mock
import pytest

from evervault.http.outboundrelayconfig import OutboundRelayConfig
from evervault.http.request import Request


class TestOutboundRelayConfig(unittest.TestCase):
    def setUp(self):
        self.request = Request("testing")
        self.base_url = "https://api.evervault.com/"

    @pytest.fixture(autouse=True)
    def run_before_and_after_tests(tmpdir):
        yield
        OutboundRelayConfig.clear_cache()
        OutboundRelayConfig.disable_polling()

    @requests_mock.Mocker()
    def test_retrieve_config_from_api(self, mock_request):
        self.__mock_relay_outbound_static(mock_request)
        OutboundRelayConfig.init(self.request, self.base_url)

        actual = OutboundRelayConfig.get_decryption_domains()
        expected = ["test-one.destinations.com", "test-two.destinations.com"]
        assert actual == expected

    @requests_mock.Mocker()
    def test_retrieve_config_from_api_change(self, mock_request):
        self.__mock_relay_outbound_config_changed(mock_request, "0.2")
        OutboundRelayConfig.init(self.request, self.base_url)

        time.sleep(0.5)

        actual = OutboundRelayConfig.get_decryption_domains()
        expected = ["test-one.destinations.com"]
        assert actual == expected

    @requests_mock.Mocker()
    def test_retrieve_config_from_api_with_poll_interval_change(self, mock_request):
        self.__mock_relay_outbound_config_poll_interval_changed(mock_request, 0.2, 0.5)
        OutboundRelayConfig.init(self.request, self.base_url)

        time.sleep(0.5)

        actual = OutboundRelayConfig.get_poll_interval()
        expected = 0.5
        assert actual == expected

    @requests_mock.Mocker()
    def test_clear_cache(self, mock_request):
        self.__mock_relay_outbound_static(mock_request, "0.2")
        OutboundRelayConfig.init(self.request, self.base_url)

        OutboundRelayConfig.clear_cache()
        actual = OutboundRelayConfig.get_decryption_domains()
        expected = None
        assert actual == expected

    def __mock_relay_outbound_static(self, mock_request, poll_interval=5):
        mock_request.get(
            "https://api.evervault.com/v2/relay-outbound",
            headers={"X-Poll-Interval": f"{poll_interval}"},
            json={
                "appUuid": "app_33b88ca7da01",
                "teamUuid": "2ef8d35ce661",
                "strictMode": True,
                "outboundDestinations": {
                    "test-one.destinations.com": {
                        "id": 144,
                        "appUuid": "app_33b88ca7da01",
                        "createdAt": "2022-10-05T08: 36: 35.681Z",
                        "updatedAt": "2022-10-05T08: 36: 35.681Z",
                        "deletedAt": None,
                        "routeSpecificFieldsToEncrypt": [],
                        "deterministicFieldsToEncrypt": [],
                        "encryptEmptyStrings": True,
                        "curve": "secp256k1",
                        "uuid": "outbound_destination_9733a04135f1",
                        "destinationDomain": "test-one.destinations.com",
                    },
                    "test-two.destinations.com": {
                        "id": 20,
                        "appUuid": "app_33b88ca7da01",
                        "createdAt": "2022-07-20T16: 02: 36.601Z",
                        "updatedAt": "2022-10-05T12: 40: 44.511Z",
                        "deletedAt": None,
                        "routeSpecificFieldsToEncrypt": [],
                        "deterministicFieldsToEncrypt": [],
                        "encryptEmptyStrings": True,
                        "curve": "secp256k1",
                        "uuid": "outbound_destination_e7f791332c51",
                        "destinationDomain": "test-two.destinations.com",
                    },
                },
            },
        )

    def __mock_relay_outbound_config_changed(self, mock_request, poll_interval=5):
        mock_request.get(
            "https://api.evervault.com/v2/relay-outbound",
            [
                {
                    "json": {
                        "appUuid": "app_33b88ca7da01",
                        "teamUuid": "2ef8d35ce661",
                        "strictMode": True,
                        "outboundDestinations": {
                            "test-one.destinations.com": {
                                "id": 144,
                                "appUuid": "app_33b88ca7da01",
                                "createdAt": "2022-10-05T08: 36: 35.681Z",
                                "updatedAt": "2022-10-05T08: 36: 35.681Z",
                                "deletedAt": None,
                                "routeSpecificFieldsToEncrypt": [],
                                "deterministicFieldsToEncrypt": [],
                                "encryptEmptyStrings": True,
                                "curve": "secp256k1",
                                "uuid": "outbound_destination_9733a04135f1",
                                "destinationDomain": "test-one.destinations.com",
                            },
                            "test-two.destinations.com": {
                                "id": 20,
                                "appUuid": "app_33b88ca7da01",
                                "createdAt": "2022-07-20T16: 02: 36.601Z",
                                "updatedAt": "2022-10-05T12: 40: 44.511Z",
                                "deletedAt": None,
                                "routeSpecificFieldsToEncrypt": [],
                                "deterministicFieldsToEncrypt": [],
                                "encryptEmptyStrings": True,
                                "curve": "secp256k1",
                                "uuid": "outbound_destination_e7f791332c51",
                                "destinationDomain": "test-two.destinations.com",
                            },
                        },
                    },
                    "headers": {"x-poll-interval": f"{poll_interval}"},
                    "status_code": 200,
                },
                {
                    "json": {
                        "appUuid": "app_33b88ca7da01",
                        "teamUuid": "2ef8d35ce661",
                        "strictMode": True,
                        "outboundDestinations": {
                            "test-one.destinations.com": {
                                "id": 144,
                                "appUuid": "app_33b88ca7da01",
                                "createdAt": "2022-10-05T08: 36: 35.681Z",
                                "updatedAt": "2022-10-05T08: 36: 35.681Z",
                                "deletedAt": None,
                                "routeSpecificFieldsToEncrypt": [],
                                "deterministicFieldsToEncrypt": [],
                                "encryptEmptyStrings": True,
                                "curve": "secp256k1",
                                "uuid": "outbound_destination_9733a04135f1",
                                "destinationDomain": "test-one.destinations.com",
                            },
                        },
                    },
                    "headers": {"x-poll-interval": f"{poll_interval}"},
                    "status_code": 200,
                },
            ],
        )

    def __mock_relay_outbound_config_poll_interval_changed(
        self, mock_request, initial_poll_interval=5, new_poll_interval=10
    ):
        mock_request.get(
            "https://api.evervault.com/v2/relay-outbound",
            [
                {
                    "json": {
                        "appUuid": "app_33b88ca7da01",
                        "teamUuid": "2ef8d35ce661",
                        "strictMode": True,
                        "outboundDestinations": {
                            "test-one.destinations.com": {
                                "id": 144,
                                "appUuid": "app_33b88ca7da01",
                                "createdAt": "2022-10-05T08: 36: 35.681Z",
                                "updatedAt": "2022-10-05T08: 36: 35.681Z",
                                "deletedAt": None,
                                "routeSpecificFieldsToEncrypt": [],
                                "deterministicFieldsToEncrypt": [],
                                "encryptEmptyStrings": True,
                                "curve": "secp256k1",
                                "uuid": "outbound_destination_9733a04135f1",
                                "destinationDomain": "test-one.destinations.com",
                            },
                            "test-two.destinations.com": {
                                "id": 20,
                                "appUuid": "app_33b88ca7da01",
                                "createdAt": "2022-07-20T16: 02: 36.601Z",
                                "updatedAt": "2022-10-05T12: 40: 44.511Z",
                                "deletedAt": None,
                                "routeSpecificFieldsToEncrypt": [],
                                "deterministicFieldsToEncrypt": [],
                                "encryptEmptyStrings": True,
                                "curve": "secp256k1",
                                "uuid": "outbound_destination_e7f791332c51",
                                "destinationDomain": "test-two.destinations.com",
                            },
                        },
                    },
                    "headers": {"X-Poll-Interval": f"{initial_poll_interval}"},
                    "status_code": 200,
                },
                {
                    "json": {
                        "appUuid": "app_33b88ca7da01",
                        "teamUuid": "2ef8d35ce661",
                        "strictMode": True,
                        "outboundDestinations": {
                            "test-one.destinations.com": {
                                "id": 144,
                                "appUuid": "app_33b88ca7da01",
                                "createdAt": "2022-10-05T08: 36: 35.681Z",
                                "updatedAt": "2022-10-05T08: 36: 35.681Z",
                                "deletedAt": None,
                                "routeSpecificFieldsToEncrypt": [],
                                "deterministicFieldsToEncrypt": [],
                                "encryptEmptyStrings": True,
                                "curve": "secp256k1",
                                "uuid": "outbound_destination_9733a04135f1",
                                "destinationDomain": "test-one.destinations.com",
                            },
                            "test-two.destinations.com": {
                                "id": 20,
                                "appUuid": "app_33b88ca7da01",
                                "createdAt": "2022-07-20T16: 02: 36.601Z",
                                "updatedAt": "2022-10-05T12: 40: 44.511Z",
                                "deletedAt": None,
                                "routeSpecificFieldsToEncrypt": [],
                                "deterministicFieldsToEncrypt": [],
                                "encryptEmptyStrings": True,
                                "curve": "secp256k1",
                                "uuid": "outbound_destination_e7f791332c51",
                                "destinationDomain": "test-two.destinations.com",
                            },
                        },
                    },
                    "headers": {"X-Poll-Interval": f"{new_poll_interval}"},
                    "status_code": 200,
                },
            ],
        )
