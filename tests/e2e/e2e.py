import evervault
import os
import requests

evervault.init(api_key=os.environ.get("EV_API_KEY"), enable_outbound_relay=True)

encrypted_payload = evervault.encrypt("I should be decrypted")
response = requests.post(
    os.environ.get("TARGET_URL"), data={"payload": encrypted_payload}
)
