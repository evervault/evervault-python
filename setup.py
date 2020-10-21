from setuptools import setup
from setuptools import find_packages
from evervault.version import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="evervault",
    version=VERSION,
    author="Jonny O'Mahony",
    author_email="jonny@evervault.com",
    url="https://evervault.com",
    license="LICENSE.txt",
    description="Evervault SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pytest", "requests", "cryptography", "certifi", "pycryptodome"],
)
