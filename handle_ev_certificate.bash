#!/bin/bash

wget https://ca.evervault.io --output ~/evervault.io.pem

# append evervault.io certificate to certifi pem :)

cat ~/evervault.io.pem >> ~/.cache/pypoetry/virtualenvs/evervault-0PWu0pY7-py3.9/lib/python3.9/site-packages/certifi/cacert.pem
