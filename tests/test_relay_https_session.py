import unittest

import requests
import pytest
import importlib
import evervault

from evervault.enclaves import EnclaveVerificationException


class RelayConnectionTest(unittest.TestCase):
    def setUp(self):
        importlib.reload(evervault)
        self.evervault = evervault
        self.app_uuid = "app-f5f084041a7e"
        self.cage_name = "synthetic-cage"
        self.evervault.init(self.app_uuid, "testing", curve="SECP256K1")
    
        
