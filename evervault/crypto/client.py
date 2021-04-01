from .key import Key
from ..errors.evervault_errors import UndefinedDataError, InvalidPublicKeyError, MissingTeamEcdhKey
from ..datatypes.map import map_header_type
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey, EllipticCurve
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from secrets import token_bytes
from base64 import b64encode
import json
import uuid
import base64

BS = 32


class Client(object):
    def __init__(self):
        self.public_key = None
        self.team_ecdh_key = None
        self.generated_ecdh_key = None
        self.shared_key = None

    def encrypt_data(self, fetch, data):
        if data is None:
            raise UndefinedDataError("Data not defined")
        self.__fetch_cage_key(fetch)
        self.shared_key = self.__derive_shared_key()
        
        if self.shared_key is None or type(self.shared_key) != bytes:
            raise InvalidPublicKeyError("Provided EC compressed point is invalid")
        if type(data) == dict:
            return self.__encrypt_object(data)
        elif self.__encryptable_data(data):
            return self.__encrypt_string(data)

    def __encrypt_object(self, data):
        if self.__encryptable_data(data):
            return self.__encrypt_string(data)
        elif type(data) == dict:
            encrypted_data = {}
            for key, value in data.items():
                encrypted_data[key] = self.__encrypt_object(value)
            return encrypted_data
        else:
            return data

    def __encrypt_string(self, data):
        iv = token_bytes(12)
        aesgcm = AESGCM(self.shared_key)
        encrypted_bytes = aesgcm.encrypt(iv, bytes(data, "utf8"), None)
        header_type = map_header_type(data)
        
        return self.__format(
            header_type,
            b64encode(iv).decode("utf"),
            b64encode(self.generated_ecdh_key).decode("utf"),
            b64encode(encrypted_bytes).decode("utf"),
        )

    def __format(self, header, iv, public_key, encrypted_payload):
        prefix = ":{header}" if header != "string" else ""
        return f"ev{prefix}:{self.__base_64_remove_padding(iv)}:{self.__base_64_remove_padding(public_key)}:{self.__base_64_remove_padding(encrypted_payload)}:$"

    def __base_64_to_base_64_url(self, base_64_string):
        return base_64_string.replace("+", "-").replace("/", "_")

    def __utf8_to_base_64_url(self, data):
        b64_string = b64encode(data.encode("utf8")).decode("utf8")
        return self.__base_64_to_base_64_url(b64_string)

    def __base_64_remove_padding(self, data):
        return data.rstrip("=")

    def __public_encrypt(self, root_key):
        return self.public_key.encrypt(
            root_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None,
            ),
        )

    def __encryptable_data(self, data):
        return data is not None and (
            type(data) == str
            or type(data) == bool
            or type(data) == list
            or type(data) == int
            or type(data) == float
        )

    def __fetch_cage_key(self, fetch):
        if self.team_ecdh_key is None:
            resp = fetch.get("cages/key")
            decoded_team_cage_key = base64.b64decode(resp["ecdhKey"])
            
            self.team_ecdh_key = EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), decoded_team_cage_key)
            
    def __derive_shared_key(self):
        if self.team_ecdh_key is None:
            raise MissingTeamEcdhKey("Team ECDH key not set in client")
        else:
            generated_key = ec.generate_private_key(
                ec.SECP256K1
            )
            self.generated_ecdh_key = generated_key.public_key().public_bytes(
                Encoding.X962,
                PublicFormat.CompressedPoint
            )
            shared_key = generated_key.exchange(
                ec.ECDH(), self.team_ecdh_key
            )
            return shared_key