#! /usr/bin env:bash
# 
# Use OpenSSL to generate RSA key pair
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
#
# * Run sh generate_rsa_keys.sh
