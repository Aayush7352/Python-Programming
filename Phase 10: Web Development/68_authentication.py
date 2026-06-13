"""
Authentication patterns demonstration.

Requires: pip install passlib bcrypt
"""
import hashlib
import os
import sys
import time


def hash_password_sha256(password: str, salt: str = None) -> tuple:
    """Hash password with SHA256 and salt."""
    if salt is None:
        salt = os.urandom(32).hex()
    salted = salt + password
    hashed = hashlib.sha256(salted.encode()).hexdigest()
    return hashed, salt


def verify_password_sha256(password: str, hashed: str, salt: str) -> bool:
    """Verify password against SHA256 hash."""
    return hash_password_sha256(password, salt)[0] == hashed


def demonstrate_basic_auth() -> None:
    """Basic username/password authentication."""
    print("=== Basic Authentication ===")
    users_db = {}

    def register(username: str, password: str) -> str:
        if username in users_db:
            return "User already exists"
        hashed, salt = hash_password_sha256(password)
        users_db[username] = {"hashed": hashed, "salt": salt}
        return f"User '{username}' registered"

    def login(username: str, password: str) -> str:
        if username not in users_db:
            return "User not found"
        user = users_db[username]
        if verify_password_sha256(password, user["hashed"], user["salt"]):
            return f"Login successful for '{username}'"
        return "Invalid password"

    print(f"  {register('alice', 'password123')}")
    print(f"  {register('bob', 'secret456')}")

    print(f"  {login('alice', 'password123')}")
    print(f"  {login('alice', 'wrongpass')}")
    print(f"  {login('charlie', 'test')}")


def demonstrate_session_auth() -> None:
    """Session-based authentication with tokens."""
    print("\n=== Session-Based Authentication ===")
    sessions = {}
    users = {"alice": hash_password_sha256("password123")[0]}

    def create_session(username: str) -> str:
        token = hashlib.sha256(f"{username}:{time.time()}:{os.urandom(16).hex()}".encode()).hexdigest()
        sessions[token] = {
            "username": username,
            "created_at": time.time(),
            "expires_at": time.time() + 3600,  # 1 hour
        }
        return token

    def validate_session(token: str) -> str | None:
        session = sessions.get(token)
        if not session:
            return None
        if time.time() > session["expires_at"]:
            del sessions[token]
            return None
        return session["username"]

    def logout(token: str) -> None:
        sessions.pop(token, None)

    token = create_session("alice")
    print(f"  Created session token: {token[:16]}...")

    user = validate_session(token)
    print(f"  Valid session for: {user}")

    expired_token = hashlib.sha256(b"expired").hexdigest()
    sessions[expired_token] = {
        "username": "bob",
        "created_at": 0,
        "expires_at": time.time() - 100,
    }
    print(f"  Expired session: {validate_session(expired_token)}")


def demonstrate_api_key_auth() -> None:
    """API key authentication."""
    print("\n=== API Key Authentication ===")
    import secrets
    api_keys = {}

    def generate_api_key(user_id: str) -> str:
        api_key = f"sk-{secrets.token_hex(32)}"
        api_keys[api_key] = {
            "user_id": user_id,
            "created_at": time.time(),
        }
        return api_key

    def validate_api_key(api_key: str) -> str | None:
        info = api_keys.get(api_key)
        if info:
            return info["user_id"]
        return None

    key = generate_api_key("user_123")
    print(f"  Generated API key: {key[:12]}...{key[-8:]}")

    user = validate_api_key(key)
    print(f"  Valid API key for: {user}")

    print(f"  Invalid key: {validate_api_key('invalid-key')}")


def demonstrate_bcrypt_auth() -> None:
    """Using bcrypt for password hashing."""
    print("\n=== bcrypt Authentication ===")
    try:
        import bcrypt
        password = b"secure_password123"

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        print(f"  Hash: {hashed[:20]}...")

        is_valid = bcrypt.checkpw(password, hashed)
        print(f"  Correct password valid: {is_valid}")

        is_invalid = bcrypt.checkpw(b"wrong_password", hashed)
        print(f"  Wrong password valid: {is_invalid}")
    except ImportError:
        print("  bcrypt not installed (pip install bcrypt)")
        print("  Using SHA256 as fallback")
        hashed, salt = hash_password_sha256("secure_password123")
        print(f"  SHA256 hash: {hashed[:20]}...")


def main():
    demonstrate_basic_auth()
    demonstrate_session_auth()
    demonstrate_api_key_auth()
    demonstrate_bcrypt_auth()

    print("\n=== Authentication Best Practices ===")
    print("  1. Never store passwords in plaintext")
    print("  2. Use strong hashing (bcrypt, argon2)")
    print("  3. Always use salt when hashing")
    print("  4. Implement rate limiting on login")
    print("  5. Use HTTPS in production")
    print("  6. Implement account lockout")
    print("  7. Use secure session management")


if __name__ == "__main__":
    main()
