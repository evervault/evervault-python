from evervault.crypto.curves.koblitz import KoblitzPublicKey
from ..errors.evervault_errors import (
    EvervaultError,
    ExceededMaxFileSizeError,
)
from ..datatypes.map import map_header_type
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from secrets import token_bytes
import base64
import time
import binascii
import struct
from .version import VERSION, VERSION_WITH_METADATA
from .curves.p256 import P256PublicKey

BS = 32
KEY_INTERVAL = 15

SECP256R1 = "SECP256R1"
SECP256K1 = "SECP256K1"
CURVES = {"SECP256K1": ec.SECP256K1, "SECP256R1": ec.SECP256R1}


class Client(object):
    def __init__(self, api_key=None, curve="SECP256K1", max_file_size_in_mb=25):
        self.curve = curve
        self.public_key = None
        self.team_ecdh_key = None
        self.decoded_team_cage_key = None
        self.compressed_public_key = None
        self.uncompressed_public_key = None
        self.shared_key = None
        self.start_time = int(time.time())
        self.api_key = api_key
        self.ev_version = self.__base_64_remove_padding(
            base64.b64encode(bytes(VERSION[self.curve], "utf8")).decode("utf")
        )
        self.ev_version_with_metadata = self.__base_64_remove_padding(
            base64.b64encode(bytes(VERSION_WITH_METADATA[self.curve], "utf8")).decode(
                "utf"
            )
        )
        self.max_file_size_in_mb = max_file_size_in_mb
        self.max_file_size_in_bytes = max_file_size_in_mb * 1024 * 1024

    def encrypt_data(self, fetch, data, role):
        if data is None:
            raise EvervaultError("Data not defined")
        if role and len(role) > 20:
            raise EvervaultError("Provided Data Role slug is invalid")
        self.__fetch_cage_key(fetch)
        self.shared_key = self.__derive_shared_key(role is not None)

        if self.shared_key is None or type(self.shared_key) != bytes:
            raise EvervaultError("Retrieved key is invalid")

        if type(data) == bytes:
            return self.__encrypt_file(data, role)
        elif type(data) == bytearray:
            return self.__encrypt_file(bytes(data), role)
        elif type(data) == dict or type(data) == list or type(data) == set:
            return self.__traverse_and_encrypt(data, role)
        elif self.__encryptable_data(data):
            return self.__encrypt_string(data, role)
        else:
            raise EvervaultError(f"Cannot encrypt unsupported type {data}")

    def __traverse_and_encrypt(self, data, role):
        if type(data) == list:
            encrypted_list = []
            for idx, item in enumerate(data):
                if not self.__encryptable_data(item):
                    encrypted_list.insert(idx, self.__traverse_and_encrypt(item, role))
                else:
                    encrypted_list.insert(idx, self.__encrypt_string(item, role))
            return encrypted_list
        elif type(data) == dict:
            return self.__encrypt_object(data, role)
        elif type(data) == set:
            return self.__encrypt_set(data, role)
        elif self.__encryptable_data(data):
            return self.__encrypt_string(data, role)
        else:
            raise EvervaultError(f"Cannot encrypt unsupported type {data}")

    def __encrypt_object(self, data, role):
        encrypted_data = {}
        for key, value in data.items():
            if self.__encryptable_data(value):
                encrypted_data[key] = self.__encrypt_string(value, role)
            else:
                encrypted_data[key] = self.__traverse_and_encrypt(value, role)
        return encrypted_data

    def __encrypt_set(self, data, role):
        encrypted_set = set()
        for item in data:
            if self.__encryptable_data(item):
                encrypted_set.add(self.__encrypt_string(item, role))
            else:
                encrypted_set.add(self.__traverse_and_encrypt(item, role))
        return encrypted_set

    def __encrypt_string(self, data, role):
        header_type = map_header_type(data)
        coerced_data = self.__coerce_type(data)
        iv = token_bytes(12)
        aesgcm = AESGCM(self.shared_key)
        has_role = role is not None

        if has_role:
            metadata = self.__generate_metadata(role)
            metadata_offset = struct.pack(
                "<H", len(metadata)
            )  # '<H' specifies 16-bit unsigned little-endian
            payload = metadata_offset + metadata + bytes(coerced_data, "utf8")
        else:
            payload = bytes(coerced_data, "utf8")

        encrypted_bytes = b""
        if self.curve == SECP256K1 and not has_role:
            encrypted_bytes = aesgcm.encrypt(iv, payload, None)
        else:
            encrypted_bytes = aesgcm.encrypt(iv, payload, self.decoded_team_cage_key)

        return self.__format(
            header_type,
            base64.b64encode(iv).decode("utf"),
            base64.b64encode(self.compressed_public_key).decode("utf"),
            base64.b64encode(encrypted_bytes).decode("utf"),
            has_role,
        )

    def __generate_metadata(self, role):
        buffer = bytearray()
        # Binary representation of a fixed map with 2 or 3 items, followed by the key-value pairs
        buffer.append(0x80 | (2 if not role else 3))

        if role:
            # Binary representation for a fixed string of length 2, followed by `dr` (for "data role")
            buffer.extend([0xA2])
            buffer.extend(b"dr")
            # Binary representation for a fixed string of role name length, followed by the role name itself
            buffer.extend([0xA0 | len(role)])
            buffer.extend(role.encode("utf-8"))

        # Binary representation for a fixed string of length 2, followed by `eo` (for "encryption origin")
        buffer.extend([0xA2])
        buffer.extend(b"eo")
        # Binary representation for the integer 7 (Python SDK)
        buffer.extend([7])

        # Binary representation for a fixed string of length 2, followed by `et` (for "encryption timestamp")
        buffer.extend([0xA2])
        buffer.extend(b"et")
        # Binary representation for a 4-byte unsigned integer (uint 32), followed by the epoch time
        buffer.extend([0xCE])
        buffer.extend(struct.pack(">I", int(time.time())))

        return buffer

    def __encrypt_file(self, data, role):
        if len(data) > self.max_file_size_in_bytes:
            raise ExceededMaxFileSizeError(
                f"File size must be less than {self.max_file_size_in_mb}MB"
            )
        iv = token_bytes(12)
        aesgcm = AESGCM(self.shared_key)

        encrypted_bytes = None
        encrypted_metadata = None

        if role is not None:
            metadata = self.__generate_metadata(role)
            encrypted_metadata = aesgcm.encrypt(
                iv, metadata, self.decoded_team_cage_key
            )
            encrypted_bytes = aesgcm.encrypt(iv, data, self.decoded_team_cage_key)
        elif self.curve == SECP256K1:
            encrypted_bytes = aesgcm.encrypt(iv, data, None)
        else:
            encrypted_bytes = aesgcm.encrypt(iv, data, self.decoded_team_cage_key)

        return self.__format_file(
            iv,
            self.compressed_public_key,
            encrypted_metadata,
            encrypted_bytes,
        )

    def __coerce_type(self, data):
        if type(data) == bool:
            return "true" if data else "false"
        elif type(data) == int or type(data) == float:
            return str(data)
        else:
            return data

    def __format(self, header, iv, public_key, encrypted_payload, has_role=False):
        prefix = f":{header}" if header != "string" else ""
        version = self.ev_version_with_metadata if has_role else self.ev_version
        return f"ev:{version}{prefix}:{self.__base_64_remove_padding(iv)}:{self.__base_64_remove_padding(public_key)}:{self.__base_64_remove_padding(encrypted_payload)}:$"

    def __format_file(self, iv, public_key, encrypted_metadata, encrypted_bytes):
        encrypted_file_identifier = bytes(b"\x25\x45\x56\x45\x4e\x43")
        flags = bytes(b"\00")
        if encrypted_metadata is not None:
            version_number = bytes(b"\04") if self.curve == SECP256K1 else bytes(b"\05")
            metadata_offset = len(encrypted_metadata).to_bytes(2, byteorder="little")
            offset_to_data = (55 + 2 + len(encrypted_metadata)).to_bytes(
                2, byteorder="little"
            )
        else:
            version_number = bytes(b"\02") if self.curve == SECP256K1 else bytes(b"\03")
            metadata_offset = bytes(b"")
            encrypted_metadata = bytes(b"")
            offset_to_data = bytes([55, 00])

        file_bytes = (
            encrypted_file_identifier
            + version_number
            + offset_to_data
            + bytes(public_key)
            + bytes(iv)
            + flags
            + metadata_offset
            + bytes(encrypted_metadata)
            + bytes(encrypted_bytes)
        )

        file_crc32 = binascii.crc32(file_bytes)
        crc32_bytes = file_crc32.to_bytes(4, byteorder="little")

        return file_bytes + crc32_bytes

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
            key_name = "ecdhKey" if self.curve == "SECP256K1" else "ecdhP256Key"
            self.decoded_team_cage_key = base64.b64decode(resp[key_name])
            self.team_ecdh_key = EllipticCurvePublicKey.from_encoded_point(
                CURVES[self.curve](), self.decoded_team_cage_key
            )

    def __derive_shared_key(self, has_role=False):
        if self.team_ecdh_key is None:
            raise EvervaultError("Team ECDH key not set in client")
        elif self.shared_key is None:
            return self.__generate_shared_key(has_role)
        else:
            now = int(time.time())
            time_diff = now - self.start_time
            if time_diff > KEY_INTERVAL:
                self.start_time = now
                return self.__generate_shared_key(has_role)
            return self.shared_key

    def __generate_shared_key(self, has_role):
        generated_key = ec.generate_private_key(CURVES[self.curve])
        public_key = generated_key.public_key()
        self.compressed_public_key = public_key.public_bytes(
            Encoding.X962, PublicFormat.CompressedPoint
        )
        self.uncompressed_public_key = public_key.public_bytes(
            Encoding.X962, PublicFormat.UncompressedPoint
        )
        shared_key = generated_key.exchange(ec.ECDH(), self.team_ecdh_key)

        if self.curve == SECP256K1 and not has_role:
            return shared_key

        if self.curve == SECP256R1:
            public_key = P256PublicKey(self.uncompressed_public_key.hex()).encode()
        else:
            public_key = KoblitzPublicKey(self.uncompressed_public_key.hex()).encode()

        # Perform KDF
        hash_input = shared_key + b"\x00\x00\x00\x01" + public_key
        digest = hashes.Hash(hashes.SHA256())
        digest.update(hash_input)
        return digest.finalize()
