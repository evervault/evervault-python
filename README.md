[![Evervault](https://evervault.com/evervault.svg)](https://evervault.com/)

[![Unit Tests Status](https://github.com/evervault/evervault-python/workflows/evervault-unit-tests/badge.svg)](https://github.com/evervault/evervault-python/actions?query=workflow%3Aevervault-unit-tests)

# Evervault Python SDK

The [Evervault](https://evervault.com) Python SDK is a toolkit for encrypting data as it enters your server, working with Functions, and proxying your outbound api requests to specific domains through [Outbound Relay](https://docs.evervault.com/concepts/relay/outbound-interception) to allow them to be decrypted before reaching their target.

## Getting Started

Before starting with the Evervault Python SDK, you will need to [create an account](https://app.evervault.com/register) and a team.

For full installation support, [book time here](https://calendly.com/evervault/support).

Before contributing, make sure to use [commitizen](https://github.com/commitizen/cz-cli) & to read [Contributing.md](./CONTRIBUTING.md).

## Documentation

See the Evervault [Python SDK documentation](https://docs.evervault.com/sdk/python).

## Installation

Our Python SDK is distributed via [pypi](https://pypi.org/project/evervault/), and can be installed using `pip`.

```sh
pip install evervault
```

## Setup

To make Evervault available for use in your app:

```python
import evervault

# Initialize the client with your team’s API key
evervault.init("<YOUR_API_KEY>")

# Encrypt your data
encrypted = evervault.encrypt({ "name": "Claude" })

# Process the encrypted data in a Function
result = evervault.run("<YOUR_FUNCTION_NAME>", encrypted)

# Send the decrypted data to a third-party API
evervault.enable_outbound_relay()
requests.post("https://example.com", json = encrypted)

# Send attested requests to a Cage
attested_session = evervault.cage_requests_session({ 'my-cage': { 'pcr_8': '...' } })
# Attested TLS directly to the enclave
attested_session.get('https://my-cage.my-app.cages.evervault.com/hello')
```

## Reference

The Evervault Python SDK exposes five functions.

### evervault.init()

`evervault.init()` initializes the SDK with your API key. Configurations for the interception of outbound requests may also be passed in this function.

```python
evervault.init(api_key = str[, decryption_domains=[], retry = bool, curve = str])
```

| Parameter | Type  | Description                                                                                                                                                    |
| --------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| api_key   | `str` | The API key of your Evervault Team                                                                                                                             |
| curve     | `str` | The elliptic curve used for cryptographic operations. See [Elliptic Curve Support](https://docs.evervault.com/reference/elliptic-curve-support) to learn more. |

### evervault.encrypt()

`evervault.encrypt()` encrypts data for use in your [Functions](https://docs.evervault.com/tutorial). To encrypt data at the server, simply pass a python primitive type into the `evervault.encrypt()` function. Store the encrypted data in your database as normal.

```python
evervault.encrypt(data = dict | list | set | str | int | bool)
```

| Parameter | Type                                        | Description          |
| --------- | ------------------------------------------- | -------------------- |
| data      | `dict`, `list`, `set`, `str`, `int`, `bool` | Data to be encrypted |

### evervault.run()

`evervault.run()` invokes a Function with a given payload.

```python
evervault.run(function_name = str, data = dict[, options = dict])
```

| Parameter     | Type   | Description                                            |
| ------------- | ------ | ------------------------------------------------------ |
| function_name | `str`  | Name of the Function to be run.                        |
| data          | `dict` | Payload for the Function.                              |
| options       | `dict` | [Options for the Function run.](#Function-Run-Options) |

#### Function Run Options

| Option  | Type      | Default | Description                                                                              |
| ------- | --------- | ------- | ---------------------------------------------------------------------------------------- |
| async   | `Boolean` | `False` | Run your Function in async mode. Async Function runs will be queued for processing.      |
| version | `Integer` | `None`  | Specify the version of your Function to run. By default, the latest version will be run. |

### evervault.create_run_token()

`evervault.create_run_token()` creates a single use, time bound token for invoking a function.

```python
evervault.create_run_token(function_name = str, data = dict)
```

| Parameter     | Type   | Description                                               |
| ------------- | ------ | --------------------------------------------------------- |
| function_name | `str`  | Name of the Function the run token should be created for. |
| data          | `dict` | Payload that the token can be used with.                  |

### evervault.enable_outbound_relay()

`evervault.enable_outbound_relay()` configures your application to proxy HTTP requests using Outbound Relay based on the configuration created in the Evervault dashboard. See [Outbound Relay](https://docs.evervault.com/concepts/outbound-relay/overview) to learn more.
Asynchronous HTTP requests are supported with [aiohttp](https://docs.aiohttp.org/). Pass in a [aiohttp.ClientSession](https://docs.aiohttp.org/en/stable/client_reference.html) to enable them for that session. Note: Requires Python 3.11+

```python
evervault.enable_outbound_relay([decryption_domains = Array, debug_requests = Boolean])
```

| Parameter          | Type                                                                              | Default | Description                                                                                                                                                    |
| ------------------ | --------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| decryption_domains | `Array`                                                                           | `None`  | Requests sent to any of the domains listed will be proxied through Outbound Relay. This will override the configuration created using the Evervault dashboard. |
| debug_requests     | `Boolean`                                                                         | `False` | Output request domains and whether they were sent through Outbound Relay.                                                                                      |
| client_session     | [aiohttp.ClientSession](https://docs.aiohttp.org/en/stable/client_reference.html) | `None`  | The [aiohttp](https://docs.aiohttp.org/) client session to enable outbound relay on. Requires Python >= 3.11.                                                  |

### evervault.cage_requests_session()

`evervault.cage_requests_session()` creates a `requests` `Session` which attests all traffic between your client and the Cage. You can provide the PCRs generated at build time to have even tighter control on the attestation.

```python
evervault.cage_requests_session([cage_attestation_data = dict])
```

| Parameter             | Type   | Default | Description                                                                                                                                                                                          |
| --------------------- | ------ | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cage_attestation_data | `dict` | `None`  | Provide attestation measures to make assertions about the code running within your enclave. The `cage_attestation_data` dict is a mapping of cage names to their corresponding attestation measures. |

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/evervault/evervault-python.

## Feedback

Questions or feedback? [Let us know](mailto:support@evervault.com).
