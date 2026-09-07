import datetime
import jwt

class JWTAuth:
    secret_key = ""
    algorithm = "HS256"
    payload = {
    "sub": "user_12345",                       # Subject (User ID)
    "name": "Alice",
    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1), # Expiration time
    "iat": datetime.datetime.now(datetime.timezone.utc)                                # Issued at
    }

    def __init__(self, secret):
        self.secret_key = secret

    def encode(self):
        token = jwt.encode(self.payload, self.secret_key, algorithm=self.algorithm)
        return token

    def decode(self, token):
        try:
        # PyJWT automatically verifies 'exp' and 'iat' claims by default
            decoded_payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            print("Decoded Payload successfully:")
            print(decoded_payload)
        except jwt.ExpiredSignatureError:
            print("Error: The token has expired.")
        except jwt.InvalidTokenError:
            print("Error: Invalid token string or signature.")   