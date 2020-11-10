# Evervault-Python
<p align="center">
  <img src="res/logo.svg">
</p>

<p align="center">
  <a href="https://github.com/evervault/evervault-python/actions?query=workflow%3Aevervault-unit-tests"><img alt="Evervault unit tests status" src="https://github.com/evervault/evervault-python/workflows/evervault-unit-tests/badge.svg"></a>
</p>


## Getting Started
Python SDK for [Evervault](https://evervault.com)

#### Prerequisites

To get started with the Evervault Python SDK, you will need to have created a team on the evervault dashboard.

We are currently in invite-only early access. You can apply for early access [here](https://evervault.com).

#### Installation

```sh
pip install evervault
```

#### Setup

```python
import evervault

# Initialize the client with your team's api key
evervault.api_key = <YOUR-API-KEY>

# Encrypt your data and run a cage
result = evervault.encrypt_and_run(<CAGE-NAME>, { 'hello': 'World!' })
```

## API Reference

### evervault.encrypt

Encrypt lets you encrypt data for use in any of your evervault cages. You can use it to store encrypted data to be used in a cage at another time.

```python
evervault.encrypt(data = dict | str)
```

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| data | `dict` or `str` | Data to be encrypted |

### evervault.run

Run lets you invoke your evervault Cages with a given payload.

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

### evervault.encryptAndRun

Encrypt your data and use it as the payload to invoke the Cage.

```python
evervault.encrypt_and_run(cageName = str, data = dict[, options = dict])
```

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| cageName | `str` | Name of the Cage to be run |
| data | `dict` | Data to be encrypted |
| options | `dict` | [Options for the Cage run.](#Cage-Run-Options) |
