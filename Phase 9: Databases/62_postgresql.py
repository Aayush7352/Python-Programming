"""
PostgreSQL database interaction.

Requires: pip install psycopg2-binary
"""
import os
import sys


def main():
    """PostgreSQL demonstration using psycopg2."""
    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        print("psycopg2 is not installed.")
        print("Install with: pip install psycopg2-binary")
        print("\nThis demo shows PostgreSQL patterns using psycopg2.")
        print("The code is structured to work with a PostgreSQL database.")
        sys.exit(1)

    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "dbname": os.getenv("DB_NAME", "testdb"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres"),
    }

    print("=== PostgreSQL with psycopg2 ===")
    print(f"  Connecting to {db_config['host']}:{db_config['port']}/{db_config['dbname']}")

    try:
        conn = psycopg2.connect(**db_config)
        print("  Connected successfully!")

        conn.autocommit = False

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    department VARCHAR(50),
                    salary NUMERIC(10, 2),
                    hire_date DATE DEFAULT CURRENT_DATE
                )
            """)

            # Batch insert
            employees = [
                ("Alice Smith", "Engineering", 85000.00),
                ("Bob Jones", "Marketing", 72000.00),
                ("Charlie Brown", "Engineering", 92000.00),
                ("Diana Ross", "HR", 65000.00),
            ]

            psycopg2.extras.execute_values(
                cur,
                "INSERT INTO employees (name, department, salary) VALUES %s",
                employees
            )
            conn.commit()
            print(f"  Inserted {len(employees)} employees")

            # Query with different fetch methods
            cur.execute("SELECT * FROM employees ORDER BY salary DESC")

            print("\n=== All Employees (sorted by salary) ===")
            for row in cur.fetchall():
                print(f"  {row[0]}: {row[1]} - {row[2]} (${row[3]:.2f})")

            # Named columns with DictCursor
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as dict_cur:
                dict_cur.execute("""
                    SELECT department,
                           COUNT(*) as count,
                           AVG(salary) as avg_salary
                    FROM employees
                    GROUP BY department
                """)
                print("\n=== Department Summary ===")
                for row in dict_cur.fetchall():
                    print(f"  {row['department']}: {row['count']} employees, "
                          f"Avg Salary: ${row['avg_salary']:.2f}")

            # Parameterized queries
            dept = "Engineering"
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM employees WHERE department = %s", (dept,))
                eng_emps = cur.fetchall()
                print(f"\n=== {dept} Employees ===")
                for emp in eng_emps:
                    print(f"  {emp['name']}: ${emp['salary']:.2f}")

        conn.close()
        print("\n  Connection closed.")

    except psycopg2.OperationalError as e:
        print(f"\n  Could not connect to PostgreSQL: {e}")
        print("  Make sure PostgreSQL is running and accessible.")
    except Exception as e:
        print(f"\n  Error: {e}")


if __name__ == "__main__":
    main()
