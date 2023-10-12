# from .e2e_test_case import EndToEndTestCase
# import base64


# class ClientSideDecryptTokenTest(EndToEndTestCase):
#     def test_create_client_side_decrypt_token(self):
#         data = ["hello", 1, 1.5, True, False, {"hello": "world"}]
#         encrypted = self.evervault.encrypt(data)
#         token_response = self.evervault.create_client_side_decrypt_token(encrypted)
#         self.assertEqual(token_response["id"].startswith("client_side_token"), True)
#         self.assertEqual(isinstance(token_response["token"], str), True)
#         self.assertEqual(isinstance(token_response["expiry"], int), True)

#         auth_value = f"{self.app_uuid}:{self.api_key}"
#         encoded_auth_value_bytes = base64.b64encode(auth_value.encode("ascii"))
#         basic_auth_str = f"Basic {encoded_auth_value_bytes.decode('utf-8')}"
#         body = self.make_request(
#             "https://api.evervault.com/decrypt",
#             {"Content-Type": "application/json", "Authorization": basic_auth_str},
#             {"token": token_response["token"], "payload": encrypted},
#         )
#         decrypted = body["payload"]
#         self.assertEqual(decrypted[0], "hello")
#         self.assertEqual(decrypted[1], 1)
#         self.assertEqual(decrypted[2], 1.5)
#         self.assertEqual(decrypted[3], True)
#         self.assertEqual(decrypted[4], False)
#         self.assertEqual(decrypted[5], {"hello": "world"})
