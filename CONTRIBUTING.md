[![Evervault](https://evervault.com/evervault.svg)](https://evervault.com/)

# Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/evervault/evervault-python.

## Getting Started

To make life easier, this module features a code formatter/linter and also a commit formatter/linter, so that our
releases will be compatible with [semantic release](https://semantic-release.gitbook.io/semantic-release/).

We also use [poetry](https://python-poetry.org/) to make dependency management and general development easier. Once you have poetry installed, you can install the dependencies using

```shell
poetry install
```

From there, you are able to run python using

```shell
poetry run python you_file.py
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

To maintain compatibility with [semantic versioning](https://semver.org/), we use a combination of commit formatting and [semantic release](https://github.com/semantic-release/semantic-release).

We use the commit style specified in [conventional commits](https://www.conventionalcommits.org/). Please ensure that all commits meet this format so that releases can be generated correctly.
