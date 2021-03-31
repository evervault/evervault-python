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

    def tearDown(self):
        self.evervault = None

    # @requests_mock.Mocker()
    # def test_encrypt_dicts(self, m):
    #     self.mock_fetch_cage_key(m)
    #     encrypted_data = self.evervault.encrypt({"name": "testing"})
    #     assert encrypted_data != {"name": "testing"}
    #     assert "name" in encrypted_data

    @requests_mock.Mocker()
    def test_encrypt_strings(self, m):
        public_key, private_key = self.build_keys()
        self.mock_fetch_cage_key(m, public_key)
        encrypted_data = self.evervault.encrypt("name")
        print(encrypted_data)
        self.decrypt_with_key(private_key, encrypted_data)
        assert encrypted_data != "name"

    # @requests_mock.Mocker()
    # def test_run(self, m):
    #     request = m.post(
    #         "https://cage.run/testing-cage",
    #         json={"result": "there was an attempt"},
    #         request_headers={"Api-Key": "testing"},
    #     )
    #     resp = self.evervault.run("testing-cage", {"name": "testing"})
    #     assert request.called
    #     assert resp["result"] == "there was an attempt"
    #     assert request.last_request.json() == {"name": "testing"}

    # @requests_mock.Mocker()
    # def test_run_with_options(self, m):
    #     request = m.post(
    #         "https://cage.run/testing-cage",
    #         json={"status": "queued"},
    #         request_headers={ "Api-Key": "testing", "x-version-id": "2", "x-async": "true" },
    #     )
    #     resp = self.evervault.run("testing-cage", {"name": "testing"}, {"async": True, "version": 2})
    #     assert request.called
    #     assert resp["status"] == "queued"
    #     assert request.last_request.json() == {"name": "testing"}
    #     assert request.last_request.headers["x-async"] == "true"
    #     assert request.last_request.headers["x-version-id"] == "2"

    # @requests_mock.Mocker()
    # def test_encrypt_and_run(self, m):
    #     self.mock_fetch_cage_key(m)
    #     request = m.post(
    #         "https://cage.run/testing-cage",
    #         json={"result": "there was an attempt"},
    #         request_headers={"Api-Key": "testing"},
    #     )
    #     resp = self.evervault.encrypt_and_run("testing-cage", {"name": "testing"})
    #     assert request.called
    #     assert resp["result"] == "there was an attempt"
    #     assert request.last_request.json() != {"name": "testing"}
    #     assert "name" in request.last_request.json()

    # @requests_mock.Mocker()
    # def test_encrypt_and_run_with_options(self, m):
    #     request = m.post(
    #         "https://cage.run/testing-cage",
    #         json={"status": "queued"},
    #         request_headers={ "Api-Key": "testing", "x-version-id": "2", "x-async": "true" },
    #     )
    #     resp = self.evervault.encrypt_and_run("testing-cage", {"name": "testing"}, {"async": True, "version": 2})
    #     assert request.called
    #     assert resp["status"] == "queued"
    #     assert request.last_request.json() != {"name": "testing"}
    #     assert request.last_request.headers["x-async"] == "true"
    #     assert request.last_request.headers["x-version-id"] == "2"

    def mock_fetch_cage_key(self, m, ecdh_public_key):
        # Create private key
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        ecdh_key = ec.generate_private_key(
            ec.SECP256K1()
        )
        
        # Create public key
        public_key = private_key.public_key()
        public_ecdh_key = ecdh_key.public_key()
 
        m.get(
            "https://api.evervault.com/cages/key",
            json={
                "key": public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                ).decode("utf8"),
                "ecdhKey": ecdh_public_key.decode("utf8")
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
        pk = ecdh_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        return (base64.b64encode(key), pk)

    def decrypt_with_key(self, private_key, data):
        split_data = data.split(":")
        keyIv = self.get_iv(split_data)
        incoming_public_key = self.get_public_key(split_data)
        encrypted_data = self.get_encrypted_data(split_data)
        incoming_public_key = EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), self.get_public_key(split_data))
        
        private_key = serialization.load_pem_private_key(
            private_key,
            password=None
        )

        shared_secret = private_key.exchange(
            ec.ECDH(),
            incoming_public_key
        )

        derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=None,
                backend=default_backend()
            ).derive(shared_secret)
        print(len(derived_key))
        print(len(encrypted_data))
        print(len(keyIv))
        aesgcm = AESGCM(derived_key)
        decrypted_data = aesgcm.decrypt(
            keyIv,
            encrypted_data,
            None
        )
        print(decrypted_data)

    def get_iv(self, data):
        return base64.b64decode(data[1])

    def get_public_key(self, data):
        return base64.b64decode(data[2])

    def get_encrypted_data(self, data):
        b64_string = data[3]
        b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
        return base64.b64decode(b64_string)