import os, re
from setuptools import setup
from setuptools import find_packages

PKG = "evervault"
VERSIONFILE = os.path.join(PKG, "version.py")
version = "unknown"
try:
    version_file_text = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass # no version file exists
else:
    version_string_regex = r"^VERSION = ['\"]([^'\"]*)['\"]"
    matches = re.search(version_string_regex, version_file_text, re.M)
    if matches:
        version = matches.group(1)
    else:
        print("unable to find version in %s" % (VERSIONFILE,))
        raise RuntimeError("if %s.py exists, it must be well formed." % (VERSIONFILE,))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=PKG,
    version=version,
    author="Evervault",
    author_email="hey@evervault.com",
    url="https://evervault.com",
    license="LICENSE.txt",
    description="Evervault SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "pytest-socket",
        "requests_mock",
        "requests",
        "cryptography",
        "certifi",
        "pycryptodome",
    ],
)
