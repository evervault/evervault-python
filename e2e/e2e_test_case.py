import evervault
import os
import importlib
import unittest
import requests
import json


class EndToEndTestCase(unittest.TestCase):
    def setUp(self, curve="SECP256K1"):
        super(EndToEndTestCase, self).setUp()
        importlib.reload(evervault)
        self.evervault = evervault
        self.app_uuid = os.getenv("EV_APP_UUID")
        self.api_key = os.getenv("EV_API_KEY")
        self.syntheticEndpointurl = os.getenv("EV_SYNTHETIC_ENDPOINT_URL")
        self.evervault.init(self.app_uuid, self.api_key, curve=curve)

    def tearDown(self):
        super(EndToEndTestCase, self).tearDown()
        self.evervault.ev_client = None
        self.evervault = None
        self.__del_env_var("EV_API_URL")
        self.__del_env_var("EV_CAGE_RUN_URL")
        self.__del_env_var("EV_TUNNEL_HOSTNAME")
        self.__del_env_var("EV_CERT_HOSTNAME")
        self.__del_env_var("EV_MAX_FILE_SIZE_IN_MB")

    def make_request(self, url, headers, payload):
        resp = requests.post(url, json=payload, headers=headers)
        return json.loads(resp.content)

    def __del_env_var(self, var):
        if var in os.environ:
            os.environ.pop(var)
