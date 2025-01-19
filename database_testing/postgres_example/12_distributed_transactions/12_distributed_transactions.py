"""
Distributed Transactions Test Suite

This module tests distributed transactions across multiple databases using
two-phase commit protocol simulation.
"""

import pytest
import time
from datetime import datetime
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class OrdersDatabase:
    def __init__(self, container):
        self.engine = create_engine(container.get_connection_url())
        self.setup_database()

    def setup_database(self):
        try:
            with self.engine.connect() as connection:
                connection.execute(text("""
                    DROP TABLE IF EXISTS orders CASCADE;
                    DROP TABLE IF EXISTS distributed_transactions CASCADE;

                    CREATE TABLE orders (
                        order_id SERIAL PRIMARY KEY,
                        customer_id INTEGER NOT NULL,
                        total_amount DECIMAL(10,2) NOT NULL,
                        status TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE distributed_transactions (
                        transaction_id TEXT PRIMARY KEY,
                        status TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """))
                connection.commit()
                print("✅ Orders database initialized!")
        except SQLAlchemyError as e:
            print(f"❌ Failed to initialize Orders database: {str(e)}")
            raise


class InventoryDatabase:
    def __init__(self, container):
        self.engine = create_engine(container.get_connection_url())
        self.setup_database()

    def setup_database(self):
        try:
            with self.engine.connect() as connection:
                connection.execute(text("""
                    DROP TABLE IF EXISTS inventory CASCADE;
                    DROP TABLE IF EXISTS distributed_transactions CASCADE;

                    CREATE TABLE inventory (
                        product_id SERIAL PRIMARY KEY,
                        quantity INTEGER NOT NULL,
                        reserved INTEGER DEFAULT 0
                    );

                    CREATE TABLE distributed_transactions (
                        transaction_id TEXT PRIMARY KEY,
                        status TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """))
                connection.commit()
                print("✅ Inventory database initialized!")
        except SQLAlchemyError as e:
            print(f"❌ Failed to initialize Inventory database: {str(e)}")
            raise

    def insert_sample_products(self):
        try:
            with self.engine.connect() as connection:
                connection.execute(text("""
                    INSERT INTO inventory (product_id, quantity) VALUES
                    (1, 100),
                    (2, 50),
                    (3, 75);
                """))
                connection.commit()
                print("✅ Sample inventory data inserted!")
        except SQLAlchemyError as e:
            print(f"❌ Failed to insert sample products: {str(e)}")
            raise


class DistributedTransaction:
    def __init__(self, orders_db, inventory_db):
        self.orders_db = orders_db
        self.inventory_db = inventory_db
        self.transaction_id = datetime.now().strftime("%Y%m%d%H%M%S")

    def prepare(self):
        """First phase: Prepare both databases for the transaction."""
        print(f"\n🔄 Starting prepare phase for transaction {self.transaction_id}")

        try:
            # Prepare Orders database
            with self.orders_db.engine.connect() as conn:
                try:
                    conn.execute(
                        text("INSERT INTO distributed_transactions (transaction_id, status) VALUES (:tid, 'preparing')"),
                        {"tid": self.transaction_id}
                    )
                    conn.commit()
                    print("✅ Orders database prepared successfully")
                except SQLAlchemyError as e:
                    print(f"❌ Failed to prepare Orders database: {str(e)}")
                    return False

            # Prepare Inventory database
            with self.inventory_db.engine.connect() as conn:
                try:
                    conn.execute(
                        text("INSERT INTO distributed_transactions (transaction_id, status) VALUES (:tid, 'preparing')"),
                        {"tid": self.transaction_id}
                    )
                    conn.commit()
                    print("✅ Inventory database prepared successfully")
                except SQLAlchemyError as e:
                    print(f"❌ Failed to prepare Inventory database: {str(e)}")
                    return False

            print("✅ Prepare phase completed successfully")
            return True

        except Exception as e:
            print(f"❌ Prepare phase failed with error: {str(e)}")
            return False

    def commit(self):
        """Second phase: Commit the transaction on both databases."""
        print(f"\n🔄 Starting commit phase for transaction {self.transaction_id}")

        try:
            # Commit on Orders database
            with self.orders_db.engine.connect() as conn:
                conn.execute(
                    text("UPDATE distributed_transactions SET status = 'committed' WHERE transaction_id = :tid"),
                    {"tid": self.transaction_id}
                )
                conn.commit()
                print("✅ Orders database committed successfully")

            # Commit on Inventory database
            with self.inventory_db.engine.connect() as conn:
                conn.execute(
                    text("UPDATE distributed_transactions SET status = 'committed' WHERE transaction_id = :tid"),
                    {"tid": self.transaction_id}
                )
                conn.commit()
                print("✅ Inventory database committed successfully")

            print("✅ Commit phase completed successfully")
            return True

        except SQLAlchemyError as e:
            print(f"❌ Commit phase failed: {str(e)}")
            return False

    def rollback(self):
        """Rollback the transaction on both databases."""
        print(f"\n🔄 Starting rollback for transaction {self.transaction_id}")

        try:
            # Rollback on Orders database
            with self.orders_db.engine.connect() as conn:
                conn.execute(
                    text("UPDATE distributed_transactions SET status = 'rolled_back' WHERE transaction_id = :tid"),
                    {"tid": self.transaction_id}
                )
                conn.commit()
                print("✅ Orders database rolled back successfully")

            # Rollback on Inventory database
            with self.inventory_db.engine.connect() as conn:
                conn.execute(
                    text("UPDATE distributed_transactions SET status = 'rolled_back' WHERE transaction_id = :tid"),
                    {"tid": self.transaction_id}
                )
                conn.commit()
                print("✅ Inventory database rolled back successfully")

            print("✅ Rollback completed successfully")
            return True

        except SQLAlchemyError as e:
            print(f"❌ Rollback failed: {str(e)}")
            return False


def wait_for_database(container, max_attempts=5):
    """Wait for the database to be ready."""
    engine = create_engine(container.get_connection_url())
    for attempt in range(max_attempts):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                return True
        except SQLAlchemyError:
            print(f"Waiting for database to be ready (attempt {attempt + 1}/{max_attempts})...")
            time.sleep(2)
    return False


@pytest.mark.distributed_transactions
def test_distributed_transactions():
    """Test distributed transactions across multiple databases."""
    # Start two PostgreSQL containers
    with PostgresContainer("postgres:15.3") as orders_container, \
         PostgresContainer("postgres:15.3") as inventory_container:

        print("\n🔄 Waiting for databases to be ready...")

        # Wait for both databases to be ready
        assert wait_for_database(orders_container), "Orders database failed to start"
        assert wait_for_database(inventory_container), "Inventory database failed to start"

        try:
            print("\n🔄 Initializing databases...")

            # Initialize databases
            orders_db = OrdersDatabase(orders_container)
            inventory_db = InventoryDatabase(inventory_container)

            # Verify database connections
            with orders_db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("✅ Orders database connection verified")

            with inventory_db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("✅ Inventory database connection verified")

            inventory_db.insert_sample_products()

            # Test successful distributed transaction
            print("\n🔄 Testing successful distributed transaction...")
            dt = DistributedTransaction(orders_db, inventory_db)

            prepare_result = dt.prepare()
            print(f"Prepare phase result: {prepare_result}")
            assert prepare_result, "Prepare phase should succeed"

            commit_result = dt.commit()
            print(f"Commit phase result: {commit_result}")
            assert commit_result, "Commit phase should succeed"

            # Test failed transaction with rollback
            print("\n🔄 Testing failed transaction with rollback...")
            dt_failed = DistributedTransaction(orders_db, inventory_db)

            prepare_result = dt_failed.prepare()
            print(f"Prepare phase result: {prepare_result}")
            assert prepare_result, "Prepare phase should succeed"

            # Simulate a failure before commit
            print("⚠️ Simulating a failure before commit...")
            time.sleep(1)  # Simulate some processing time

            rollback_result = dt_failed.rollback()
            print(f"Rollback result: {rollback_result}")
            assert rollback_result, "Rollback should succeed"

            print("\n✅ All distributed transaction tests completed successfully!")

        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
            raise


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
