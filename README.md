[![Evervault](https://evervault.com/evervault.svg)](https://evervault.com/)

[![Unit Tests Status](https://github.com/evervault/evervault-python/workflows/evervault-unit-tests/badge.svg)](https://github.com/evervault/evervault-python/actions?query=workflow%3Aevervault-unit-tests)

# Evervault Python SDK

The [Evervault](https://evervault.com) Python SDK is a toolkit for encrypting data as it enters your server, and working with Cages. By default, initializing the SDK will result in all outbound HTTPS requests being intercepted and decrypted.

## Getting Started

Before starting with the Evervault Python SDK, you will need to [create an account](https://app.evervault.com/register) and a team.

For full installation support, [book time here](https://calendly.com/evervault/cages-onboarding).

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

# Initialize the client with your team's api key
evervault.init('<YOUR-API-KEY>')

# Encrypt your data and run a cage
result = evervault.encrypt_and_run(<CAGE-NAME>, { 'hello': 'World!' })
```

## Reference

The Evervault Python SDK exposes five functions.

### evervault.init()

`evervault.init()` initializes the SDK with your API key. Configurations for the interception of outbound requests may also be passed in this function.

```python
evervault.init(api_key = str[, intercept = bool, ignore_domains = list])
```

| Parameter      | Type        | Description                                                              |
| -------------- | ----------- | ------------------------------------------------------------------------ |
| api_key        | `str`       | The API key of your Evervault Team                                       |
| intercept      | `bool`      | Decides if outbound requests are intercepted (`true` by default)         |
| ignore_domains | `list(str)` | Requests sent to any of the domains in this list will not be intercepted |

### evervault.encrypt()

`evervault.encrypt()` encrypts data for use in your [Cages](https://docs.evervault.com/tutorial). To encrypt data at the server, simply pass a python primitive type into the `evervault.encrypt()` function. Store the encrypted data in your database as normal.

```python
evervault.encrypt(data = dict | list | set | str | int | bool)
```

| Parameter | Type                                        | Description          |
| --------- | ------------------------------------------- | -------------------- |
| data      | `dict`, `list`, `set`, `str`, `int`, `bool` | Data to be encrypted |

### evervault.run()

`evervault.run()` invokes a Cage with a given payload.

```python
evervault.run(cage_name = str, data = dict[, options = dict])
```

| Parameter | Type   | Description                                    |
| --------- | ------ | ---------------------------------------------- |
| cageName  | `str`  | Name of the Cage to be run                     |
| data      | `dict` | Payload for the Cage                           |
| options   | `dict` | [Options for the Cage run.](#Cage-Run-Options) |

#### Cage Run Options

| Option  | Type      | Default | Description                                                                          |
| ------- | --------- | ------- | ------------------------------------------------------------------------------------ |
| async   | `Boolean` | `False` | Run your Cage in async mode. Async Cage runs will be queued for processing.          |
| version | `Integer` | `None`  | Specify the version of your Cage to run. By default, the latest version will be run. |

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/evervault/evervault-python.

## Feedback

Questions or feedback? [Let us know](mailto:support@evervault.com).
