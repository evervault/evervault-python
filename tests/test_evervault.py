from evervault.errors.evervault_errors import (
    UnknownEncryptType,
    ForbiddenIPError,
    AuthenticationError,
    ExceededMaxFileSizeError,
    UndefinedDataError,
)
import unittest
from evervault.http.outboundrelayconfig import RelayOutboundConfig
import requests_mock
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import evervault
import os
import requests
import importlib
import binascii
import datetime


class TestEvervault(unittest.TestCase):
    CURVES = {"SECP256K1": ec.SECP256K1, "SECP256R1": ec.SECP256R1}

    def setUp(self, curve="SECP256K1"):
        self.curve = curve
        importlib.reload(evervault)
        self.evervault = evervault
        self.evervault.init("testAppUuid", "testing", curve=curve)
        self.public_key = self.build_keys()

    def tearDown(self):
        self.evervault.ev_client = None
        self.evervault = None
        self.__del_env_var("EV_API_URL")
        self.__del_env_var("EV_CAGE_RUN_URL")
        self.__del_env_var("EV_TUNNEL_HOSTNAME")
        self.__del_env_var("EV_CERT_HOSTNAME")
        self.__del_env_var("EV_MAX_FILE_SIZE_IN_MB")

    @requests_mock.Mocker()
    def test_encrypting_number_generates_ev_number_type(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        input = 1
        encrypted_input = self.evervault.encrypt(input)
        assert self.__is_evervault_string(encrypted_input, "number")

    @requests_mock.Mocker()
    def test_encrypting_boolean_generates_ev_boolean_type(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        input = False
        encrypted_input = self.evervault.encrypt(input)
        assert self.__is_evervault_string(encrypted_input, "boolean")

    @requests_mock.Mocker()
    def test_encrypting_string_generates_ev_string_type(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        input = "string"
        encrypted_input = self.evervault.encrypt(input)
        assert self.__is_evervault_string(encrypted_input, "string")

    @requests_mock.Mocker()
    def test_encrypt_sets(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        level_1_set = set(["a", True, 3])
        level_1_set_encrypted = self.evervault.encrypt(level_1_set)
        assert len(level_1_set_encrypted) == 3
        for item in level_1_set_encrypted:
            assert self.__is_evervault_string_format(item)

    @requests_mock.Mocker()
    def test_encrypt_lists_of_various_types(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        level_1_list = ["a", True, 3]
        level_1_list_encrypted = self.evervault.encrypt(level_1_list)
        for item in level_1_list_encrypted:
            assert self.__is_evervault_string_format(item)

        level_2_list = ["a", False, 4.0, ["b", 2], set(["x", "b"])]
        level_2_list_encrypted = self.evervault.encrypt(level_2_list)
        for item in level_2_list_encrypted:
            if type(item) == list or type(item) == set:
                for sub_item in item:
                    assert self.__is_evervault_string_format(sub_item)
            else:
                assert self.__is_evervault_string_format(item)

    @requests_mock.Mocker()
    def test_encrypt_dicts(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        test_payload = {
            "name": "testname",
            "age": 20,
            "array": ["team1", 1],
            "dict": {"subname": "subtestname", "subnumber": 2},
        }
        encrypted_data = self.evervault.encrypt(test_payload)
        assert encrypted_data != {"name": "testname"}
        assert "name" in encrypted_data
        assert "dict" in encrypted_data
        assert type(encrypted_data["dict"]) == dict
        assert self.__is_evervault_string(encrypted_data["dict"]["subnumber"], "number")

    @requests_mock.Mocker()
    def test_encrypt_files(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        test_payload = b"\00\01\03"
        encrypted_data = self.evervault.encrypt(test_payload)
        assert self.__is_evervault_file(encrypted_data)

        # Check that curve is set correctly
        assert encrypted_data[6:7] == b"\02"

        # Check that offset to data is set correctly
        assert encrypted_data[7:9] == bytes([55, 00])

        # Re-calculate the crc32 and ensure it matches
        crc32 = binascii.crc32(encrypted_data[:-4])
        assert encrypted_data[-4:] == crc32.to_bytes(4, byteorder="little")

    @requests_mock.Mocker()
    def test_encrypt_files_with_bytearray(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        test_payload = bytearray(10)
        encrypted_data = self.evervault.encrypt(test_payload)
        assert self.__is_evervault_file(encrypted_data)

        # Check that curve is set correctly
        assert encrypted_data[6:7] == b"\02"

        # Check that offset to data is set correctly
        assert encrypted_data[7:9] == bytes([55, 00])

    @requests_mock.Mocker()
    def test_encrypt_large_files_throws_exception(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        test_payload = bytes(bytearray(26 * 1024 * 1024))
        self.assertRaises(
            ExceededMaxFileSizeError, self.evervault.encrypt, test_payload
        )

    @requests_mock.Mocker()
    def test_encrypt_large_files_succeeds_with_max_size_override(self, mock_request):
        os.environ["EV_MAX_FILE_SIZE_IN_MB"] = "30"
        self.setUp()
        self.mock_fetch_cage_key(mock_request)

        test_payload = bytes(bytearray(26 * 1024 * 1024))
        encrypted_data = self.evervault.encrypt(test_payload)
        assert self.__is_evervault_file(encrypted_data)

        # Check that curve is set correctly
        assert encrypted_data[6:7] == b"\02"

        # Check that offset to data is set correctly
        assert encrypted_data[7:9] == bytes([55, 00])

    @requests_mock.Mocker()
    def test_encrypt_with_unsupported_type_throws_exception(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        class MyTestClass:
            x = 5

        test_instance = MyTestClass()
        level_1_list = ["a", test_instance, 3]
        level_2_list = ["a", ["a", test_instance]]

        self.assertRaises(UnknownEncryptType, self.evervault.encrypt, test_instance)
        self.assertRaises(UnknownEncryptType, self.evervault.encrypt, level_1_list)
        self.assertRaises(UnknownEncryptType, self.evervault.encrypt, level_2_list)

    @requests_mock.Mocker()
    def test_create_decrypt_token_without_expiry(self, mock_request):
        request = mock_request.post(
            "https://api.evervault.com/client-side-tokens",
            json={"token": "token123", "expiry": 1234567890},
            request_headers={
                "Authorization": "Basic dGVzdEFwcFV1aWQ6dGVzdGluZw==",
                "Content-Type": "application/json",
            },
        )
        resp = self.evervault.create_client_side_decrypt_token(
            {"data": "ev:abc123"}, None
        )
        assert request.called
        assert resp == {"token": "token123", "expiry": 1234567890}
        assert request.last_request.json() == {
            "payload": {"data": "ev:abc123"},
            "expiry": None,
            "action": "api:decrypt",
        }

    @requests_mock.Mocker()
    def test_create_decrypt_token_with_expiry(self, mock_request):
        request = mock_request.post(
            "https://api.evervault.com/client-side-tokens",
            json={"token": "token123", "expiry": 1234567890},
            request_headers={
                "Authorization": "Basic dGVzdEFwcFV1aWQ6dGVzdGluZw==",
                "Content-Type": "application/json",
            },
        )
        now = datetime.datetime.now()
        expected_datetime_in_request = int(now.timestamp() * 1000)
        resp = self.evervault.create_client_side_decrypt_token(
            {"data": "ev:abc123"}, now
        )
        assert request.called
        assert resp == {"token": "token123", "expiry": 1234567890}
        assert request.last_request.json() == {
            "payload": {"data": "ev:abc123"},
            "expiry": expected_datetime_in_request,
            "action": "api:decrypt",
        }

    @requests_mock.Mocker()
    def test_create_decrypt_token_without_payload_throws(self, mock_request):
        self.assertRaises(
            UndefinedDataError,
            self.evervault.create_client_side_decrypt_token,
            None,
            None,
        )

    @requests_mock.Mocker()
    def test_decrypt_dict(self, mock_request):
        request = mock_request.post(
            "https://api.evervault.com/decrypt",
            json={"data": {"encrypted": "testString"}},
            request_headers={
                "Authorization": "Basic dGVzdEFwcFV1aWQ6dGVzdGluZw==",
                "Content-Type": "application/json",
            },
        )
        resp = self.evervault.decrypt({"encrypted": "ev:abc123"})
        assert request.called
        assert resp["encrypted"] == "testString"
        assert request.last_request.json() == {"data": {"encrypted": "ev:abc123"}}

    @requests_mock.Mocker()
    def test_decrypt_str(self, mock_request):
        request = mock_request.post(
            "https://api.evervault.com/decrypt",
            json={"data": "testString"},
            request_headers={
                "Authorization": "Basic dGVzdEFwcFV1aWQ6dGVzdGluZw==",
                "Content-Type": "application/json",
            },
        )
        resp = self.evervault.decrypt("ev:abc123")
        assert request.called
        assert resp == "testString"
        assert request.last_request.json() == {"data": "ev:abc123"}

    @requests_mock.Mocker()
    def test_decrypt_bool(self, mock_request):
        request = mock_request.post(
            "https://api.evervault.com/decrypt",
            json={"data": True},
            request_headers={
                "Authorization": "Basic dGVzdEFwcFV1aWQ6dGVzdGluZw==",
                "Content-Type": "application/json",
            },
        )
        resp = self.evervault.decrypt("ev:abc123")
        assert request.called
        assert resp
        assert request.last_request.json() == {"data": "ev:abc123"}

    @requests_mock.Mocker()
    def test_run(self, mock_request):
        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"result": "there was an attempt"},
            request_headers={
                "Api-Key": "testing",
            },
        )
        resp = self.evervault.run("testing-cage", {"name": "testing"})
        assert request.called
        assert resp["result"] == "there was an attempt"
        assert request.last_request.json() == {"name": "testing"}

    @requests_mock.Mocker()
    def test_run_with_options(self, mock_request):
        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"status": "queued"},
            request_headers={
                "Api-Key": "testing",
                "x-version-id": "2",
                "x-async": "true",
            },
        )
        resp = self.evervault.run(
            "testing-cage", {"name": "testing"}, {"async": True, "version": 2}
        )
        assert request.called
        assert resp["status"] == "queued"
        assert request.last_request.json() == {"name": "testing"}
        assert request.last_request.headers["x-async"] == "true"
        assert request.last_request.headers["x-version-id"] == "2"

    @requests_mock.Mocker()
    def test_encrypt_and_run(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"result": "there was an attempt"},
            request_headers={
                "Api-Key": "testing",
            },
        )
        resp = self.evervault.encrypt_and_run("testing-cage", {"name": "testing"})
        assert request.called
        assert resp["result"] == "there was an attempt"
        assert request.last_request.json() != {"name": "testing"}
        assert "name" in request.last_request.json()

    @requests_mock.Mocker()
    def test_encrypt_and_forbidden_ip_run(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"error": "An error occurred"},
            request_headers={
                "Api-Key": "testing",
            },
            headers={"x-evervault-error-code": "forbidden-ip-error"},
            status_code=403,
        )
        self.assertRaises(
            ForbiddenIPError,
            self.evervault.encrypt_and_run,
            "testing-cage",
            {"name": "testing"},
        )
        assert request.called

    @requests_mock.Mocker()
    def test_encrypt_and_forbidden_run(self, mock_request):
        self.mock_fetch_cage_key(mock_request)

        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"error": "An error occurred"},
            request_headers={
                "Api-Key": "testing",
            },
            headers={},
            status_code=403,
        )
        self.assertRaises(
            AuthenticationError,
            self.evervault.encrypt_and_run,
            "testing-cage",
            {"name": "testing"},
        )
        assert request.called

    @requests_mock.Mocker()
    def test_encrypt_and_run_with_options(self, mock_request):
        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"status": "queued"},
            request_headers={
                "Api-Key": "testing",
                "x-version-id": "2",
                "x-async": "true",
            },
        )
        self.mock_fetch_cage_key(mock_request)

        resp = self.evervault.encrypt_and_run(
            "testing-cage", {"name": "testing"}, {"async": True, "version": 2}
        )
        assert request.called
        assert resp["status"] == "queued"
        assert request.last_request.json() != {"name": "testing"}
        assert request.last_request.headers["x-async"] == "true"
        assert request.last_request.headers["x-version-id"] == "2"

    @requests_mock.Mocker()
    def test_endpoint_overrides(self, mock_request):
        mock_request.get("https://ca.evervault.com", {})
        mock_request.get("https://ca.url.com", {})

        # Test default values
        self.evervault.init("testAppUuid", "testing")
        assert self.evervault.ev_client.base_url == "https://api.evervault.com/"
        assert self.evervault.ev_client.base_run_url == "https://run.evervault.com/"
        assert self.evervault.ev_client.relay_url == "https://relay.evervault.com:443"
        assert self.evervault.ev_client.ca_host == "https://ca.evervault.com"

        # Set overrides
        os.environ["EV_API_URL"] = "https://custom.url.com"
        os.environ["EV_CAGE_RUN_URL"] = "https://custom.run.url.com"
        os.environ["EV_TUNNEL_HOSTNAME"] = "https://custom.tunnel.url.com"
        os.environ["EV_CERT_HOSTNAME"] = "https://ca.url.com"

        # Force client to reinit
        self.evervault.ev_client = None
        self.evervault.init("testAppUuid", "testing")

        assert self.evervault.ev_client.base_url == "https://custom.url.com"
        assert self.evervault.ev_client.base_run_url == "https://custom.run.url.com"
        assert self.evervault.ev_client.relay_url == "https://custom.tunnel.url.com"
        assert self.evervault.ev_client.ca_host == "https://ca.url.com"

    @requests_mock.Mocker()
    def test_create_run_token(self, mock_request):
        request = mock_request.post(
            "https://api.evervault.com/v2/functions/testing-cage/run-token",
            json={"result": "there was an attempt"},
            request_headers={
                "Api-Key": "testing",
            },
        )
        resp = self.evervault.create_run_token("testing-cage", {"name": "testing"})
        assert request.called
        assert resp["result"] == "there was an attempt"
        assert request.last_request.json() == {"name": "testing"}

    ################################################################
    #                                                              #
    # TESTS USING P256 CURVE - SETUP IS CALLED AGAIN ON EACH TEST  #
    #                                                              #
    ################################################################

    @requests_mock.Mocker()
    def test_p256_encrypting_number_generates_ev_number_type(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)
        self.mock_fetch_cage_key(mock_request)

        input = 1
        encrypted_input = self.evervault.encrypt(input)
        assert self.__is_evervault_string(encrypted_input, "number")

    @requests_mock.Mocker()
    def test_p256_encrypting_boolean_generates_ev_boolean_type(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)
        self.mock_fetch_cage_key(mock_request)

        input = False
        encrypted_input = self.evervault.encrypt(input)
        assert self.__is_evervault_string(encrypted_input, "boolean")

    @requests_mock.Mocker()
    def test_p256_encrypting_string_generates_ev_string_type(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)
        self.mock_fetch_cage_key(mock_request)

        input = "string"
        encrypted_input = self.evervault.encrypt(input)
        assert self.__is_evervault_string(encrypted_input, "string")

    @requests_mock.Mocker()
    def test_p256_encrypt_sets(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)

        self.mock_fetch_cage_key(mock_request)

        level_1_set = set(["a", True, 3])
        level_1_set_encrypted = self.evervault.encrypt(level_1_set)
        assert len(level_1_set_encrypted) == 3
        for item in level_1_set_encrypted:
            assert self.__is_evervault_string_format(item)

    @requests_mock.Mocker()
    def test_p256_encrypt_lists_of_various_types(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)

        self.mock_fetch_cage_key(mock_request)

        level_1_list = ["a", True, 3]
        level_1_list_encrypted = self.evervault.encrypt(level_1_list)
        for item in level_1_list_encrypted:
            assert self.__is_evervault_string_format(item)

        level_2_list = ["a", False, 4.0, ["b", 2], set(["x", "b"])]
        level_2_list_encrypted = self.evervault.encrypt(level_2_list)
        for item in level_2_list_encrypted:
            if type(item) == list or type(item) == set:
                for sub_item in item:
                    assert self.__is_evervault_string_format(sub_item)
            else:
                assert self.__is_evervault_string_format(item)

    @requests_mock.Mocker()
    def test_p256_encrypt_dicts(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)

        self.mock_fetch_cage_key(mock_request)

        test_payload = {
            "name": "testname",
            "age": 20,
            "array": ["team1", 1],
            "dict": {"subname": "subtestname", "subnumber": 2},
        }
        encrypted_data = self.evervault.encrypt(test_payload)
        assert encrypted_data != {"name": "testname"}
        assert "name" in encrypted_data
        assert "dict" in encrypted_data
        assert type(encrypted_data["dict"]) == dict
        assert self.__is_evervault_string(encrypted_data["dict"]["subnumber"], "number")

    @requests_mock.Mocker()
    def test_p256_encrypt_files(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)
        self.mock_fetch_cage_key(mock_request)

        test_payload = b"\00\01\03"
        encrypted_data = self.evervault.encrypt(test_payload)
        assert self.__is_evervault_file(encrypted_data)

        # Check that curve is set correctly
        assert encrypted_data[6:7] == b"\03"

        # Check that offset to data is set correctly
        assert encrypted_data[7:9] == bytes([55, 00])

        # Re-calculate the crc32 and ensure it matches
        crc32 = binascii.crc32(encrypted_data[:-4])
        assert encrypted_data[-4:] == crc32.to_bytes(4, byteorder="little")

    @requests_mock.Mocker()
    def test_p256_encrypt_with_unsupported_type_throws_exception(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)

        self.mock_fetch_cage_key(mock_request)

        class MyTestClass:
            x = 5

        test_instance = MyTestClass()
        level_1_list = ["a", test_instance, 3]
        level_2_list = ["a", ["a", test_instance]]

        self.assertRaises(UnknownEncryptType, self.evervault.encrypt, test_instance)
        self.assertRaises(UnknownEncryptType, self.evervault.encrypt, level_1_list)
        self.assertRaises(UnknownEncryptType, self.evervault.encrypt, level_2_list)

    @requests_mock.Mocker()
    def test_p256_run(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)

        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"result": "there was an attempt"},
            request_headers={
                "Api-Key": "testing",
            },
        )
        resp = self.evervault.run("testing-cage", {"name": "testing"})
        assert request.called
        assert resp["result"] == "there was an attempt"
        assert request.last_request.json() == {"name": "testing"}

    @requests_mock.Mocker()
    def test_p256_run_with_options(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)

        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"status": "queued"},
            request_headers={
                "Api-Key": "testing",
                "x-version-id": "2",
                "x-async": "true",
            },
        )
        resp = self.evervault.run(
            "testing-cage", {"name": "testing"}, {"async": True, "version": 2}
        )
        assert request.called
        assert resp["status"] == "queued"
        assert request.last_request.json() == {"name": "testing"}
        assert request.last_request.headers["x-async"] == "true"
        assert request.last_request.headers["x-version-id"] == "2"

    @requests_mock.Mocker()
    def test_p256_encrypt_and_run(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)

        self.mock_fetch_cage_key(mock_request)

        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"result": "there was an attempt"},
            request_headers={
                "Api-Key": "testing",
            },
        )
        resp = self.evervault.encrypt_and_run("testing-cage", {"name": "testing"})
        assert request.called
        assert resp["result"] == "there was an attempt"
        assert request.last_request.json() != {"name": "testing"}
        assert "name" in request.last_request.json()

    @requests_mock.Mocker()
    def test_p256_encrypt_and_run_with_options(self, mock_request):
        self.setUp(evervault.Curves.SECP256R1)

        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"status": "queued"},
            request_headers={
                "Api-Key": "testing",
                "x-version-id": "2",
                "x-async": "true",
            },
        )
        self.mock_fetch_cage_key(mock_request)

        resp = self.evervault.encrypt_and_run(
            "testing-cage", {"name": "testing"}, {"async": True, "version": 2}
        )
        assert request.called
        assert resp["status"] == "queued"
        assert request.last_request.json() != {"name": "testing"}
        assert request.last_request.headers["x-async"] == "true"
        assert request.last_request.headers["x-version-id"] == "2"

    @requests_mock.Mocker()
    def test_run_with_decryption_domain_constructor(self, mock_request):
        self.__mock_cert(mock_request)

        evervault.init("testAppUuid", "testing", decryption_domains=["test2.com"])

        request = mock_request.get("https://test2.com/hello")
        requests.get("https://test2.com/hello")
        assert request.last_request.headers["Proxy-Authorization"] == "testing"

        self.__reinit_client()

    @requests_mock.Mocker()
    def test_run_with_decryption_domain(self, mock_request):
        self.__mock_cert(mock_request)

        evervault.init("testAppUuid", "testing")
        evervault.enable_outbound_relay(decryption_domains=["test2.com"])

        request = mock_request.get("https://test2.com/hello")
        requests.get("https://test2.com/hello")
        assert request.last_request.headers["Proxy-Authorization"] == "testing"

        self.__reinit_client()

    @requests_mock.Mocker()
    def test_run_with_wildcard_decryption_domain(self, mock_request):
        self.__mock_cert(mock_request)

        evervault.init("testAppUuid", "testing", decryption_domains=["*.test2.com"])

        request = mock_request.get("https://test.test2.com/hello")
        requests.get("https://test.test2.com/hello")
        assert request.last_request.headers["Proxy-Authorization"] == "testing"

        self.__reinit_client()

    @requests_mock.Mocker()
    def test_run_with_decryption_domain_set_and_other_domain_requested_constructor(
        self, mock_request
    ):
        self.__mock_cert(mock_request)

        evervault.init("testAppUuid", "testing", decryption_domains=["test-other.com"])

        request = mock_request.get("https://www.test2.com/hello")
        requests.get("https://www.test2.com/hello")

        self.assertRaises(
            KeyError, lambda: request.last_request.headers["Proxy-Authorization"]
        )

        self.__reinit_client()

    @requests_mock.Mocker()
    def test_run_with_decryption_domain_set_and_other_domain_requested(
        self, mock_request
    ):
        self.__mock_cert(mock_request)

        evervault.init("testAppUuid", "testing")
        evervault.enable_outbound_relay(decryption_domains=["test-other.com"])

        request = mock_request.get("https://www.test2.com/hello")
        requests.get("https://www.test2.com/hello")

        self.assertRaises(
            KeyError, lambda: request.last_request.headers["Proxy-Authorization"]
        )

        self.__reinit_client()

    @requests_mock.Mocker()
    def test_run_with_relay_outbound_enabled_constructor(self, mock_request):
        self.__mock_cert(mock_request)
        self.__mock_relay_outbound_config(mock_request)

        request = mock_request.get("https://test-one.destinations.com/hello")
        evervault.init("testAppUuid", "testing", enable_outbound_relay=True)
        requests.get("https://test-one.destinations.com/hello")

        assert request.last_request.headers["Proxy-Authorization"] == "testing"
        self.__reinit_client()

    @requests_mock.Mocker()
    def test_run_with_relay_outbound_enabled(self, mock_request):
        self.__mock_cert(mock_request)
        self.__mock_relay_outbound_config(mock_request)

        request = mock_request.get("https://test-one.destinations.com/hello")
        evervault.init("testAppUuid", "testing")
        evervault.enable_outbound_relay()
        requests.get("https://test-one.destinations.com/hello")

        assert request.last_request.headers["Proxy-Authorization"] == "testing"
        self.__reinit_client()

    def mock_fetch_cage_key(self, mock_request):
        mock_request.get(
            "https://api.evervault.com/cages/key",
            json={
                "ecdhKey": self.public_key.decode("utf8"),
                "ecdhP256Key": self.public_key.decode("utf8"),
            },
        )

    def mock_metrics_endpoint(self, mock_request):
        mock_request.post(
            "https://api.evervault.com/metrics/sdkEncryptions?sdk=python&numEncryptions=1",
            text="OK",
        )

    def build_keys(self):
        ecdh_private_key = ec.generate_private_key(TestEvervault.CURVES[self.curve]())

        public_key = ecdh_private_key.public_key()
        key = public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.CompressedPoint,
        )

        return base64.b64encode(key)

    def __del_env_var(self, var):
        if var in os.environ:
            os.environ.pop(var)

    def __is_evervault_string(self, data, type):
        parts = data.split(":")
        if len(parts) < 6:
            return False
        elif type == "string":
            return len(parts) == 6
        elif type != "string" and not len(parts) == 7:
            return False
        elif type != parts[2]:
            return False
        return True

    def __is_evervault_file(self, data):
        return data[0:6] == bytes(b"\x25\x45\x56\x45\x4e\x43")

    def __is_evervault_string_format(self, data):
        parts = data.split(":")
        if len(parts) < 5:
            return False
        if parts[1] == "number" or parts[1] == "boolean":
            return len(parts) == 6
        return True

    def __reinit_client(self):
        if self.evervault.ev_client.cert.relay_outbound_config is not None:
            self.evervault.ev_client.cert.relay_outbound_config.clear_cache()
        self.evervault.ev_client = None
        self.evervault.init("testAppUuid", "testing")
        RelayOutboundConfig.clear_cache()
        RelayOutboundConfig.disable_polling()

    def __mock_cert(self, mock_request):
        mock_request.get(
            "https://ca.evervault.com",
            text="-----BEGIN CERTIFICATE-----\n"
            "MIIDgzCCAmugAwIBAgIUEL9SyDnNVvLXq8opJM2nrLgoFpgwDQYJKoZIhvcNAQEL\n"
            "BQAwUTELMAkGA1UEBhMCSUUxEzARBgNVBAgMCkR1YmxpbiBDby4xDzANBgNVBAcM\n"
            "BlN3b3JkczEcMBoGA1UECgwTRGVmYXVsdCBDb21wYW55IEx0ZDAeFw0wODEyMjQw\n"
            "ODE2MDhaFw0wOTAxMDMwODE2MDhaMFExCzAJBgNVBAYTAklFMRMwEQYDVQQIDApE\n"
            "dWJsaW4gQ28uMQ8wDQYDVQQHDAZTd29yZHMxHDAaBgNVBAoME0RlZmF1bHQgQ29t\n"
            "cGFueSBMdGQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDoCOTOgSCf\n"
            "wsbSefJQwu51Krbz9jTFic4tbaM3B2BROtqAxDHdDIE5HQ1nhuZ06XyL9aLjDI2J\n"
            "9WOWTkN/iXh0XcUJmIlBgErs7EQbIeXjO6pTa4S+tjBtbnVF8Aaz2Bj2AuD4O9VJ\n"
            "AP8HmS654dOWjhqnEsRbv9IJo+ccvy699afWsoYePILZOJmoeiGXvQ/ZTbj4cYDx\n"
            "CxZOkYK5HK3Zv0VfK5B+hsz3buuijkPdIG46o6DAE2nmNjrTxaz1/BuiWDEvC8RK\n"
            "8NOY92LoiDMSxWVP2/UDDsKqWlGS7KmpdmIx1ndH6eYyYJut5xvLE7vlkr6s96O2\n"
            "AN5EQ28oQNNHAgMBAAGjUzBRMB0GA1UdDgQWBBQDqdmoCx8KJdc6giTS69YtlAsc\n"
            "vDAfBgNVHSMEGDAWgBQDqdmoCx8KJdc6giTS69YtlAscvDAPBgNVHRMBAf8EBTAD\n"
            "AQH/MA0GCSqGSIb3DQEBCwUAA4IBAQAiBFVUOI07QOVbMAMWNk5D3L308wx6avqI\n"
            "4FY6aSfmIGp898ab6L3XOrz54ztOuIyjdUaQ8/U1yFGxTBe66zPKDyorHm0a+kNp\n"
            "2h5luIXRsm6IZrpGblO7CD+ZzYZ04qWkHgugLSieKhO3GVKObdkdfnJIf2O5KW7j\n"
            "PulHfTQ3MNd/qXhOBNUXgI0rcWeI5xGKzAVWRoiAcAHU9UmNrunVg9CQMh0i6nYA\n"
            "i7xFTBvY5QrZGK/Y6mEAdGCRoGusOputz1MHn721sIyH5DtCAMXdJ/s94Ki7m557\n"
            "qLZdvkgx0KBRnP/JPZ55VgjZ8ipH9+SGxsZeTg9sX6nw+x/Plncz\n"
            "-----END CERTIFICATE-----\n",
        )

    def __mock_relay_outbound_config(self, mock_request):
        mock_request.get(
            "https://api.evervault.com/v2/relay-outbound",
            headers={"X-Poll-Interval": "5"},
            json={
                "appUuid": "app_33b88ca7da01",
                "teamUuid": "2ef8d35ce661",
                "strictMode": True,
                "outboundDestinations": {
                    "test-one.destinations.com": {
                        "id": 144,
                        "appUuid": "app_33b88ca7da01",
                        "createdAt": "2022-10-05T08: 36: 35.681Z",
                        "updatedAt": "2022-10-05T08: 36: 35.681Z",
                        "deletedAt": None,
                        "routeSpecificFieldsToEncrypt": [],
                        "deterministicFieldsToEncrypt": [],
                        "encryptEmptyStrings": True,
                        "curve": "secp256k1",
                        "uuid": "outbound_destination_9733a04135f1",
                        "destinationDomain": "test-one.destinations.com",
                    },
                    "test-two.destinations.com": {
                        "id": 20,
                        "appUuid": "app_33b88ca7da01",
                        "createdAt": "2022-07-20T16: 02: 36.601Z",
                        "updatedAt": "2022-10-05T12: 40: 44.511Z",
                        "deletedAt": None,
                        "routeSpecificFieldsToEncrypt": [],
                        "deterministicFieldsToEncrypt": [],
                        "encryptEmptyStrings": True,
                        "curve": "secp256k1",
                        "uuid": "outbound_destination_e7f791332c51",
                        "destinationDomain": "test-two.destinations.com",
                    },
                },
            },
        )
