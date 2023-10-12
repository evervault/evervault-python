[![Evervault](https://evervault.com/evervault.svg)](https://evervault.com/)

# Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/evervault/evervault-python.

## Getting Started

We use [poetry](https://python-poetry.org/) to make dependency management and general development easier. Once you have poetry installed, you can install the dependencies using

```shell
poetry install
```

From there, you are able to run python using

```shell
poetry run python your_file.py
```

## Testing and Code Formatting

We use [black](https://github.com/psf/black) and [flake8](https://flake8.pycqa.org/en/latest/) for code formatting and linting. You can run them through poetry by running

```shell
poetry run black .
poetry run flake8 --ignore=E501,W503,E722
```

You can also run the tests using [pytest](https://docs.pytest.org/en/6.2.x/) by running

```shell
poetry run pytest
```

All of these are run using a GitHub action on pull-requests, so please ensure that your code passes these tests before pushing, to save yourself some time.

## Commit Formatting & Releases

We use [changesets](https://github.com/changesets/changesets) to version manage in this repo.

When creating a pr that needs to be rolled into a version release, do `npx changeset`, select the level of the version bump required and describe the changes for the change logs. DO NOT select major for releasing breaking changes without team approval.

To release:

Merge the version PR that the changeset bot created to bump the version numbers. This will bump the versions of the packages, create a git tag for the release, and release the new version to npm.