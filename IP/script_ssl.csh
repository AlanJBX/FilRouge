#!/bin/bash

openssl genrsa -aes256 -out certificat.key 4096
mv certificat.key certificat.key.lock
openssl rsa -in certificat.key.lock -out certificat.key
openssl req -new -key certificat.key.lock -out certificat.csr
openssl x509 -req -days 365 -in certificat.csr -signkey certificat.key.lock -out certificat.crt
mv certificat.key ../Flask/certificat.key
mv certificat.crt ../Flask/certificat.crt