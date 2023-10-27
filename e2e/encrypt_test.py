from evervault.errors.evervault_errors import EvervaultError
from .e2e_test_case import EndToEndTestCase
from parameterized import parameterized
import re

CURVES = ["SECP256K1", "SECP256R1"]
ROLES_AND_SUCCESSES = [
    {"role": "permit-all", "decryption_should_succeed": True},
    {"role": "forbid-all", "decryption_should_succeed": False},
    {"role": None, "decryption_should_succeed": True},
]
metadata_string_regex = r"((ev(:|%3A))(debug(:|%3A))?((QlJV|TENZ|)(:|%3A))?((number|boolean|string)(:|%3A))?(([A-z0-9+\/=%]+)(:|%3A)){3}(\$|%24))|(((eyJ[A-z0-9+=.]+){2})([\w]{8}(-[\w]{4}){3}-[\w]{12}))"


def check_object_has_strings_with_correct_versions(value):
    if isinstance(value, list):
        for arr_val in value:
            if not re.match(metadata_string_regex, arr_val):
                return False
        return True
    else:
        return re.match(metadata_string_regex, value)


def generate_combinations(list1, list2):
    return [(x, y) for x in list1 for y in list2]


class EncryptTest(EndToEndTestCase):
    @parameterized.expand(generate_combinations(CURVES, ROLES_AND_SUCCESSES))
    def test_encrypt_str(self, curve, role_and_success):
        self.setUp(curve)
        role = role_and_success["role"]
        decryption_should_succeed = role_and_success["decryption_should_succeed"]
        string = "hello world"
        try:
            encrypted = self.evervault.encrypt(string, role)
            if role is not None:
                assert check_object_has_strings_with_correct_versions(encrypted)
            decrypted = self.evervault.decrypt(encrypted)
            assert decryption_should_succeed
            assert string == decrypted
        except EvervaultError as e:
            assert not decryption_should_succeed
            assert (
                str(e)
                == "Decryption of the provided data is restricted by your current policies. Please check and modify your policies, if needed, to enable decryption in this context."
            )

    @parameterized.expand(generate_combinations(CURVES, ROLES_AND_SUCCESSES))
    def test_encrypt_bool_true(self, curve, role_and_success):
        self.setUp(curve)
        role = role_and_success["role"]
        decryption_should_succeed = role_and_success["decryption_should_succeed"]
        boolean = True

        try:
            encrypted = self.evervault.encrypt(boolean, role)
            if role is not None:
                assert check_object_has_strings_with_correct_versions(encrypted)
            decrypted = self.evervault.decrypt(encrypted)
            assert decryption_should_succeed
            assert boolean == decrypted
        except EvervaultError as e:
            assert not decryption_should_succeed
            assert (
                str(e)
                == "Decryption of the provided data is restricted by your current policies. Please check and modify your policies, if needed, to enable decryption in this context."
            )

    @parameterized.expand(generate_combinations(CURVES, ROLES_AND_SUCCESSES))
    def test_encrypt_bool_false(self, curve, role_and_success):
        self.setUp(curve)
        role = role_and_success["role"]
        decryption_should_succeed = role_and_success["decryption_should_succeed"]
        boolean = False

        try:
            encrypted = self.evervault.encrypt(boolean, role)
            if role is not None:
                assert check_object_has_strings_with_correct_versions(encrypted)
            decrypted = self.evervault.decrypt(encrypted)
            assert decryption_should_succeed
            assert boolean == decrypted
        except EvervaultError as e:
            assert not decryption_should_succeed
            assert (
                str(e)
                == "Decryption of the provided data is restricted by your current policies. Please check and modify your policies, if needed, to enable decryption in this context."
            )

    @parameterized.expand(generate_combinations(CURVES, ROLES_AND_SUCCESSES))
    def test_encrypt_int(self, curve, role_and_success):
        self.setUp(curve)
        role = role_and_success["role"]
        decryption_should_succeed = role_and_success["decryption_should_succeed"]
        integer = 1

        try:
            encrypted = self.evervault.encrypt(integer, role)
            if role is not None:
                assert check_object_has_strings_with_correct_versions(encrypted)
            decrypted = self.evervault.decrypt(encrypted)
            assert decryption_should_succeed
            assert integer == decrypted
        except EvervaultError as e:
            assert not decryption_should_succeed
            assert (
                str(e)
                == "Decryption of the provided data is restricted by your current policies. Please check and modify your policies, if needed, to enable decryption in this context."
            )

    @parameterized.expand(generate_combinations(CURVES, ROLES_AND_SUCCESSES))
    def test_encrypt_float(self, curve, role_and_success):
        self.setUp(curve)
        role = role_and_success["role"]
        decryption_should_succeed = role_and_success["decryption_should_succeed"]
        flt = 3.14

        try:
            encrypted = self.evervault.encrypt(flt, role)
            if role is not None:
                assert check_object_has_strings_with_correct_versions(encrypted)
            decrypted = self.evervault.decrypt(encrypted)
            assert decryption_should_succeed
            assert flt == decrypted
        except EvervaultError as e:
            assert not decryption_should_succeed
            assert (
                str(e)
                == "Decryption of the provided data is restricted by your current policies. Please check and modify your policies, if needed, to enable decryption in this context."
            )

    @parameterized.expand(generate_combinations(CURVES, ROLES_AND_SUCCESSES))
    def test_encrypt_list(self, curve, role_and_success):
        self.setUp(curve)
        role = role_and_success["role"]
        decryption_should_succeed = role_and_success["decryption_should_succeed"]
        lst = ["hello", True, False, 1, 1.5]

        try:
            encrypted = self.evervault.encrypt(lst.copy(), role)
            if role is not None:
                assert check_object_has_strings_with_correct_versions(encrypted)
            decrypted = self.evervault.decrypt(encrypted)
            assert decryption_should_succeed
            assert lst == decrypted
        except EvervaultError as e:
            assert not decryption_should_succeed
            assert (
                str(e)
                == "Decryption of the provided data is restricted by your current policies. Please check and modify your policies, if needed, to enable decryption in this context."
            )

    @parameterized.expand(generate_combinations(CURVES, ROLES_AND_SUCCESSES))
    def test_encrypt_dict(self, curve, role_and_success):
        self.setUp(curve)
        role = role_and_success["role"]
        decryption_should_succeed = role_and_success["decryption_should_succeed"]
        dictionary = {"hello": "world"}

        try:
            encrypted = self.evervault.encrypt(dictionary, role)
            if role is not None:
                assert check_object_has_strings_with_correct_versions(encrypted)
            decrypted = self.evervault.decrypt(encrypted)
            assert decryption_should_succeed
            assert dictionary == decrypted
        except EvervaultError as e:
            assert not decryption_should_succeed
            assert (
                str(e)
                == "Decryption of the provided data is restricted by your current policies. Please check and modify your policies, if needed, to enable decryption in this context."
            )
