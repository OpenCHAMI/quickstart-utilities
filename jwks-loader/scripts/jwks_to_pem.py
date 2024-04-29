#! /usr/bin/python

import os
import json
import requests
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from base64 import urlsafe_b64decode
import argparse

def jwks_to_pem(jwks_url):
    # Fetch the JWKS
    response = requests.get(jwks_url)
    jwks = response.json()
    # Assuming the first key in the set is the one we need
    key = jwks['keys'][0]
    # Decode the modulus and exponent
    modulus = int.from_bytes(urlsafe_b64decode(key['n'] + '=='), byteorder='big')
    exponent = int.from_bytes(urlsafe_b64decode(key['e'] + '=='), byteorder='big')
    # Create a public key
    public_key = rsa.RSAPublicNumbers(e=exponent, n=modulus).public_key()
    # Serialize the public key to PEM format
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode('utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JWKS to PEM')
    parser.add_argument('--jwks-url', dest='jwks_url', action='store', default=None,
                        help='URL for testing purposes')
    parser.add_argument('--output-dir', dest='output_dir', action='store', default=None,
                        help='Output file directory.  The name will be public_key.pem')
    args = parser.parse_args()

    if args.jwks_url:
        jwks_url = args.jwks_url
    else:
        # Use Docker environment variable if not in testing mode
        jwks_url = os.getenv("JWKS_URL", "http://hydra:4444/.well-known/jwks.json")

    pem_output = jwks_to_pem(jwks_url)

    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir  = os.getenv("JWKS_PATH")

    if output_dir: 
        filepath = os.path.join(output_dir, 'public_key.pem')
        with open(filepath, 'w') as f:
            f.write(pem_output)
    else:
        print(pem_output)
