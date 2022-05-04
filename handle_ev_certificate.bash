#!/bin/bash

sudo apt-get update
sudo apt-get install -y apt-transport-https curl ca-certificates

wget https://ca.evervault.io --output ~/evervault.io.pem

sudo curl https://ca.evervault.io --output /usr/local/share/ca-certificates/evervault.io.crt
find /usr/local/share/ca-certificates
sudo update-ca-certificates
