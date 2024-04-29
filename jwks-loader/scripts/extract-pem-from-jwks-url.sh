#!/bin/bash
# Fetch JWKS
#curl -s http://example.com/.well-known/jwks.json > jwks.json
curl -sLO http://hydra:4444/.well-known/jwks.json	
# Assuming we're using the first key as an example
# Extract modulus and exponent in base64url and convert to normal base64
MODULUS=$(jq -r '.keys[0].n' jwks.json | tr '_-' '+/' | tr -d '\n' | sed 's/$/=/' | sed 's/$/=/' | sed 's/$/=/' | tr -d '=')
EXPONENT=$(jq -r '.keys[0].e' jwks.json | tr '_-' '+/' | tr -d '\n' | sed 's/$/=/' | sed 's/$/=/' | sed 's/$/=/' | tr -d '=')
# Convert from base64url to hex
MODULUS_HEX=$(echo $MODULUS | base64 -d | xxd -p | tr -d "\\n")
EXPONENT_HEX=$(echo $EXPONENT | base64 -d | xxd -p | tr -d "\\n")
# Create the public key file
echo "Modulus: $MODULUS_HEX"
echo "Exponent: $EXPONENT_HEX"
cat <<EOF > public_key.pem
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA$(echo $MODULUS | base64 -w 0)
$(echo $EXPONENT | base64 -w 0)
-----END PUBLIC KEY-----
EOF
cat public_key.pem
