import evervault
import requests

evervault.init("app_33b88ca7da0d", "#")

# Extend requests session to use relay RP
# Pulls down relays from API and rewrites request to match evervault relay domain
relay_requests_adapter = evervault.relay_requests_adapter()

response = relay_requests_adapter.get('https://putsreq.com/1DBL0KZy79WdcfVUsi4Z')


# Uses Relay connect and matches on domain passed as arg
# Doesn't require pulling down relays from API
adapter = evervault.enable_relay_interception(domains="putsreq.com", client='requests')
session = requests.Session()
session.mount('https://', adapter)
response = session.get('https://putsreq.com/1DBL0KZy79WdcfVUsi4Z')

print(response.text)

