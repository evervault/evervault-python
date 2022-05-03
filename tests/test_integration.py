import unittest
import evervault
import os
import logging
import certifi

API_KEY = "API_KEY"
EV_CAGE_NAME = "EV_CAGE_NAME"
TEAM_UUID = "TEAM_UUID"
DEFAULT_GET_URL = "https://enssc1aqsjv0g.x.pipedream.net/outbound"


class TestIntegration(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        print(certifi.where())
        os.environ["EV_API_URL"] = "https://api.evervault.io/"
        os.environ["EV_CAGE_RUN_URL"] = "https://run.evervault.io/"
        os.environ["EV_TUNNEL_HOSTNAME"] = "https://relay.evervault.io:443"
        os.environ["EV_CERT_HOSTNAME"] = "https://ca.evervault.io"

    def tearDown(self):
        self.__del_env_var("EV_API_URL")
        self.__del_env_var("EV_CAGE_RUN_URL")
        self.__del_env_var("EV_TUNNEL_HOSTNAME")
        self.__del_env_var("EV_CERT_HOSTNAME")

    def __del_env_var(self, var):
        if var in os.environ:
            os.environ.pop(var)

    def test_encrypts_and_run_correctly_with_intercept(self):
        api_key = os.environ.get(API_KEY)
        ev_cage_name = os.environ.get(EV_CAGE_NAME)
        evervault.init(api_key)
        result = evervault.encrypt_and_run(ev_cage_name, {"name": "foo"})
        assert result['result']['message'] == "Hello from a Cage! It seems you have 3 letters in your name"

    def test_relay_works_as_expected_without_intercept(self):
        api_key = os.environ.get(API_KEY)
        ev_cage_name = os.environ.get(EV_CAGE_NAME)
        evervault.init(api_key, intercept=False)
        result = evervault.encrypt_and_run(ev_cage_name, {"name": "foo"})
        assert result['result']['message'] == "Hello from a Cage! It seems you have 3 letters in your name"

    def test_encrypts_and_run_correctly_with_intercept_256R1(self):
        api_key = os.environ.get(API_KEY)
        ev_cage_name = os.environ.get(EV_CAGE_NAME)
        evervault.init(api_key, curve=evervault.Curves.SECP256R1)
        result = evervault.encrypt_and_run(ev_cage_name, {"name": "foo"})
        assert result['result']['message'] == "Hello from a Cage! It seems you have 3 letters in your name"

    def test_relay_works_as_expected_without_intercept_256R1(self):
        api_key = os.environ.get(API_KEY)
        ev_cage_name = os.environ.get(EV_CAGE_NAME)
        evervault.init(api_key, intercept=False, curve=evervault.Curves.SECP256R1)
        result = evervault.encrypt_and_run(ev_cage_name, {"name": "foo"})
        assert result['result']['message'] == "Hello from a Cage! It seems you have 3 letters in your name"
