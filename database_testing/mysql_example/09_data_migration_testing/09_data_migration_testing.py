"""
Data Migration Testing Example

This script tests the migration of data between two database schemas.
It ensures data consistency, validates the new schema, and tests rollback functionality.
"""

import pytest
import time
from sqlalchemy import create_engine, text
from testcontainers.mysql import MySqlContainer

# Constants
MYSQL_VERSION = "mysql:8.0"
DATABASE_NAME = "migration_test"
MYSQL_ROOT_PASSWORD = "test"

def wait_for_mysql_ready(engine, max_retries=10, retry_interval=2):
    """Wait for the MySQL database to be ready."""
    print("\nWaiting for MySQL to be ready...")
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                print("MySQL is ready!")
                return True
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Database not ready yet. Retrying...")
            time.sleep(retry_interval)
    raise RuntimeError("MySQL did not become ready in time.")

@pytest.fixture(scope="module")
def mysql_container():
    """Fixture to provide a MySQL container."""
    with MySqlContainer(MYSQL_VERSION) as container:
        container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        container.with_env("MYSQL_DATABASE", DATABASE_NAME)
        yield container

@pytest.fixture(scope="module")
def engine(mysql_container):
    """Fixture to provide a SQLAlchemy engine."""
    engine = create_engine(mysql_container.get_connection_url())
    wait_for_mysql_ready(engine)
    setup_initial_schema(engine)
    yield engine
    engine.dispose()

def setup_initial_schema(engine):
    """Set up the initial database schema and insert sample data."""
    try:
        print("\nSetting up initial schema...")
        with engine.connect() as connection:
            # Create the initial schema
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            connection.commit()
            print("Created users table.")

            # Insert sample data
            connection.execute(text("""
                INSERT INTO users (name, email) VALUES
                ('Alice', 'alice@example.com'),
                ('Bob', 'bob@example.com'),
                ('Charlie', 'charlie@example.com');
            """))
            connection.commit()
            print("Inserted sample data.")
    except Exception as e:
        print(f"Error setting up initial schema: {e}")
        raise

def migrate_schema(engine):
    """Perform the schema migration."""
    try:
        print("\nStarting schema migration...")
        with engine.connect() as connection:
            # Add a new column
            print("Adding phone column to users table...")
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN phone VARCHAR(15);
            """))
            connection.commit()
            print("Added phone column successfully.")

            # Create a new table
            print("Creating orders table...")
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    total_amount DECIMAL(10,2) NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """))
            connection.commit()
            print("Created orders table successfully.")
    except Exception as e:
        print(f"Error during schema migration: {e}")
        raise

def rollback_migration(engine):
    """Rollback the schema migration."""
    try:
        print("\nStarting migration rollback...")
        with engine.connect() as connection:
            # Drop the new table
            print("Dropping orders table...")
            connection.execute(text("DROP TABLE IF EXISTS orders;"))
            connection.commit()
            print("Dropped orders table successfully.")

            # Remove the new column
            print("Removing phone column from users table...")
            connection.execute(text("ALTER TABLE users DROP COLUMN phone;"))
            connection.commit()
            print("Removed phone column successfully.")
    except Exception as e:
        print(f"Error during migration rollback: {e}")
        raise

def validate_migration(engine):
    """Validate the migrated schema."""
    try:
        print("\nValidating migration...")
        with engine.connect() as connection:
            # Check if the new column exists
            result = connection.execute(text("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'phone';
            """)).fetchone()
            assert result is not None, "Migration failed: 'phone' column not found in 'users' table."
            print("Validated phone column exists.")

            # Check if the new table exists
            result = connection.execute(text("""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = 'orders';
            """)).fetchone()
            assert result is not None, "Migration failed: 'orders' table not found."
            print("Validated orders table exists.")
    except Exception as e:
        print(f"Error during migration validation: {e}")
        raise

def validate_rollback(engine):
    """Validate the rollback was successful."""
    try:
        print("\nValidating rollback...")
        with engine.connect() as connection:
            # Check if the new column was removed
            result = connection.execute(text("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'phone';
            """)).fetchone()
            assert result is None, "Rollback failed: 'phone' column still exists in 'users' table."
            print("Validated phone column was removed.")

            # Check if the new table was dropped
            result = connection.execute(text("""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = 'orders';
            """)).fetchone()
            assert result is None, "Rollback failed: 'orders' table still exists."
            print("Validated orders table was dropped.")
    except Exception as e:
        print(f"Error during rollback validation: {e}")
        raise

@pytest.mark.migration
def test_data_migration(engine):
    """Test the data migration process."""
    try:
        # Perform the migration
        migrate_schema(engine)

        # Validate the migration
        validate_migration(engine)

        # Rollback the migration
        rollback_migration(engine)

        # Validate rollback
        validate_rollback(engine)

        print("\nMigration test completed successfully!")
    except Exception as e:
        print(f"\nMigration test failed: {e}")
        raise

if __name__ == "__main__":
    print("\nStarting data migration testing...")
    try:
        # Create and configure the MySQL container
        with MySqlContainer(MYSQL_VERSION) as container:
            container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
            container.with_env("MYSQL_DATABASE", DATABASE_NAME)
            
            # Create engine and run tests
            engine = create_engine(container.get_connection_url())
            wait_for_mysql_ready(engine)
            setup_initial_schema(engine)
            
            print("\nRunning migration test...")
            test_data_migration(engine)
            
    except Exception as e:
        print(f"\nTest execution failed: {e}")
        raise
    finally:
        print("\nTest execution completed.")
