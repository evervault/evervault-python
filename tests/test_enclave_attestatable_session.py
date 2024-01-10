import unittest

import requests
import pytest
import importlib
import evervault

from evervault.enclaves import EnclaveVerificationException


class EnclaveAttestationTest(unittest.TestCase):
    def setUp(self):
        importlib.reload(evervault)
        self.evervault = evervault
        self.app_uuid = "app-f5f084041a7e"
        self.enclave_name = "synthetic-cage"
        self.evervault.init(self.app_uuid, "testing", curve="SECP256K1")

    def test_valid_pcrs(self):
        attested_session = self.evervault.attestable_enclave_session(
            {
                self.enclave_name: {
                    "pcr_8": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                }
            }
        )
        response = attested_session.get(
            f"https://{self.enclave_name}.{self.app_uuid}.enclave.evervault.com/echo"
        )
        assert response.status_code == 401

    def test_valid_pcrs_from_array(self):

        attested_session = self.evervault.attestable_enclave_session(
            {
                self.enclave_name: [
                    {
                        "pcr_8": "invalid00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                    },
                    {
                        "pcr_8": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                    },
                ]
            }
        )
        response = attested_session.get(
            f"https://{self.enclave_name}.{self.app_uuid}.enclave.evervault.com/echo"
        )
        assert response.status_code == 401

    def test_valid_pcrs_from_provider(self):
        def provider():
            pcrs = requests.get(
                "https://gist.githubusercontent.com/donaltuohy/5dbc1c175bcd0f0a9a621184cf3c78dc/raw/df25a123dea6424fb630ea80f241c676931728da/pcrs.json"
            ).json()
            return pcrs

        attested_session = self.evervault.attestable_enclave_session(
            {self.enclave_name: provider}
        )
        response = attested_session.get(
            f"https://{self.enclave_name}.{self.app_uuid}.enclave.evervault.com/echo"
        )
        assert response.status_code == 401

    def test_invalid_pcrs_from_provider(self):
        def provider():
            pcrs = requests.get(
                "https://gist.githubusercontent.com/hanneary/d076f6702c1694d29c117a1e00f1957e/raw/2c4999694e302cedb6283ba531dcdab45d556bcc/invalidpcr.json"
            ).json()
            return pcrs

        with pytest.raises(
            EnclaveVerificationException,
            match="The PCRs found were different to the expected values",
        ):
            attested_session = self.evervault.attestable_enclave_session(
                {self.enclave_name: provider}
            )

            attested_session.get(
                f"https://{self.enclave_name}.{self.app_uuid}.enclave.evervault.com/echo"
            )

    def test_invalid_pcrs(self):
        with pytest.raises(
            EnclaveVerificationException,
            match="The PCRs found were different to the expected values",
        ):
            attested_session = self.evervault.attestable_enclave_session(
                {
                    self.enclave_name: {
                        "pcr_8": "invalid000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                    }
                }
            )
            attested_session.get(
                f"https://{self.enclave_name}.{self.app_uuid}.enclave.evervault.com/echo"
            )
