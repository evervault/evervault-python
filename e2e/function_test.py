from .e2e_test_case import EndToEndTestCase
import base64, os

class FunctionTest(EndToEndTestCase):
    FUNCTION_NAME = os.getenv("EV_FUNCTION_NAME")

    def test_function_run(self):
        data = {"name": "test"}
        encrypted = self.evervault.encrypt(data)
        function_response = self.evervault.run(FunctionTest.FUNCTION_NAME, encrypted)
        assert function_response["result"]["message"] == "Hello from a Function! It seems you have 4 letters in your name"

    def test_function_run_async(self):
        data = {"name": "test"}
        encrypted = self.evervault.encrypt(data)
        function_response = self.evervault.run(FunctionTest.FUNCTION_NAME, encrypted, {"async": True })
        assert function_response == None

    def test_create_function_run_token(self):
        data = {"name": "test"}
        encrypted = self.evervault.encrypt(data)
        function_response = self.evervault.create_run_token(FunctionTest.FUNCTION_NAME, encrypted)
        assert isinstance(function_response["token"], str) == True

        run_response = self.__run_function_with_token(function_response["token"], FunctionTest.FUNCTION_NAME, encrypted)
        assert run_response["result"]["message"] == "Hello from a Function! It seems you have 4 letters in your name"

    def __run_function_with_token(self, token, function_name, payload):
        url = f"https://run.evervault.com/{function_name}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type" : "application/json"
        }
        return self.make_request(url, headers, payload)