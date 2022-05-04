#!/bin/bash

sudo apt-get update
sudo apt-get install -y apt-transport-https curl ca-certificates

sudo curl https://ca.evervault.io --output /usr/local/share/ca-certificates/evervault.io.crt
sudo update-ca-certificates
