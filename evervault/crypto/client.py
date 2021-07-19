from ..errors.evervault_errors import UndefinedDataError, InvalidPublicKeyError, MissingTeamEcdhKey, UnknownEncryptType
from ..datatypes.map import map_header_type
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from secrets import token_bytes
import base64
import time 
from .version import EV_VERSION

BS = 32
KEY_INTERVAL = 15

class Client(object):
    def __init__(self):
        self.public_key = None
        self.team_ecdh_key = None
        self.generated_ecdh_key = None
        self.shared_key = None
        self.start_time = int(time.time())
        self.ev_version = self.__base_64_remove_padding(base64.b64encode(bytes(EV_VERSION, "utf8")).decode("utf"))

    def encrypt_data(self, fetch, data):
        if data is None:
            raise UndefinedDataError("Data not defined")
        self.__fetch_cage_key(fetch)
        self.shared_key = self.__derive_shared_key()
        
        if self.shared_key is None or type(self.shared_key) != bytes:
            raise InvalidPublicKeyError("Provided EC compressed point is invalid")        
        
        if type(data) == dict or type(data) == list or type(data) == set:
            return self.__traverse_and_encrypt(data)
        elif self.__encryptable_data(data):
            return self.__encrypt_string(data)
        else:
            raise UnknownEncryptType(f'Cannot encrypt unsupported type {data}')

    def __traverse_and_encrypt(self, data):
        if type(data) == list:
            for idx, item in enumerate(data):
                if not self.__encryptable_data(item):
                    data[idx] = self.__traverse_and_encrypt(item)
                else:
                    data[idx] = self.__encrypt_string(item)
            return data
        elif type(data) == dict:
            return self.__encrypt_object(data)
        elif type(data) == set:
            return self.__encrypt_set(data)    
        elif self.__encryptable_data(data):
            return self.__encrypt_string(data)
        else: 
            raise UnknownEncryptType(f'Cannot encrypt unsupported type {data}')
    
    def __encrypt_object(self, data):
        encrypted_data = {}
        for key, value in data.items():
            if self.__encryptable_data(value):
                encrypted_data[key] = self.__encrypt_string(value)
            else:
                encrypted_data[key] = self.__traverse_and_encrypt(value)
        return encrypted_data

    def __encrypt_set(self, data):
        encrypted_set = set()
        for item in data:
            if self.__encryptable_data(item):
                encrypted_set.add(self.__encrypt_string(item))
            else:
                encrypted_set.add(self.__traverse_and_encrypt(item))
        return encrypted_set

    def __encrypt_string(self, data):
        header_type = map_header_type(data)
        coerced_data = self.__coerce_type(data) 
        iv = token_bytes(12)
        aesgcm = AESGCM(self.shared_key)
        
        encrypted_bytes = aesgcm.encrypt(iv, bytes(coerced_data, "utf8"), None)
        
        return self.__format(
            header_type,
            base64.b64encode(iv).decode("utf"),
            base64.b64encode(self.generated_ecdh_key).decode("utf"),
            base64.b64encode(encrypted_bytes).decode("utf"),
        )

    def __coerce_type(self, data):
        if type(data) == bool:
            return str(int(data))
        elif type(data) == int or type(data) == float:
            return str(data)
        else:
            return data

    def __format(self, header, iv, public_key, encrypted_payload):
        prefix = f":{header}" if header != "string" else ""
        return f"ev:{self.ev_version}{prefix}:{self.__base_64_remove_padding(iv)}:{self.__base_64_remove_padding(public_key)}:{self.__base_64_remove_padding(encrypted_payload)}:$"

    def __base_64_remove_padding(self, data):
        return data.rstrip("=")

    def __encryptable_data(self, data):
        return data is not None and (
            type(data) == str
            or type(data) == bool
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
        elif self.shared_key is None:
            return self.__generate_shared_key()
        else:
            now = int(time.time())
            time_diff = now - self.start_time
            if time_diff > KEY_INTERVAL:
                self.start_time = now
                return self.__generate_shared_key()
            return self.shared_key

    def __generate_shared_key(self):
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