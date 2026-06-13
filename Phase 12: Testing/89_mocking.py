"""
Mocking and patching demonstration.

Requires: pip install pytest
"""
import os
import json
import time
from unittest.mock import Mock, patch, MagicMock, PropertyMock, call


class DatabaseClient:
    """Database client to be mocked."""

    def connect(self, host: str, port: int):
        raise NotImplementedError

    def query(self, sql: str):
        raise NotImplementedError

    def insert(self, table: str, data: dict):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class EmailService:
    """Email service to be mocked."""

    def send_email(self, to: str, subject: str, body: str) -> bool:
        raise NotImplementedError

    def send_bulk(self, recipients: list, subject: str, body: str) -> int:
        raise NotImplementedError


class UserService:
    """Service that uses DatabaseClient and EmailService."""

    def __init__(self, db: DatabaseClient, email: EmailService):
        self.db = db
        self.email = email

    def register_user(self, name: str, email: str) -> dict:
        user_data = {"name": name, "email": email, "id": int(time.time())}
        result = self.db.insert("users", user_data)
        self.email.send_email(
            to=email,
            subject="Welcome!",
            body=f"Welcome {name}!",
        )
        return user_data

    def get_user_stats(self) -> dict:
        result = self.db.query("SELECT COUNT(*) as total FROM users")
        return {"total_users": result[0]["total"]} if result else {"total_users": 0}


class ExternalAPIClient:
    """External API client with file operations."""

    def fetch_data(self, url: str) -> dict:
        raise NotImplementedError

    def save_to_file(self, filepath: str, data: dict):
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load_from_file(self, filepath: str) -> dict:
        with open(filepath, "r") as f:
            return json.load(f)


def test_mock_basics():
    """Basic mock creation and usage."""
    print("=== Basic Mock ===")
    mock = Mock()
    mock.return_value = "mocked_value"
    print(f"  mock(): {mock()}")

    mock.some_method.return_value = 42
    print(f"  mock.some_method(): {mock.some_method()}")

    mock.side_effect = [1, 2, 3]
    print(f"  mock() x3: {mock()}, {mock()}, {mock()}")


def test_mock_database():
    """Mock database operations."""
    print("\n=== Mock Database ===")
    db_mock = Mock(spec=DatabaseClient)
    db_mock.insert.return_value = 1
    db_mock.query.return_value = [{"total": 5}]

    email_mock = Mock(spec=EmailService)
    email_mock.send_email.return_value = True

    service = UserService(db_mock, email_mock)
    result = service.register_user("Alice", "alice@example.com")
    print(f"  Registered user: {result}")
    print(f"  insert called: {db_mock.insert.called}")
    print(f"  insert call args: {db_mock.insert.call_args}")

    stats = service.get_user_stats()
    print(f"  User stats: {stats}")

    # Assert calls
    db_mock.insert.assert_called_once()
    email_mock.send_email.assert_called_once()
    db_mock.query.assert_called_once_with("SELECT COUNT(*) as total FROM users")


def test_patch_context_manager():
    """Patching with context manager."""
    print("\n=== Patching with Context Manager ===")

    with patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = "/mocked/path"
        print(f"  os.getcwd(): {os.getcwd()}")

    print(f"  os.getcwd() (after patch): {os.getcwd()}")


def test_patch_decorator():
    """Patching with decorator."""
    @patch("time.time")
    @patch("os.getenv")
    def test_inner(mock_getenv, mock_time):
        mock_time.return_value = 1234567890.0
        mock_getenv.return_value = "mocked_value"

        env = os.getenv("DATABASE_URL")
        print(f"  os.getenv('DATABASE_URL'): {env}")
        print(f"  time.time(): {time.time()}")

    print("\n=== Patching with Decorator ===")
    test_inner()


def test_mock_side_effects():
    """Mock side effects for different behaviors."""
    print("\n=== Mock Side Effects ===")

    mock = Mock()

    # Side effect as function
    def side_effect_func(arg):
        return f"Processed: {arg}"

    mock.side_effect = side_effect_func
    print(f"  mock('test'): {mock('test')}")

    # Side effect as exception
    mock.side_effect = ValueError("Custom error")
    try:
        mock()
    except ValueError as e:
        print(f"  Exception side effect: {e}")

    # Multiple return values
    mock.side_effect = [10, 20, 30, StopIteration]
    print(f"  Iteration: {mock()}, {mock()}, {mock()}")


def test_mock_property():
    """Mock property attributes."""
    print("\n=== Mock Property ===")

    mock = Mock()
    mock.some_property = PropertyMock(return_value="property_value")
    print(f"  mock.some_property: {mock.some_property}")

    mock.configure_mock(name="Alice", age=30)
    print(f"  mock.name: {mock.name}, mock.age: {mock.age}")


def test_mock_file_operations():
    """Mock file operations."""
    print("\n=== Mock File Operations ===")

    mock_api = Mock(spec=ExternalAPIClient)
    mock_api.fetch_data.return_value = {"key": "value"}

    mock_open = MagicMock()
    mock_open.__enter__.return_value.read.return_value = '{"data": "test"}'

    with patch("builtins.open", mock_open):
        data = json.loads('{"data": "test"}')
        print(f"  Read data: {data}")


def test_mock_chaining():
    """Mock method chaining."""
    print("\n=== Method Chaining ===")

    mock = Mock()
    mock.child.method.return_value = "chained_result"
    print(f"  mock.child.method(): {mock.child.method()}")

    # Chain multiple calls
    mock.return_value.child.grandchild.get.return_value = "deeply_nested"
    print(f"  mock().child.grandchild.get(): {mock().child.grandchild.get()}")


def test_spy():
    """Spy on existing objects."""
    print("\n=== Spy Pattern ===")

    original = DatabaseClient()

    # Wrap with mock
    spy = Mock(wraps=original)
    spy.insert.return_value = 99

    # When insert is real:
    # spy.insert("test", {"data": 1})
    print(f"  spy.insert called: {spy.insert.called}")


def main():
    test_mock_basics()
    test_mock_database()
    test_patch_context_manager()
    test_patch_decorator()
    test_mock_side_effects()
    test_mock_property()
    test_mock_file_operations()
    test_mock_chaining()
    test_spy()

    print("\n=== Mocking Best Practices ===")
    print("  1. Use spec to validate method signatures")
    print("  2. Prefer patch context managers over decorators")
    print("  3. Only mock what you own (not third-party)")
    print("  4. Verify calls with assert_called_*")
    print("  5. Use side_effect for dynamic behavior")


if __name__ == "__main__":
    main()
