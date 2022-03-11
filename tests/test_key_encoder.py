from evervault.crypto.curves.p256 import P256PublicKey

import unittest
import base64

class TestKeyEncoder(unittest.TestCase):
   def test_encoding_of_p256_public_key(self):
    public_key = P256PublicKey(
      "04b7556ac070c439ba914e6e2f3ba2e582304dc548524ffc8414abc07ab5a843ecb1f1d71d3a620e6a7c08b895a72d62e2250d248a31da2a5d59ba6ecd636726c4"
    )
    der_encoded = base64.b64encode(public_key.encode()).decode('utf-8')
    expected_der = "MIIBSzCCAQMGByqGSM49AgEwgfcCAQEwLAYHKoZIzj0BAQIhAP////8AAAABAAAAAAAAAAAAAAAA////////////////MFsEIP////8AAAABAAAAAAAAAAAAAAAA///////////////8BCBaxjXYqjqT57PrvVV2mIa8ZR0GsMxTsPY7zjw+J9JgSwMVAMSdNgiG5wSTamZ44ROdJreBn36QBEEEaxfR8uEsQkf4vOblY6RA8ncDfYEt6zOg9KE5RdiYwpZP40Li/hp/m47n60p8D54WK84zV2sxXs7LtkBoN79R9QIhAP////8AAAAA//////////+85vqtpxeehPO5ysL8YyVRAgEBA0IABLdVasBwxDm6kU5uLzui5YIwTcVIUk/8hBSrwHq1qEPssfHXHTpiDmp8CLiVpy1i4iUNJIox2ipdWbpuzWNnJsQ="
    assert der_encoded == expected_der
