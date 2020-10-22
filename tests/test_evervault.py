import unittest
import pytest
import evervault
import requests_mock
from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class TestEvervault(unittest.TestCase):
    def setUp(self):
        self.evervault = evervault
        self.evervault.api_key = "testing"

    def tearDown(self):
        self.evervault = None

    @requests_mock.Mocker()
    def test_encrypt_dicts(self, m):
        self.mock_fetch_cage_key(m)
        encrypted_data = self.evervault.encrypt({"name": "testing"})
        assert encrypted_data != {"name": "testing"}
        assert "name" in encrypted_data

    @requests_mock.Mocker()
    def test_encrypt_strings(self, m):
        self.mock_fetch_cage_key(m)
        encrypted_data = self.evervault.encrypt("name")
        assert encrypted_data != "name"

    @requests_mock.Mocker()
    def test_run(self, m):
        request = m.post(
            "https://cage.run/testing-cage",
            json={"result": "there was an attempt"},
            request_headers={"Api-Key": "testing"},
        )
        resp = self.evervault.run("testing-cage", {"name": "testing"})
        assert request.called
        assert resp["result"] == "there was an attempt"
        assert request.last_request.json() == {"name": "testing"}

    @requests_mock.Mocker()
    def test_encrypt_and_run(self, m):
        self.mock_fetch_cage_key(m)
        request = m.post(
            "https://cage.run/testing-cage",
            json={"result": "there was an attempt"},
            request_headers={"Api-Key": "testing"},
        )
        resp = self.evervault.encrypt_and_run("testing-cage", {"name": "testing"})
        assert request.called
        assert resp["result"] == "there was an attempt"
        assert request.last_request.json() != {"name": "testing"}
        assert "name" in request.last_request.json()

    def mock_fetch_cage_key(self, m):
        # Create private key
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        # Create public key
        public_key = private_key.public_key()

        m.get(
            "https://api.evervault.com/cages/key",
            json={
                "key": public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                ).decode("utf8")
            },
        )
