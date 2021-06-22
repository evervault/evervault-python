[![Evervault](https://evervault.com/evervault.svg)](https://evervault.com/)

[![Unit Tests Status](https://github.com/evervault/evervault-python/workflows/evervault-unit-tests/badge.svg)](https://github.com/evervault/evervault-python/actions?query=workflow%3Aevervault-unit-tests)

# Evervault Python SDK

The [Evervault](https://evervault.com) Python SDK is a toolkit for encrypting data as it enters your server, and working with Cages.

## Getting Started

Before starting with the Evervault Python SDK, you will need to [create an account](https://app.evervault.com/register) and a team.

For full installation support, [book time here](https://calendly.com/evervault/cages-onboarding).

## Documentation

See the Evervault [Python SDK documentation](https://docs.evervault.com/python).

## Installation

Our Python SDK is distributed via [pypi](https://pypi.org/project/evervault/), and can be installed using `pip`.

```sh
pip install evervault
```

## Setup

To make Evervault available for use in your app:

```python
import evervault

# Initialize the client with your team's api key
evervault.api_key = <YOUR-API-KEY>

# Encrypt your data and run a cage
result = evervault.encrypt_and_run(<CAGE-NAME>, { 'hello': 'World!' })
```

## Reference

The Evervault Python SDK exposes five functions.

### evervault.encrypt()

`evervault.encrypt()` encrypts data for use in your [Cages](https://docs.evervault.com/tutorial). To encrypt data at the server, simply pass a python primitive type into the `evervault.encrypt()` function. Store the encrypted data in your database as normal.

```python
evervault.encrypt(data = dict | list | set | str | int | bool)
```

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| data | `dict`, `list`, `set`, `str`, `int`, `bool` | Data to be encrypted |

### evervault.run()

`evervault.run()` invokes a Cage with a given payload.

```python
evervault.run(cageName = str, payload = dict[, options = dict])
```

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| cageName | `str` | Name of the Cage to be run |
| data | `dict` | Payload for the Cage |
| options | `dict` | [Options for the Cage run.](#Cage-Run-Options) |

#### Cage Run Options

| Option  | Type      | Default   | Description                                                                        |
| ------- | --------- | --------- | ---------------------------------------------------------------------------------- |
| async   | `Boolean` | `False` | Run your Cage in async mode. Async Cage runs will be queued for processing.          |
| version | `Integer` | `None`  | Specify the version of your Cage to run. By default, the latest version will be run. |

### evervault.encryptAndRun()

`evervault.encryptAndRun()` encrypts data and uses it as the payload to invoke the Cage.

```python
evervault.encrypt_and_run(cageName = str, data = dict[, options = dict])
```

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| cageName | `str` | Name of the Cage to be run |
| data | `dict` | Data to be encrypted |
| options | `dict` | [Options for the Cage run.](#Cage-Run-Options) |

### evervault.cages()

Return a `dict` of your team's Cage objects in `dict` format, with `cage-name` as keys.

### evervault.relay()

You may configure the SDK to automatically route all outbound HTTPS requests through [Relay](https://docs.evervault.com/product/relay) by calling the `relay()` function. This currently supports requests made using the popular [`requests`](https://docs.python-requests.org/en/master/) package.

```python
evervault.relay()
# all further HTTPS requests made in your program will be routed through Relay
```

You may also optionally pass in a list of domains which you **don't** want to go through Relay, i.e. requests sent to these domains will not be decrypted.

```python
evervault.relay(['httpbin.org', 'www.facebook.com'])
# requests sent to urls such as https://httpbin.org/post or https://api.facebook.com will not be sent through Relay
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/evervault/evervault-python.

## Feedback

Questions or feedback? [Let us know](mailto:support@evervault.com).
