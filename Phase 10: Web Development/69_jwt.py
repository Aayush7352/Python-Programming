"""
JWT (JSON Web Token) demonstration.

Requires: pip install pyjwt
"""
import sys
import time
import json


def demonstrate_jwt():
    """JWT encode, decode, and validation."""
    try:
        import jwt
    except ImportError:
        print("PyJWT is not installed.")
        print("Install with: pip install pyjwt")
        return

    print("=== JWT Basics ===")

    SECRET_KEY = "my-secret-key-please-use-environment-variable-in-production"

    # Create a payload
    payload = {
        "sub": "user_123",
        "name": "Alice Smith",
        "email": "alice@example.com",
        "role": "admin",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,  # 1 hour expiry
    }

    # Encode
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print(f"  Token: {token[:50]}...{token[-20:]}")

    # Decode & verify
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(f"\n  Decoded payload:")
        for key, value in decoded.items():
            print(f"    {key}: {value}")
    except jwt.ExpiredSignatureError:
        print("  Token expired")
    except jwt.InvalidTokenError as e:
        print(f"  Invalid token: {e}")

    # Token verification
    print("\n=== Token Verification ===")

    def verify_token(token: str, secret: str) -> dict | None:
        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            print("  Token has expired")
        except jwt.InvalidSignatureError:
            print("  Invalid signature")
        except jwt.InvalidTokenError as e:
            print(f"  Invalid token: {e}")
        return None

    result = verify_token(token, SECRET_KEY)
    print(f"  Verified: {result is not None}")

    result = verify_token(token, "wrong-secret")
    print(f"  Wrong secret: {result is not None}")

    # Different algorithms
    print("\n=== Different Algorithms ===")

    for algo in ["HS256", "HS384", "HS512"]:
        t = jwt.encode(payload, SECRET_KEY, algorithm=algo)
        decoded = jwt.decode(t, SECRET_KEY, algorithms=[algo])
        print(f"  {algo}: {len(t)} chars - sub={decoded['sub']}")

    # RS256 (asymmetric)
    print("\n=== RS256 (Asymmetric) ===")
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        rsa_token = jwt.encode(payload, private_pem, algorithm="RS256")
        print(f"  RS256 token: {rsa_token[:30]}...")
        decoded = jwt.decode(rsa_token, public_pem, algorithms=["RS256"])
        print(f"  Verified with public key: sub={decoded['sub']}")

    except ImportError:
        print("  cryptography not installed (pip install cryptography)")

    # JWT Claims validation
    print("\n=== Claims Validation ===")

    def create_token_with_claims(payload: dict) -> str:
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    def validate_claims(token: str, required_claims: list = None) -> dict:
        options = {
            "verify_signature": True,
            "require": required_claims or [],
            "verify_exp": True,
            "verify_iat": True,
        }
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options=options)

    # Token with custom claims
    custom_payload = {
        "sub": "user_456",
        "name": "Bob",
        "role": "user",
        "permissions": ["read", "write"],
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }

    custom_token = create_token_with_claims(custom_payload)
    decoded = validate_claims(custom_token, required_claims=["sub", "exp"])
    print(f"  Validated with required claims: sub={decoded['sub']}")

    # Token expiry
    print("\n=== Token Expiry ===")
    expired_payload = {
        "sub": "user_expired",
        "exp": int(time.time()) - 10,  # expired 10 seconds ago
    }
    expired_token = create_token_with_claims(expired_payload)
    result = verify_token(expired_token, SECRET_KEY)
    print(f"  Expired token verified: {result}")


def main():
    demonstrate_jwt()

    print("\n=== JWT Best Practices ===")
    print("  1. Store secret keys securely (env vars)")
    print("  2. Set appropriate expiry times")
    print("  3. Use HTTPS in production")
    print("  4. Validate all claims on every request")
    print("  5. Use asymmetric keys (RS256) for microservices")
    print("  6. Include minimal payload (avoid sensitive data)")
    print("  7. Implement token refresh mechanism")


if __name__ == "__main__":
    main()
