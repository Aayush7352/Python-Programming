import sqlite3
import os


def create_connection(db_path: str) -> sqlite3.Connection:
    """Create a database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(conn: sqlite3.Connection) -> None:
    """Create tables."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    print("  Tables created")


def insert_data(conn: sqlite3.Connection) -> None:
    """Insert sample data."""
    users = [
        ("Alice", "alice@example.com", 30),
        ("Bob", "bob@example.com", 25),
        ("Charlie", "charlie@example.com", 35),
    ]

    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        users
    )
    conn.commit()
    print(f"  Inserted {cursor.rowcount} users")

    posts = [
        (1, "Hello World", "My first post!"),
        (1, "Python Tips", "Some useful tips..."),
        (2, "SQLite Tutorial", "Learning SQLite"),
        (3, "Data Science", "Working with data"),
    ]

    cursor.executemany(
        "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
        posts
    )
    conn.commit()
    print(f"  Inserted {cursor.rowcount} posts")


def query_data(conn: sqlite3.Connection) -> None:
    """Query data with different patterns."""
    print("\n=== All Users ===")
    cursor = conn.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(f"  ID: {row['id']}, Name: {row['name']}, Email: {row['email']}, Age: {row['age']}")

    print("\n=== Users with Posts (JOIN) ===")
    query = """
        SELECT u.name, p.title, p.created_at
        FROM users u
        JOIN posts p ON u.id = p.user_id
        ORDER BY p.created_at DESC
    """
    for row in conn.execute(query):
        print(f"  {row['name']}: '{row['title']}' ({row['created_at']})")

    print("\n=== Parameterized Query ===")
    cursor = conn.execute("SELECT * FROM users WHERE age > ?", (28,))
    for row in cursor:
        print(f"  {row['name']}: {row['age']} years old")


def update_and_delete(conn: sqlite3.Connection) -> None:
    """Update and delete operations."""
    print("\n=== Update ===")
    conn.execute("UPDATE users SET age = ? WHERE name = ?", (31, "Alice"))
    conn.commit()
    print("  Updated Alice's age to 31")

    cursor = conn.execute("SELECT name, age FROM users WHERE name = ?", ("Alice",))
    row = cursor.fetchone()
    print(f"  Verified: {row['name']} is {row['age']}")

    print("\n=== Delete ===")
    conn.execute("DELETE FROM posts WHERE title = ?", ("SQLite Tutorial",))
    conn.commit()
    print("  Deleted 'SQLite Tutorial' post")


def transactions(conn: sqlite3.Connection) -> None:
    """Transaction management."""
    print("\n=== Transactions ===")
    try:
        conn.execute("BEGIN TRANSACTION")
        conn.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                     ("David", "david@example.com", 28))
        conn.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                     ("Eve", "eve@example.com", None))  # will succeed
        conn.commit()
        print("  Transaction committed")
    except Exception as e:
        conn.rollback()
        print(f"  Transaction rolled back: {e}")


def aggregate_queries(conn: sqlite3.Connection) -> None:
    """Aggregate queries."""
    print("\n=== Aggregations ===")
    cursor = conn.execute("""
        SELECT
            COUNT(*) as total_users,
            AVG(age) as avg_age,
            MIN(age) as min_age,
            MAX(age) as max_age
        FROM users
    """)
    row = cursor.fetchone()
    print(f"  Total: {row['total_users']}, Avg Age: {row['avg_age']:.1f}")
    print(f"  Min Age: {row['min_age']}, Max Age: {row['max_age']}")


def main():
    db_path = "/tmp/sqlite_demo.db"

    print("=== SQLite Demo ===")
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = create_connection(db_path)
    print(f"  SQLite version: {sqlite3.sqlite_version}")

    create_tables(conn)
    insert_data(conn)
    query_data(conn)
    update_and_delete(conn)
    transactions(conn)
    aggregate_queries(conn)

    # Using connection as context manager
    print("\n=== Context Manager Usage ===")
    with sqlite3.connect("/tmp/sqlite_demo2.db") as conn2:
        conn2.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, val TEXT)")
        conn2.execute("INSERT INTO test (val) VALUES (?)", ("auto-commit",))
        print("  Auto-committed on context exit")

    conn.close()
    os.remove(db_path)
    os.remove("/tmp/sqlite_demo2.db")


if __name__ == "__main__":
    main()
