import unittest
import time
import os
import pytest
import importlib
import evervault
import json

from evervault.cages_v2 import CageVerificationException


class CageAttestationTest(unittest.TestCase):
    def setUp(self):
        importlib.reload(evervault)
        self.evervault = evervault
        self.app_uuid = "app-f5f084041a7e"
        self.cage_name = "synthetic-cage"
        self.evervault.init(self.app_uuid, "testing", curve="SECP256K1")

    def test_valid_pcrs(self):
        attested_session = self.evervault.attestable_cage_session(
            {
                self.cage_name: {
                    "pcr_8": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                }
            }
        )
        response = attested_session.get(
            f"https://{self.cage_name}.{self.app_uuid}.cage.evervault.com/echo"
        )
        assert response.status_code == 401

    def test_invalid_pcrs(self):
        with pytest.raises(
            CageVerificationException,
            match="The PCRs found were different to the expected values",
        ):
            attested_session = self.evervault.attestable_cage_session(
                {
                    self.cage_name: {
                        "pcr_8": "invalid000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                    }
                }
            )
            attested_session.get(
                f"https://{self.cage_name}.{self.app_uuid}.cage.evervault.com/echo"
            )

    def test_valid_pcrs_beta(self):
        attested_session = self.evervault.cage_requests_session(
            {
                self.cage_name: {
                    "pcr_8": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                }
            }
        )
        response = attested_session.get(
            f"https://{self.cage_name}.{self.app_uuid}.cages.evervault.com/echo"
        )
        assert response.status_code == 401

    def test_invalid_pcrs_beta(self):
        with pytest.raises(
            CageVerificationException,
            match="The PCRs found were different to the expected values",
        ):
            attested_session = self.evervault.cage_requests_session(
                {
                    self.cage_name: {
                        "pcr_8": "invalid000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                    }
                }
            )
            attested_session.get(
                f"https://{self.cage_name}.{self.app_uuid}.cages.evervault.com/echo"
            )
