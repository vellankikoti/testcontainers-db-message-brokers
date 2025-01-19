"""
Custom Docker Image Test Example
This file can be run directly with python3 or with pytest
"""

from sqlalchemy import create_engine, text
from testcontainers.core.container import DockerContainer
import time

# Constants
CUSTOM_IMAGE = "custom-mysql:1.0"
DATABASE_NAME = "hotel"
MYSQL_ROOT_PASSWORD = "test"

class CustomMySQLContainer(DockerContainer):
    """Custom MySQL container implementation."""

    def __init__(self):
        super(CustomMySQLContainer, self).__init__(CUSTOM_IMAGE)
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
        self.wait_for_mysql_ready()
        return self

    def wait_for_mysql_ready(self, timeout=30):
        """Wait for MySQL to be ready to accept connections."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                engine = create_engine(self.get_connection_url())
                with engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                    print("✅ MySQL is ready!")
                    return
            except Exception:
                time.sleep(1)
        raise TimeoutError("MySQL did not become ready within the timeout period.")

def test_preloaded_data(engine):
    """Test that the preloaded data is available in the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM guests ORDER BY guest_id"))
        rows = result.fetchall()
        assert len(rows) == 3, f"Expected 3 rows, but got {len(rows)}"
        print("✅ Preloaded data verified successfully!")

        # Print the rows for debugging
        for row in rows:
            print(row)

def test_custom_configuration(engine):
    """Test that the custom configuration is applied."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE()"))
        database_name = result.scalar()
        assert database_name == DATABASE_NAME, f"Expected database name '{DATABASE_NAME}', but got '{database_name}'"
        print("✅ Custom configuration verified successfully!")

def main():
    """Main function to run tests directly."""
    print("Starting Custom MySQL Container Tests...")

    # Create and start the container
    container = CustomMySQLContainer()
    try:
        container.start()
        print("\nContainer started successfully!")

        # Create engine
        engine = create_engine(container.get_connection_url())

        # Run tests
        print("\nRunning test_preloaded_data:")
        test_preloaded_data(engine)

        print("\nRunning test_custom_configuration:")
        test_custom_configuration(engine)

        print("\n✅ All tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
    finally:
        print("\nStopping container...")
        container.stop()
        print("Container stopped.")

if __name__ == "__main__":
    main()
