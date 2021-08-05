from evervault.errors.evervault_errors import UnknownEncryptType
import unittest
import requests_mock
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import evervault

class TestEvervault(unittest.TestCase):
    def setUp(self):
        self.evervault = evervault
        self.evervault.init("testing", intercept=False)
        self.public_key = self.build_keys()

    def tearDown(self):
        self.evervault = None

    @requests_mock.Mocker()
    def test_encrypting_number_generates_ev_number_type(self, mock_request):
        self.mock_fetch_cage_key(mock_request)
        input = 1
        encrypted_input = self.evervault.encrypt(input)
        assert self.__is_evervault_string(encrypted_input, "number") == True

    @requests_mock.Mocker()
    def test_encrypting_boolean_generates_ev_boolean_type(self, mock_request):
        self.mock_fetch_cage_key(mock_request)
        input = False
        encrypted_input = self.evervault.encrypt(input)
        assert self.__is_evervault_string(encrypted_input, "boolean") == True

    @requests_mock.Mocker()
    def test_encrypting_string_generates_ev_string_type(self, mock_request):
        self.mock_fetch_cage_key(mock_request)
        input = "string"
        encrypted_input = self.evervault.encrypt(input)
        assert self.__is_evervault_string(encrypted_input, "string") == True

    @requests_mock.Mocker()
    def test_encrypt_sets(self, mock_request):
        self.mock_fetch_cage_key(mock_request)
        level_1_set = set(['a', True, 3])
        level_1_set_encrypted = self.evervault.encrypt(level_1_set)
        assert len(level_1_set_encrypted) == 3
        for item in level_1_set_encrypted:
            assert self.__is_evervault_string_format(item)
    
    @requests_mock.Mocker()
    def test_encrypt_lists_of_various_types(self, mock_request):
        self.mock_fetch_cage_key(mock_request)
        level_1_list = ['a', True, 3]
        level_1_list_encrypted = self.evervault.encrypt(level_1_list)
        for item in level_1_list_encrypted:
            assert self.__is_evervault_string_format(item)


        level_2_list = ['a', False, 4.0, ['b', 2], set(["x", "b"])]
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
            "dict": {
                "subname": "subtestname",
                "subnumber": 2
            }
        }
        encrypted_data = self.evervault.encrypt(test_payload)
        assert encrypted_data != {"name": "testname"}
        assert "name" in encrypted_data
        assert "dict" in encrypted_data
        assert type(encrypted_data["dict"]) == dict
        assert self.__is_evervault_string(encrypted_data["dict"]["subnumber"], "number")
    
    @requests_mock.Mocker()
    def test_encrypt_with_unsupported_type_throws_exception(self, mock_request):
        self.mock_fetch_cage_key(mock_request)
        class MyTestClass:
            x = 5

        test_instance = MyTestClass()
        level_1_list = ['a', test_instance, 3]
        level_2_list = ['a', ['a', test_instance]]
        
        self.assertRaises(UnknownEncryptType, self.evervault.encrypt, test_instance)
        self.assertRaises(UnknownEncryptType, self.evervault.encrypt, level_1_list)
        self.assertRaises(UnknownEncryptType, self.evervault.encrypt, level_2_list)

    @requests_mock.Mocker()
    def test_run(self, mock_request):
        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"result": "there was an attempt"},
            request_headers={"Api-Key": "testing"},
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
            request_headers={ "Api-Key": "testing", "x-version-id": "2", "x-async": "true" },
        )
        resp = self.evervault.run("testing-cage", {"name": "testing"}, {"async": True, "version": 2})
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
            request_headers={"Api-Key": "testing"},
        )
        resp = self.evervault.encrypt_and_run("testing-cage", {"name": "testing"})
        assert request.called
        assert resp["result"] == "there was an attempt"
        assert request.last_request.json() != {"name": "testing"}
        assert "name" in request.last_request.json()

    @requests_mock.Mocker()
    def test_encrypt_and_run_with_options(self, mock_request):
        request = mock_request.post(
            "https://run.evervault.com/testing-cage",
            json={"status": "queued"},
            request_headers={ "Api-Key": "testing", "x-version-id": "2", "x-async": "true" },
        )
        resp = self.evervault.encrypt_and_run("testing-cage", {"name": "testing"}, {"async": True, "version": 2})
        assert request.called
        assert resp["status"] == "queued"
        assert request.last_request.json() != {"name": "testing"}
        assert request.last_request.headers["x-async"] == "true"
        assert request.last_request.headers["x-version-id"] == "2"

    def mock_fetch_cage_key(self, mock_request):
        mock_request.get(
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

    def __is_evervault_string_format(self, data):
        parts = data.split(":")
        if len(parts) < 5:
            return False
        if parts[1] == "number" or parts[1] == "boolean":
            return len(parts) == 6
        return True    