import unittest
import pytest
import evervault
import requests_mock
import base64
from evervault.crypto.key import Key
from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey

class TestEvervault(unittest.TestCase):
    def setUp(self):
        self.evervault = evervault
        self.evervault.api_key = "testing"
        self.public_key = self.build_keys()

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
    def test_run_with_options(self, m):
        request = m.post(
            "https://cage.run/testing-cage",
            json={"status": "queued"},
            request_headers={ "Api-Key": "testing", "x-version-id": "2", "x-async": "true" },
        )
        resp = self.evervault.run("testing-cage", {"name": "testing"}, {"async": True, "version": 2})
        assert request.called
        assert resp["status"] == "queued"
        assert request.last_request.json() == {"name": "testing"}
        assert request.last_request.headers["x-async"] == "true"
        assert request.last_request.headers["x-version-id"] == "2"

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

    @requests_mock.Mocker()
    def test_encrypt_and_run_with_options(self, m):
        request = m.post(
            "https://cage.run/testing-cage",
            json={"status": "queued"},
            request_headers={ "Api-Key": "testing", "x-version-id": "2", "x-async": "true" },
        )
        resp = self.evervault.encrypt_and_run("testing-cage", {"name": "testing"}, {"async": True, "version": 2})
        assert request.called
        assert resp["status"] == "queued"
        assert request.last_request.json() != {"name": "testing"}
        assert request.last_request.headers["x-async"] == "true"
        assert request.last_request.headers["x-version-id"] == "2"

    def mock_fetch_cage_key(self, m):
        m.get(
            "https://api.evervault.com/cages/key",
            json={
                "ecdhKey": self.public_key.decode("utf8")
            },
        )
    
    def build_keys(self):
        ecdh_private_key = ec.generate_private_key(
            ec.SECP256K1()
        )

        public_key = ecdh_private_key.public_key()
        key = public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.CompressedPoint
        )
        
        return (base64.b64encode(key))

    def get_iv(self, data):
        return base64.b64decode(data[1])

    def get_public_key(self, data):
        return base64.b64decode(data[2])

    def get_encrypted_data(self, data):
        b64_string = data[3]
        b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
        return base64.b64decode(b64_string)