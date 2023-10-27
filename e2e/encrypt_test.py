from .e2e_test_case import EndToEndTestCase
from parameterized import parameterized

CURVES = ["SECP256K1", "SECP256R1"]
METADATA = [{"role": "permit-all"}, {}]

def generate_combinations(list1, list2):
    return [(x, y) for x in list1 for y in list2]

class EncryptTest(EndToEndTestCase):
    @parameterized.expand(generate_combinations(CURVES, METADATA))
    def test_encrypt_str(self, curve, metadata):
        self.setUp(curve)
        string = "hello world"
        encrypted = self.evervault.encrypt(string, metadata)
        decrypted = self.evervault.decrypt(encrypted)
        assert string == decrypted

    @parameterized.expand(generate_combinations(CURVES, METADATA))
    def test_encrypt_bool_true(self, curve, metadata):
        self.setUp(curve)
        boolean = True
        encrypted = self.evervault.encrypt(boolean, metadata)
        decrypted = self.evervault.decrypt(encrypted)
        assert boolean == decrypted

    @parameterized.expand(generate_combinations(CURVES, METADATA))
    def test_encrypt_bool_false(self, curve, metadata):
        self.setUp(curve)
        boolean = False
        encrypted = self.evervault.encrypt(boolean, metadata)
        decrypted = self.evervault.decrypt(encrypted)
        assert boolean == decrypted

    @parameterized.expand(generate_combinations(CURVES, METADATA))
    def test_encrypt_int(self, curve, metadata):
        self.setUp(curve)
        integer = 1
        encrypted = self.evervault.encrypt(integer, metadata)
        decrypted = self.evervault.decrypt(encrypted)
        assert integer == decrypted

    @parameterized.expand(generate_combinations(CURVES, METADATA))
    def test_encrypt_float(self, curve, metadata):
        self.setUp(curve)
        flt = 3.14
        encrypted = self.evervault.encrypt(flt, metadata)
        decrypted = self.evervault.decrypt(encrypted)
        assert flt == decrypted

    @parameterized.expand(generate_combinations(CURVES, METADATA))
    def test_encrypt_list(self, curve, metadata):
        self.setUp(curve)
        lst = ["hello", True, False, 1, 1.5]
        encrypted = self.evervault.encrypt(lst.copy(), metadata)
        decrypted = self.evervault.decrypt(encrypted)
        assert lst == decrypted

    @parameterized.expand(generate_combinations(CURVES, METADATA))
    def test_encrypt_dict(self, curve, metadata):
        self.setUp(curve)
        dictionary = {"hello": "world"}
        encrypted = self.evervault.encrypt(dictionary, metadata)
        decrypted = self.evervault.decrypt(encrypted)
        assert dictionary == decrypted
