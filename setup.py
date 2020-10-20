from setuptools import setup
from setuptools import find_packages

setup(
    name="Evervault",
    version="0.1.0",
    author="Jonny O'Mahony",
    author_email="jonny@evervault.com",
    url="https://evervault.com",
    license="LICENSE.txt",
    description="Evervault SDK",
    long_description=open("README.md").read(),
    packages=find_packages(),
    install_requires=["pytest", "requests", "cryptography", "certifi", "pycryptodome"],
)
