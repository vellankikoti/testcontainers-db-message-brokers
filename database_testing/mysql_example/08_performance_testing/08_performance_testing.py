"""
Performance Testing Example for MySQL Database Operations
Tests the performance of various database operations using metrics and timing.
"""

import pytest
import time
import statistics
from sqlalchemy import create_engine, text
from testcontainers.mysql import MySqlContainer
from datetime import datetime

# Constants
MYSQL_VERSION = "mysql:8.0"
DATABASE_NAME = "performance_test"
MYSQL_ROOT_PASSWORD = "test"
NUM_ITERATIONS = 5  # Number of times to run each test for averaging

class PerformanceMetrics:
    """Class to track and calculate performance metrics"""

    def __init__(self):
        self.timings = []
        self.start_time = None

    def start(self):
        """Start timing"""
        self.start_time = time.perf_counter()

    def stop(self):
        """Stop timing and record duration"""
        if self.start_time is None:
            raise RuntimeError("Timer was not started")
        duration = time.perf_counter() - self.start_time
        self.timings.append(duration)
        self.start_time = None
        return duration

    def get_statistics(self):
        """Calculate statistics from recorded timings"""
        if not self.timings:
            return None
        return {
            'min': min(self.timings),
            'max': max(self.timings),
            'avg': statistics.mean(self.timings),
            'median': statistics.median(self.timings)
        }

@pytest.fixture(scope="module")
def mysql_container():
    """Fixture to provide a MySQL container"""
    with MySqlContainer(MYSQL_VERSION) as container:
        container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        container.with_env("MYSQL_DATABASE", DATABASE_NAME)
        yield container

@pytest.fixture(scope="module")
def engine(mysql_container):
    """Fixture to provide a SQLAlchemy engine"""
    engine = create_engine(mysql_container.get_connection_url())
    setup_database(engine)
    yield engine
    engine.dispose()

def setup_database(engine):
    """Initialize database schema and insert sample data"""
    with engine.connect() as connection:
        # Create customers table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        connection.commit()

        # Create orders table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """))
        connection.commit()

        # Insert sample data
        for i in range(1000):
            connection.execute(
                text("INSERT INTO customers (name, email) VALUES (:name, :email)"),
                {"name": f"Customer {i}", "email": f"customer{i}@example.com"}
            )
        connection.commit()

def run_performance_test(engine, query, params=None):
    """Execute a query multiple times and measure performance"""
    metrics = PerformanceMetrics()

    for _ in range(NUM_ITERATIONS):
        with engine.connect() as connection:
            metrics.start()
            if params:
                connection.execute(text(query), params)
            else:
                connection.execute(text(query))
            duration = metrics.stop()
            print(f"Query executed in {duration:.4f} seconds")

    return metrics.get_statistics()

@pytest.mark.performance
def test_select_performance(engine):
    """Test SELECT query performance"""
    query = "SELECT * FROM customers LIMIT 100"
    stats = run_performance_test(engine, query)

    print("\nSELECT Performance Statistics:")
    print(f"Min: {stats['min']:.4f}s")
    print(f"Max: {stats['max']:.4f}s")
    print(f"Avg: {stats['avg']:.4f}s")
    print(f"Median: {stats['median']:.4f}s")

    assert stats['avg'] < 1.0, "SELECT query average time exceeded threshold"

@pytest.mark.performance
def test_insert_performance(engine):
    """Test INSERT query performance"""
    query = """
    INSERT INTO orders (customer_id, total_amount)
    VALUES (:customer_id, :amount)
    """

    stats = run_performance_test(
        engine,
        query,
        {"customer_id": 1, "amount": 99.99}
    )

    print("\nINSERT Performance Statistics:")
    print(f"Min: {stats['min']:.4f}s")
    print(f"Max: {stats['max']:.4f}s")
    print(f"Avg: {stats['avg']:.4f}s")
    print(f"Median: {stats['median']:.4f}s")

    assert stats['avg'] < 0.5, "INSERT query average time exceeded threshold"

@pytest.mark.performance
def test_join_performance(engine):
    """Test JOIN query performance"""
    query = """
    SELECT c.name, o.total_amount
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    LIMIT 100
    """

    stats = run_performance_test(engine, query)

    print("\nJOIN Performance Statistics:")
    print(f"Min: {stats['min']:.4f}s")
    print(f"Max: {stats['max']:.4f}s")
    print(f"Avg: {stats['avg']:.4f}s")
    print(f"Median: {stats['median']:.4f}s")

    assert stats['avg'] < 1.5, "JOIN query average time exceeded threshold"

if __name__ == "__main__":
    # Create engine and run tests
    with MySqlContainer(MYSQL_VERSION) as container:
        container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        container.with_env("MYSQL_DATABASE", DATABASE_NAME)
        engine = create_engine(container.get_connection_url())
        setup_database(engine)

        print("\nRunning performance tests...")
        test_select_performance(engine)
        test_insert_performance(engine)
        test_join_performance(engine)
