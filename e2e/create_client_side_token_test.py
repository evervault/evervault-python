from .e2e_test_case import EndToEndTestCase
import base64

class ClientSideDecryptTokenTest(EndToEndTestCase):
    def test_create_client_side_decrypt_token(self):
        data = [
            "hello",
            1,
            1.5,
            True,
            False,
            {"hello": "world"}
        ]
        encrypted = self.evervault.encrypt(data)
        token_response = self.evervault.create_client_side_decrypt_token(encrypted)
        assert token_response["id"].startswith("client_side_token") == True
        assert isinstance(token_response["token"], str) == True
        assert isinstance(token_response["expiry"], int) == True

        auth_value = f"{self.app_uuid}:{self.api_key}"
        encoded_auth_value_bytes = base64.b64encode(auth_value.encode("ascii"))
        basic_auth_str = f"Basic {encoded_auth_value_bytes.decode('utf-8')}"
        body = self.make_request("https://api.evervault.com/decrypt", {"Content-Type": "application/json", "Authorization": basic_auth_str}, { "token": token_response["token"], "payload": encrypted })
        decrypted = body["payload"]
        assert decrypted[0] == "hello"
        assert decrypted[1] == 1
        assert decrypted[2] == 1.5
        assert decrypted[3] == True
        assert decrypted[4] == False
        assert decrypted[5] == {"hello": "world"}
