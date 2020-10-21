# Evervault-Python
Python SDK for [Evervault](https://evervault.com)

## Getting Started

#### Prerequisites

To get started with the Evervault Python SDK, you will need to have created a team on the evervault dashboard.

We are currently in invite-only early access. You can apply for early access [here](https://evervault.com).

#### Installation

```sh
pip install evervault
```

#### Setup

```python
from evervault.client import Client

# Initialize the client with your team's api key
evervault_client = Client(<API-KEY>);

# Encrypt your data and run a cage
result = evervault_client.encrypt_and_run(<CAGE-NAME>, { 'hello': 'World!' })
```

## API Reference

#### evervault_client.encrypt

Encrypt lets you encrypt data for use in any of your evervault cages. You can use it to store encrypted data to be used in a cage at another time.

```python
evervault_client.encrypt(data = dict | str)
```

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| data | dict or str | Data to be encrypted |

#### evervault_client.run

Run lets you invoke your evervault cages with a given payload.

```python
evervault_client.run(cageName = str, payload = dict)
```

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| cageName | str | Name of the cage to be run |
| data | dict | Payload for the cage |

#### evervault_client.encryptAndRun

Encrypt your data and use it as the payload to invoke the cage.

```python
evervault_client.encrypt_and_run(cageName = str, data = dict)
```

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| cageName | str | Name of the cage to be run |
| data | dict | Data to be encrypted |
