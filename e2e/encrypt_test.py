from .e2e_test_case import EndToEndTestCase


class EncryptTest(EndToEndTestCase):
    def test_encrypt_str(self):
        string = "hello world"
        encrypted = self.evervault.encrypt(string)
        decrypted = self.evervault.decrypt(encrypted)
        assert string == decrypted

    def test_encrypt_bool_true(self):
        boolean = True
        encrypted = self.evervault.encrypt(boolean)
        decrypted = self.evervault.decrypt(encrypted)
        assert boolean == decrypted

    def test_encrypt_bool_false(self):
        boolean = False
        encrypted = self.evervault.encrypt(boolean)
        decrypted = self.evervault.decrypt(encrypted)
        assert boolean == decrypted

    def test_encrypt_int(self):
        integer = 1
        encrypted = self.evervault.encrypt(integer)
        decrypted = self.evervault.decrypt(encrypted)
        assert integer == decrypted

    def test_encrypt_float(self):
        flt = 3.14
        encrypted = self.evervault.encrypt(flt)
        decrypted = self.evervault.decrypt(encrypted)
        assert flt == decrypted

    def test_encrypt_list(self):
        lst = ["hello", True, False, 1, 1.5]
        encrypted = self.evervault.encrypt(lst.copy())
        decrypted = self.evervault.decrypt(encrypted)
        assert lst == decrypted

    def test_encrypt_dict(self):
        dictionary = {"hello": "world"}
        encrypted = self.evervault.encrypt(dictionary)
        decrypted = self.evervault.decrypt(encrypted)
        assert dictionary == decrypted
