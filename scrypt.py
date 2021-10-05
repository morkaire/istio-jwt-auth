"""
This script uses RSA public/private key pair generated using Openssl command line tool.
The series of steps are listed below
1. Import openssl generated public/private key pair
3. Generate the Token using the Private key from step 1
4. Validate the JWT Token using the Public key from step 1
"""
# ______________________________ Step 0 ______________________________________
# import python_jwt
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime

# ______________________________ Step 1 ______________________________________
# ______________________________ IMPORT KEY ______________________________________
# Import the key.
# The private key will be used to Generate the Token

# Path to the private and public key files generated using openssl
PRIVATE_KEY_FILE="./keys/private-key.pem"
PUBLIC_KEY_FILE="./keys/public-key.pem"

# Define payload
# payload that the server will send back the client encoded in the JWT Token
# While generating a token, you can define any type of payload in valid JSON format
# the iss(issuer), sub(subject) and aud(audience) are reserved claims. https://tools.ietf.org/html/rfc7519#section-4.1
# These reserved claims are not mandatory to define in a standard JWT token.
# But when working with Istio, it's better you define these.

payload = {
    'iss':'ISSUER', 
    'sub':'SUBJECT', 
    'aud':'AUDIENCE', 
    'role': 'user', 
    'permission': 'read' 
}


public_key = ""
private_key = ""
token=""

with open(PUBLIC_KEY_FILE, "rb") as pemfile:
    public_key = jwk.JWK.from_pem(pemfile.read())
    public_key = public_key.export()
    


with open(PRIVATE_KEY_FILE, "rb") as pemfile:
    private_key = jwk.JWK.from_pem(pemfile.read())
    private_key = private_key.export()


# ______________________________ Step 2 ______________________________________
# ______________________________ GENERATE JWT TOKEN ______________________________________
# Generate the JWT Tokes using the Private Key
# Provide the payload and the Private Key. RS256 is the Hash used and last value is the expiration time.
# You can set the expiration time according to your need.
# To generate JWT Token, you need the private key as a JWK object
token = jwt.generate_jwt(payload, jwk.JWK.from_json(private_key), 'RS256', datetime.timedelta(minutes=500000))


# Print the public key, private key and the token
print("\n_________________PUBLIC___________________\n")
print(public_key)
print("\n_________________PRIVATE___________________\n")
print(private_key)
print("\n_________________TOKEN___________________\n")
print(token)



# ______________________________ Step 4 ______________________________________
# ______________________________ VALIDATE JWT TOKEN USING PUBLIC KEY ______________________________________


# To validate JWT Token, you need the public key as a JWK object
header, claims = jwt.verify_jwt(token, jwk.JWK.from_json(public_key), ['RS256'])

print("\n_________________TOKEN INFO___________________\n")
print(header)
print(claims)
