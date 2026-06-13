"""
Integration testing patterns and examples.

Integration tests verify that different components work together correctly.
"""
import os
import json
import tempfile
import sqlite3
from typing import List, Dict, Optional


class UserRepository:
    """User data access layer."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    age INTEGER
                )
            """)

    def create(self, name: str, email: str, age: int) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (name, email, age)
            )
            return {"id": cursor.lastrowid, "name": name, "email": email, "age": age}

    def get_by_id(self, user_id: int) -> Optional[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all(self) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM users")
            return [dict(row) for row in cursor.fetchall()]

    def update(self, user_id: int, data: dict) -> Optional[dict]:
        fields = ", ".join(f"{k} = ?" for k in data)
        values = list(data.values()) + [user_id]
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(f"UPDATE users SET {fields} WHERE id = ?", values)
            return self.get_by_id(user_id)

    def delete(self, user_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return cursor.rowcount > 0


class EmailValidator:
    """Email validation service."""

    @staticmethod
    def validate(email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1]


class UserService:
    """Service layer combining UserRepository and validators."""

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, name: str, email: str, age: int) -> dict:
        if not name or len(name) < 2:
            raise ValueError("Name must be at least 2 characters")
        if not EmailValidator.validate(email):
            raise ValueError(f"Invalid email: {email}")
        if age < 0 or age > 150:
            raise ValueError(f"Invalid age: {age}")

        return self.repo.create(name, email, age)

    def bulk_register(self, users: List[dict]) -> List[dict]:
        return [self.register_user(**u) for u in users]


# Integration test functions
def test_user_repository_integration():
    """Integration test: UserRepository with real SQLite."""
    print("=== User Repository Integration Test ===")

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        repo = UserRepository(db_path)

        # Create
        user = repo.create("Alice", "alice@example.com", 30)
        assert user["id"] > 0
        print(f"  Created user: {user}")

        # Read
        retrieved = repo.get_by_id(user["id"])
        assert retrieved["name"] == "Alice"
        print(f"  Retrieved user: {retrieved}")

        # Update
        updated = repo.update(user["id"], {"age": 31})
        assert updated["age"] == 31
        print(f"  Updated user: {updated}")

        # List all
        all_users = repo.get_all()
        assert len(all_users) >= 1
        print(f"  All users: {all_users}")

        # Delete
        deleted = repo.delete(user["id"])
        assert deleted == True
        assert repo.get_by_id(user["id"]) is None
        print(f"  Delete successful: {deleted}")

        print("  All repository tests PASSED")

    finally:
        os.unlink(db_path)


def test_user_service_integration():
    """Integration test: UserService with real UserRepository."""
    print("\n=== User Service Integration Test ===")

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        repo = UserRepository(db_path)
        service = UserService(repo)

        # Valid registration
        user = service.register_user("Bob", "bob@example.com", 25)
        assert user["name"] == "Bob"
        print(f"  Registered: {user}")

        # Invalid email
        try:
            service.register_user("Charlie", "invalid-email", 20)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            print(f"  Correctly rejected invalid email: {e}")

        # Invalid age
        try:
            service.register_user("Charlie", "charlie@example.com", -5)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            print(f"  Correctly rejected invalid age: {e}")

        # Short name
        try:
            service.register_user("X", "x@example.com", 20)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            print(f"  Correctly rejected short name: {e}")

        # Bulk registration
        users = service.bulk_register([
            {"name": "Charlie", "email": "charlie@example.com", "age": 35},
            {"name": "Diana", "email": "diana@example.com", "age": 28},
        ])
        assert len(users) == 2
        print(f"  Bulk registered: {len(users)} users")

        print("  All service tests PASSED")

    finally:
        os.unlink(db_path)


def test_end_to_end():
    """End-to-end integration test."""
    print("\n=== End-to-End Integration Test ===")

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        repo = UserRepository(db_path)
        service = UserService(repo)

        # Simulate complete workflow
        users_data = [
            {"name": "Alice", "email": "alice@example.com", "age": 30},
            {"name": "Bob", "email": "bob@example.com", "age": 25},
        ]

        created_users = service.bulk_register(users_data)

        # Verify all were created
        all_users = repo.get_all()
        assert len(all_users) == 2
        print(f"  Created {len(all_users)} users")

        # Verify data integrity
        assert all_users[0]["name"] in ["Alice", "Bob"]
        assert all_users[1]["email"].endswith("@example.com")
        print(f"  Data integrity verified")

        # Update and verify
        updated = repo.update(created_users[0]["id"], {"age": 31})
        assert updated["age"] == 31
        print(f"  Update verified: {updated}")

        print("  End-to-end tests PASSED")

    finally:
        os.unlink(db_path)


def main():
    print("=== Integration Testing ===")
    print("""
Integration testing verifies that components work together.
Unlike unit tests, integration tests use real dependencies
(Database, network, filesystem).

Key principles:
  - Test real interactions between components
  - Use temporary resources (temp files, test databases)
  - Clean up after tests
  - Don't mock infrastructure
  - Test happy paths and error scenarios
""")

    test_user_repository_integration()
    test_user_service_integration()
    test_end_to_end()

    print("\n=== All Integration Tests PASSED ===")


if __name__ == "__main__":
    main()
