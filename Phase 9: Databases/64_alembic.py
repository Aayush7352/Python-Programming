"""
Alembic database migration demonstration.

Alembic is a lightweight database migration tool for SQLAlchemy.
This file demonstrates Alembic concepts programmatically.

Requires: pip install alembic sqlalchemy
"""
import os
import sys
import tempfile


def main():
    """Demonstrate Alembic migration concepts."""
    print("=== Alembic Database Migrations ===")
    print("""
Alembic manages database schema changes version by version.

Key Concepts:
  - Migration: a versioned change to the database schema
  - Revision: a single migration file
  - Upgrade: apply a migration
  - Downgrade: revert a migration

Workflow:
  1. alembic init alembic          # Initialize
  2. alembic revision -m "create users table"  # Create migration
  3. alembic upgrade head          # Apply migrations
  4. alembic downgrade -1          # Revert last migration
""")

    print("=== Sample Migration Script ===")
    sample_revision = '''
"""create users table

Revision ID: abc123
Revises: None
Create Date: 2024-01-15 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = "abc123"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the users table."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(200), unique=True, nullable=False),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    """Drop the users table."""
    op.drop_table("users")
'''

    print(sample_revision)

    print("=== Second Migration (add column) ===")
    second_revision = '''
"""add bio column to users

Revision ID: def456
Revises: abc123
Create Date: 2024-01-16 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "def456"
down_revision = "abc123"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add bio column."""
    op.add_column("users", sa.Column("bio", sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove bio column."""
    op.drop_column("users", "bio")
'''

    print(second_revision)

    print("=== Performing Migrations Programmatically ===")
    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy.orm import declarative_base, Session
    except ImportError:
        print("  SQLAlchemy not installed (pip install sqlalchemy)")
        return

    engine = create_engine("sqlite:///:memory:", echo=False)
    Base = declarative_base()

    # Instead of actual alembic, we manually apply migrations
    with engine.connect() as conn:
        # Migration 1: Create users table
        print("\n  Migration 1: Creating users table...")
        conn.execute(text("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(200) UNIQUE NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()
        print("  Table 'users' created")

        # Migration 2: Add bio column
        print("\n  Migration 2: Adding bio column...")
        conn.execute(text("ALTER TABLE users ADD COLUMN bio TEXT"))
        conn.commit()
        print("  Column 'bio' added")

        # Migration 3 (pending): Rename column
        print("\n  Migration 3 (downgrade): Drop bio column...")
        # SQLite doesn't support DROP COLUMN easily, so this is illustrative
        print("  (SQLite: need to recreate table to drop column)")

        # Verify schema
        print("\n=== Final Schema ===")
        result = conn.execute(text("PRAGMA table_info(users)"))
        for row in result:
            print(f"  Column: {row[1]} ({row[2]})")

    print("\n=== Alembic Commands Reference ===")
    print("  alembic init alembic              # Initialize")
    print("  alembic revision --autogenerate -m 'msg'  # Auto-detect changes")
    print("  alembic upgrade head              # Apply all pending")
    print("  alembic upgrade +2                # Apply next 2")
    print("  alembic downgrade -1              # Revert 1 step")
    print("  alembic history                   # Show migration history")
    print("  alembic current                   # Show current revision")


if __name__ == "__main__":
    main()
