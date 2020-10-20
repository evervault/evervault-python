from .key import Key
from ..errors.evervault_errors import UndefinedDataError, InvalidPublicKeyError
from ..datatypes.map import map_header_type
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from secrets import token_bytes
from base64 import b64encode
import json
import uuid

BS = 32


class Client(object):
    def __init__(self):
        self.cage_key = None
        self.public_key = None

    def encrypt_data(self, fetch, data):
        if data is None:
            raise UndefinedDataError("Data not defined")
        self.__fetch_cage_key(fetch)

        if self.cage_key is None or type(self.cage_key) != str:
            raise InvalidPublicKeyError("Provided public key is invalid")
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
        iv = token_bytes(int(BS / 2))
        root_key = token_bytes(BS)
        aes = AES.new(root_key, AES.MODE_GCM, iv)
        encrypted_string, auth_tag = aes.encrypt_and_digest(data.encode("utf8"))

        encrypted_buffer = encrypted_string + auth_tag
        encrypted_key = self.__public_encrypt(root_key)
        header_type = map_header_type(data)

        return self.__format(
            header_type,
            b64encode(encrypted_key).decode("utf"),
            b64encode(encrypted_buffer).decode("utf"),
            b64encode(iv).decode("utf"),
        )

    def __format(self, header, encrypted_key, encrypted_buffer, iv):
        header = self.__utf8_to_base_64_url(
            json.dumps({"iss": "evervault", "version": 1, "datatype": header})
        )
        payload = self.__utf8_to_base_64_url(
            json.dumps(
                {
                    "cageData": encrypted_key,
                    "keyIv": iv,
                    "sharedEncryptedData": encrypted_buffer,
                }
            )
        )
        return f"{header}.{payload}.{str(uuid.uuid4())}"

    def __base_64_to_base_64_url(self, base_64_string):
        return base_64_string.replace("+", "-").replace("/", "_")

    def __utf8_to_base_64_url(self, data):
        b64_string = b64encode(data.encode("utf8")).decode("utf8")
        return self.__base_64_to_base_64_url(b64_string)

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
        if self.cage_key is None:
            resp = fetch.get("cages/key")
            self.cage_key = Key(resp["key"]).key
            self.public_key = serialization.load_pem_public_key(
                self.cage_key.encode("utf8"), backend=default_backend()
            )
