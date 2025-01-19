"""
Basic MySQL Testing Example

This module demonstrates basic MySQL container testing using testcontainers,
including:
- Container setup and configuration
- Basic CRUD operations
- Simple assertions
"""

import pytest
import time
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from sqlalchemy import create_engine, text

# Constants
MYSQL_VERSION = "mysql:8.0"
DATABASE_NAME = "hotel"
MYSQL_ROOT_PASSWORD = "test"

class MySQLContainer(DockerContainer):
    """Custom MySQL container implementation."""

    def __init__(self):
        super(MySQLContainer, self).__init__(MYSQL_VERSION)
        self.with_exposed_ports(3306)
        self.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        self.with_env("MYSQL_DATABASE", DATABASE_NAME)

    def get_connection_url(self):
        """Get the MySQL connection URL."""
        port = self.get_exposed_port(3306)
        return f"mysql+mysqlconnector://root:{MYSQL_ROOT_PASSWORD}@localhost:{port}/{DATABASE_NAME}"

    def start(self):
        """Start the container and wait for MySQL to be ready."""
        super().start()
        wait_for_logs(self, "ready for connections", timeout=30)
        # Additional wait to ensure MySQL is fully ready
        time.sleep(2)
        return self

def setup_database(connection):
    """Initialize the database schema with a guests table."""
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS guests (
            guest_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20)
        );
    """))
    connection.commit()

def insert_sample_data(connection):
    """Insert sample guest data."""
    connection.execute(text("""
        INSERT INTO guests (first_name, last_name, email, phone) VALUES
        ('John', 'Doe', 'john.doe@email.com', '123-456-7890'),
        ('Jane', 'Smith', 'jane.smith@email.com', '098-765-4321');
    """))
    connection.commit()

@pytest.mark.basic
def test_mysql_basic_operations():
    """Test basic MySQL operations using testcontainers."""
    # Start MySQL container
    mysql = MySQLContainer()
    mysql.start()

    try:
        # Create database connection with retry logic
        max_retries = 5
        retry_delay = 2
        last_exception = None

        for attempt in range(max_retries):
            try:
                engine = create_engine(mysql.get_connection_url())
                with engine.connect() as connection:
                    # Setup database
                    setup_database(connection)

                    # Test INSERT operation
                    insert_sample_data(connection)

                    # Test SELECT operation
                    result = connection.execute(text("SELECT COUNT(*) FROM guests"))
                    count = result.scalar()
                    assert count == 2, f"Expected 2 guests, but found {count}"

                    # Test UPDATE operation
                    connection.execute(text("""
                        UPDATE guests 
                        SET phone = '555-0123' 
                        WHERE email = 'john.doe@email.com'
                    """))
                    connection.commit()

                    # Verify UPDATE
                    result = connection.execute(text("""
                        SELECT phone 
                        FROM guests 
                        WHERE email = 'john.doe@email.com'
                    """))
                    phone = result.scalar()
                    assert phone == '555-0123', f"Expected updated phone '555-0123', but found {phone}"

                    # Test DELETE operation
                    connection.execute(text("""
                        DELETE FROM guests 
                        WHERE email = 'jane.smith@email.com'
                    """))
                    connection.commit()

                    # Verify DELETE
                    result = connection.execute(text("SELECT COUNT(*) FROM guests"))
                    count = result.scalar()
                    assert count == 1, f"Expected 1 guest after deletion, but found {count}"

                    print("✅ All basic MySQL operations passed!")
                    break
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise last_exception

    finally:
        mysql.stop()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
