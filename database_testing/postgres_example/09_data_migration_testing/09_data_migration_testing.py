"""
Data Migration Testing Suite

This module tests database migrations, including:
- Applying schema changes.
- Verifying data consistency after migrations.
- Ensuring database functionality post-migration.
"""

import pytest
from sqlalchemy import create_engine, text
from testcontainers.core.container import DockerContainer
import time


class MigrationPostgresContainer(DockerContainer):
    """Custom PostgreSQL container for migration testing."""

    def __init__(self):
        super().__init__("custom-postgres:1.0")
        self.with_exposed_ports(5432)
        self.with_env("POSTGRES_DB", "testdb")
        self.with_env("POSTGRES_USER", "testuser")
        self.with_env("POSTGRES_PASSWORD", "testpass")

    def get_connection_url(self):
        """Get the database connection URL."""
        port = self.get_exposed_port(5432)
        return f"postgresql://testuser:testpass@localhost:{port}/testdb"

    def wait_for_database(self):
        """Wait for the database to be ready."""
        max_retries = 10
        retry_interval = 2  # seconds

        for attempt in range(max_retries):
            try:
                engine = create_engine(self.get_connection_url())
                with engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                print("✅ Database is ready!")
                return
            except Exception as e:
                print(f"Waiting for database... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_interval)

        raise RuntimeError("Database did not become ready in time.")


def apply_migration(connection, migration_file):
    """Apply a migration to the database."""
    with open(migration_file, "r") as file:
        migration_sql = file.read()
    connection.execute(text(migration_sql))
    connection.commit()
    print(f"✅ Migration {migration_file} applied successfully!")


@pytest.mark.migration
def test_data_migration():
    """Test database migrations."""
    with MigrationPostgresContainer() as postgres:
        postgres.wait_for_database()

        engine = create_engine(postgres.get_connection_url())
        with engine.connect() as connection:
            # Verify initial schema
            print("\nVerifying initial schema...")
            tables = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)).fetchall()
            print(f"Initial tables: {[table[0] for table in tables]}")
            assert "bookings" in [table[0] for table in tables], "Initial schema is missing the 'bookings' table."

            # Apply migration
            print("\nApplying migration...")
            apply_migration(connection, "migration.sql")

            # Verify new schema
            print("\nVerifying new schema...")
            tables = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)).fetchall()
            print(f"Tables after migration: {[table[0] for table in tables]}")
            assert "payments" in [table[0] for table in tables], "Migration did not create the 'payments' table."

            # Verify data consistency
            print("\nVerifying data consistency...")
            bookings = connection.execute(text("SELECT COUNT(*) FROM bookings;")).scalar()
            print(f"Number of bookings: {bookings}")
            assert bookings > 0, "Data consistency check failed: no bookings found."

            # Test new functionality
            print("\nTesting new functionality...")
            connection.execute(text("""
                INSERT INTO payments (booking_id, amount, payment_date)
                VALUES (1, 100.00, '2024-01-01');
            """))
            connection.commit()
            payments = connection.execute(text("SELECT COUNT(*) FROM payments;")).scalar()
            print(f"Number of payments: {payments}")
            assert payments == 1, "New functionality test failed: payment not recorded."

            print("\n✅ Data migration tests passed successfully!")
