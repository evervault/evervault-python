from evervault.errors.evervault_errors import FunctionRuntimeError
from .e2e_test_case import EndToEndTestCase
import os


class FunctionTest(EndToEndTestCase):
    FUNCTION_NAME = os.getenv("EV_FUNCTION_NAME")
    INITIALIZATION_ERROR_FUNCTION_NAME = os.getenv(
        "EV_INITIALIZATION_ERROR_FUNCTION_NAME"
    )

    PAYLOAD = {
        "string": "hello",
        "integer": 1,
        "float": 1.5,
        "true": True,
        "false": False,
        "array": ["hello", 1, 1.5, True, False],
        "obj": {
            "hello": "world",
        },
    }

    EXPECTED_RESPONSE = {
        "string": "string",
        "integer": "number",
        "float": "number",
        "true": "boolean",
        "false": "boolean",
        "array": {
            "0": "string",
            "1": "number",
            "2": "number",
            "3": "boolean",
            "4": "boolean",
        },
        "obj": {"hello": "string"},
    }

    def test_function_run(self):
        encrypted = self.evervault.encrypt(FunctionTest.PAYLOAD)
        function_response = self.evervault.run(FunctionTest.FUNCTION_NAME, encrypted)
        for key, value in FunctionTest.EXPECTED_RESPONSE.items():
            assert function_response["result"][key] == value

    def test_function_run_with_error(self):
        encrypted = self.evervault.encrypt({"shouldError": True})
        try:
            self.evervault.run(FunctionTest.FUNCTION_NAME, encrypted)
        except FunctionRuntimeError as e:
            assert str(e) == "User threw an error"

    def test_function_run_with_initialization_error(self):
        try:
            self.evervault.run(FunctionTest.INITIALIZATION_ERROR_FUNCTION_NAME, {})
        except FunctionRuntimeError as e:
            print("-----++++++--------++++++--------")
            print(e)
            print(e.stack)
            print("-----++++++--------++++++--------")
            assert (
                str(e)
                == "The function failed to initialize. This error is commonly encountered when there are problems with the function code (e.g. a syntax error) or when a required import is missing."
            )

    def test_create_function_run_token(self):
        encrypted = self.evervault.encrypt(FunctionTest.PAYLOAD)
        function_response = self.evervault.create_run_token(
            FunctionTest.FUNCTION_NAME, encrypted
        )
        self.assertEqual(isinstance(function_response["token"], str), True)

        run_response = self.__run_function_with_token(
            function_response["token"], FunctionTest.FUNCTION_NAME, encrypted
        )
        assert run_response["result"] == FunctionTest.EXPECTED_RESPONSE

    def __run_function_with_token(self, token, function_name, encrypted_payload):
        url = f"https://api.evervault.com/functions/{function_name}/runs"
        headers = {
            "Authorization": f"RunToken {token}",
            "Content-Type": "application/json",
        }
        return self.make_request(url, headers, {"payload": encrypted_payload})
