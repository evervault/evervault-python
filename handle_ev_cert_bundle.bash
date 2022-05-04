#!/bin/bash

POETRY_ENV=$(poetry env info --path)
VERSION=$(python -V 2>&1 | cut -d\  -f 2)
VERSION=(${VERSION//./ })

CERT_FILE="${POETRY_ENV}/lib/python${VERSION[0]}.${VERSION[1]}/site_packages/certifi/cacert.pem"

echo ${CERT_FILE}

