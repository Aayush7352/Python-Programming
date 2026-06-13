from abc import ABC, abstractmethod
from typing import List, Optional


class Database(ABC):
    """Abstract base class for database operations."""

    @abstractmethod
    def connect(self, connection_string: str) -> bool:
        """Establish a database connection."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close the database connection."""
        pass

    @abstractmethod
    def execute(self, query: str) -> List[dict]:
        """Execute a query and return results."""
        pass

    @abstractmethod
    def insert(self, table: str, data: dict) -> int:
        """Insert a record and return the ID."""
        pass

    def transaction(self) -> "Transaction":
        """Non-abstract: provides a transaction helper."""
        return Transaction(self)


class Transaction:
    """Helper class for database transactions."""

    def __init__(self, db: Database):
        self.db = db
        self.operations: list = []

    def add(self, query: str) -> None:
        self.operations.append(query)

    def commit(self) -> List[dict]:
        results = []
        for op in self.operations:
            results.append(self.db.execute(op))
        return results


class PostgreSQL(Database):
    """Concrete implementation for PostgreSQL."""

    def __init__(self):
        self.connected = False

    def connect(self, connection_string: str) -> bool:
        print(f"PostgreSQL: Connecting to {connection_string}")
        self.connected = True
        return True

    def disconnect(self) -> None:
        print("PostgreSQL: Disconnecting")
        self.connected = False

    def execute(self, query: str) -> List[dict]:
        if not self.connected:
            raise RuntimeError("Not connected to database")
        print(f"PostgreSQL: Executing '{query}'")
        return [{"result": "data"}]

    def insert(self, table: str, data: dict) -> int:
        print(f"PostgreSQL: Inserting into {table}: {data}")
        return 1


class SQLite(Database):
    """Concrete implementation for SQLite."""

    def __init__(self):
        self.connected = False

    def connect(self, connection_string: str) -> bool:
        print(f"SQLite: Connecting to {connection_string}")
        self.connected = True
        return True

    def disconnect(self) -> None:
        print("SQLite: Disconnecting")
        self.connected = False

    def execute(self, query: str) -> List[dict]:
        if not self.connected:
            raise RuntimeError("Not connected")
        print(f"SQLite: Executing '{query}'")
        return [{"id": 1, "name": "test"}]

    def insert(self, table: str, data: dict) -> int:
        print(f"SQLite: Inserting into {table}: {data}")
        return 1


def main():
    print("=== Database Abstraction ===")
    databases: List[Database] = [PostgreSQL(), SQLite()]

    for db in databases:
        print(f"\nUsing {db.__class__.__name__}:")
        db.connect("localhost:5432/mydb")
        result = db.execute("SELECT * FROM users")
        print(f"  Query result: {result}")
        id_val = db.insert("users", {"name": "Alice", "age": 30})
        print(f"  Inserted with ID: {id_val}")
        db.disconnect()

    # Using the abstract interface with a transaction
    print("\n=== Transaction Abstraction ===")
    pg = PostgreSQL()
    pg.connect("localhost:5432/mydb")
    txn = pg.transaction()
    txn.add("INSERT INTO users (name) VALUES ('Bob')")
    txn.add("UPDATE users SET age = 25 WHERE name = 'Bob'")
    results = txn.commit()
    print(f"Transaction results: {results}")
    pg.disconnect()

    # Abstract classes cannot be instantiated
    print("\n=== Abstract class cannot be instantiated ===")
    try:
        db = Database()
    except TypeError as e:
        print(f"  Correctly raises: {e}")


if __name__ == "__main__":
    main()
