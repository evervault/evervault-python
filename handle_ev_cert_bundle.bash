#!/bin/bash

POETRY_ENV=$(poetry env info --path)
VERSION=$(python -V 2>&1 | cut -d\  -f 2)
VERSION=(${VERSION//./ })

CERT_FILE="${POETRY_ENV}/lib/python${VERSION[0]}.${VERSION[1]}/site-packages/certifi/cacert.pem"
UBUNTU_BUNDLE="/etc/ssl/certs/ca-certificates.crt"

# removing virtual env file and replacing it with OS bundle
rm ${CERT_FILE}
ln -s ${UBUNTU_BUNDLE} ${CERT_FILE}

ls -la ${CERT_FILE}