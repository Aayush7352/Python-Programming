from contextlib import contextmanager
import time


class FileManager:
    """Context manager class for file handling."""

    def __init__(self, filepath: str, mode: str = "r"):
        self.filepath = filepath
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"  Opening {self.filepath} with mode '{self.mode}'")
        self.file = open(self.filepath, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            print(f"  Closed {self.filepath}")
        if exc_type:
            print(f"  Exception handled: {exc_type.__name__}: {exc_val}")
        return False  # Don't suppress exceptions


class Timer:
    """Context manager for timing code blocks."""

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"  Elapsed: {self.elapsed:.4f} seconds")
        return False


class DatabaseTransaction:
    """Simulated database transaction context manager."""

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.operations = []

    def add_operation(self, op: str):
        self.operations.append(op)

    def __enter__(self):
        print(f"  Beginning transaction on {self.db_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"  Rolling back transaction due to: {exc_val}")
            self.operations.clear()
        else:
            print(f"  Committing {len(self.operations)} operations")
        return True  # Suppress exceptions in commit


@contextmanager
def temporary_change(obj, attr, new_value):
    """Context manager using decorator pattern."""
    old_value = getattr(obj, attr)
    setattr(obj, attr, new_value)
    print(f"  Changed {attr} from {old_value} to {new_value}")
    try:
        yield
    finally:
        setattr(obj, attr, old_value)
        print(f"  Restored {attr} back to {old_value}")


class Config:
    def __init__(self):
        self.debug = False
        self.timeout = 30


class ManagedResource:
    """Resource with acquire/release pattern."""

    def __init__(self, name: str):
        self.name = name
        print(f"  Initializing resource: {name}")

    def __enter__(self):
        print(f"  Acquiring: {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  Releasing: {self.name}")
        if exc_type:
            print(f"  Exception during use: {exc_val}")
        return False

    def use(self):
        print(f"  Using resource: {self.name}")


def main():
    print("=== Class-based Context Manager ===")
    with FileManager("/tmp/test.txt", "w") as f:
        f.write("Hello, Context Manager!")

    with FileManager("/tmp/test.txt", "r") as f:
        content = f.read()
        print(f"  Read: {content}")

    print("\n=== Timer Context Manager ===")
    with Timer():
        total = sum(i ** 2 for i in range(1000000))
        print(f"  Sum computed: {total}")

    print("\n=== Database Transaction ===")
    with DatabaseTransaction("main_db") as txn:
        txn.add_operation("INSERT INTO users (name) VALUES ('Alice')")
        txn.add_operation("UPDATE accounts SET balance = 1000")
        print(f"  Operations queued: {len(txn.operations)}")

    # Transaction with error (rollback)
    with DatabaseTransaction("main_db") as txn:
        txn.add_operation("INSERT INTO users (name) VALUES ('Bob')")
        raise ValueError("Connection lost")

    print("\n=== @contextmanager Decorator ===")
    config = Config()
    print(f"  Before: debug={config.debug}, timeout={config.timeout}")
    with temporary_change(config, "debug", True):
        with temporary_change(config, "timeout", 60):
            print(f"  Inside: debug={config.debug}, timeout={config.timeout}")
    print(f"  After: debug={config.debug}, timeout={config.timeout}")

    print("\n=== Resource Pattern ===")
    with ManagedResource("Network Connection") as res:
        res.use()

    # Nested context managers
    print("\n=== Nested Context Managers ===")
    with Timer():
        with ManagedResource("Database Pool") as db:
            db.use()


if __name__ == "__main__":
    main()
