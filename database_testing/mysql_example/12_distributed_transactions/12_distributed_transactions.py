"""
Distributed Transactions Testing Example

This script demonstrates testing distributed transactions across multiple MySQL databases
using two-phase commit protocol simulation.
"""

import pytest
import time
from sqlalchemy import create_engine, text
from testcontainers.mysql import MySqlContainer
from contextlib import contextmanager

# Constants
MYSQL_VERSION = "mysql:8.0"
MYSQL_ROOT_PASSWORD = "test"

class OrdersDatabase:
    """Manages the orders database operations."""
    
    def __init__(self, container):
        self.container = container
        self.engine = create_engine(container.get_connection_url())
        self.setup_database()

    def setup_database(self):
        """Initialize the orders database schema."""
        with self.engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    status VARCHAR(50) DEFAULT 'pending'
                );
            """))
            connection.commit()

    def prepare_order(self, product_id, quantity):
        """Prepare an order for the two-phase commit."""
        with self.engine.begin() as connection:
            result = connection.execute(
                text("""
                    INSERT INTO orders (product_id, quantity, status)
                    VALUES (:product_id, :quantity, 'preparing')
                    RETURNING order_id;
                """),
                {"product_id": product_id, "quantity": quantity}
            )
            order_id = result.scalar()
            return order_id

    def commit_order(self, order_id):
        """Commit the order in the final phase."""
        with self.engine.begin() as connection:
            connection.execute(
                text("UPDATE orders SET status = 'committed' WHERE order_id = :order_id"),
                {"order_id": order_id}
            )

    def rollback_order(self, order_id):
        """Rollback the order if any phase fails."""
        with self.engine.begin() as connection:
            connection.execute(
                text("UPDATE orders SET status = 'rolled_back' WHERE order_id = :order_id"),
                {"order_id": order_id}
            )

class InventoryDatabase:
    """Manages the inventory database operations."""
    
    def __init__(self, container):
        self.container = container
        self.engine = create_engine(container.get_connection_url())
        self.setup_database()

    def setup_database(self):
        """Initialize the inventory database schema."""
        with self.engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS inventory (
                    product_id INT PRIMARY KEY,
                    quantity INT NOT NULL,
                    reserved INT DEFAULT 0
                );
            """))
            connection.commit()
            
            # Insert sample inventory data
            connection.execute(text("""
                INSERT INTO inventory (product_id, quantity)
                VALUES (1, 100), (2, 50)
                ON DUPLICATE KEY UPDATE quantity = VALUES(quantity);
            """))
            connection.commit()

    def prepare_inventory(self, product_id, quantity):
        """Prepare inventory reservation for the two-phase commit."""
        with self.engine.begin() as connection:
            result = connection.execute(
                text("""
                    SELECT quantity, reserved
                    FROM inventory
                    WHERE product_id = :product_id
                    FOR UPDATE;
                """),
                {"product_id": product_id}
            ).fetchone()

            if not result:
                raise ValueError(f"Product {product_id} not found")

            available = result[0] - result[1]
            if available < quantity:
                raise ValueError(f"Insufficient inventory for product {product_id}")

            connection.execute(
                text("""
                    UPDATE inventory
                    SET reserved = reserved + :quantity
                    WHERE product_id = :product_id;
                """),
                {"product_id": product_id, "quantity": quantity}
            )
            return True

    def commit_inventory(self, product_id, quantity):
        """Commit the inventory changes in the final phase."""
        with self.engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE inventory
                    SET quantity = quantity - :quantity,
                        reserved = reserved - :quantity
                    WHERE product_id = :product_id;
                """),
                {"product_id": product_id, "quantity": quantity}
            )

    def rollback_inventory(self, product_id, quantity):
        """Rollback the inventory reservation if any phase fails."""
        with self.engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE inventory
                    SET reserved = reserved - :quantity
                    WHERE product_id = :product_id;
                """),
                {"product_id": product_id, "quantity": quantity}
            )

class DistributedTransaction:
    """Manages distributed transactions across orders and inventory databases."""
    
    def __init__(self, orders_db, inventory_db):
        self.orders_db = orders_db
        self.inventory_db = inventory_db

    def process_order(self, product_id, quantity):
        """Process an order using two-phase commit protocol."""
        try:
            # Phase 1: Prepare
            print("\nPreparing distributed transaction...")
            order_id = self.orders_db.prepare_order(product_id, quantity)
            self.inventory_db.prepare_inventory(product_id, quantity)
            print("Preparation phase completed successfully")

            # Phase 2: Commit
            print("\nCommitting distributed transaction...")
            self.orders_db.commit_order(order_id)
            self.inventory_db.commit_inventory(product_id, quantity)
            print("Commit phase completed successfully")
            return order_id

        except Exception as e:
            print(f"\nError during distributed transaction: {e}")
            print("Rolling back changes...")
            if 'order_id' in locals():
                self.orders_db.rollback_order(order_id)
            self.inventory_db.rollback_inventory(product_id, quantity)
            raise

@pytest.fixture(scope="function")
def distributed_databases():
    """Fixture to provide distributed database setup."""
    orders_container = MySqlContainer(MYSQL_VERSION)
    inventory_container = MySqlContainer(MYSQL_VERSION)
    
    orders_container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
    orders_container.with_env("MYSQL_DATABASE", "orders")
    inventory_container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
    inventory_container.with_env("MYSQL_DATABASE", "inventory")

    orders_container.start()
    inventory_container.start()

    orders_db = OrdersDatabase(orders_container)
    inventory_db = InventoryDatabase(inventory_container)
    
    yield orders_db, inventory_db

    orders_db.engine.dispose()
    inventory_db.engine.dispose()
    orders_container.stop()
    inventory_container.stop()

@pytest.mark.distributed
def test_successful_distributed_transaction(distributed_databases):
    """Test successful distributed transaction processing."""
    orders_db, inventory_db = distributed_databases
    dt = DistributedTransaction(orders_db, inventory_db)

    # Process a valid order
    order_id = dt.process_order(product_id=1, quantity=10)

    # Verify order status
    with orders_db.engine.connect() as conn:
        order_status = conn.execute(
            text("SELECT status FROM orders WHERE order_id = :order_id"),
            {"order_id": order_id}
        ).scalar()
        assert order_status == 'committed'

    # Verify inventory update
    with inventory_db.engine.connect() as conn:
        inventory = conn.execute(
            text("SELECT quantity, reserved FROM inventory WHERE product_id = 1")
        ).fetchone()
        assert inventory[0] == 90  # Initial 100 - 10
        assert inventory[1] == 0   # No remaining reservations

@pytest.mark.distributed
def test_failed_distributed_transaction(distributed_databases):
    """Test rollback of distributed transaction on failure."""
    orders_db, inventory_db = distributed_databases
    dt = DistributedTransaction(orders_db, inventory_db)

    # Attempt to process an order with insufficient inventory
    with pytest.raises(ValueError) as exc_info:
        dt.process_order(product_id=2, quantity=100)  # More than available stock
    assert "Insufficient inventory" in str(exc_info.value)

    # Verify no changes in inventory
    with inventory_db.engine.connect() as conn:
        inventory = conn.execute(
            text("SELECT quantity, reserved FROM inventory WHERE product_id = 2")
        ).fetchone()
        assert inventory[0] == 50  # Original quantity unchanged
        assert inventory[1] == 0   # No reservations

def run_distributed_test():
    """Run the distributed transaction test directly."""
    print("\nStarting distributed transaction test...")
    orders_container = None
    inventory_container = None
    try:
        # Set up containers
        orders_container = MySqlContainer(MYSQL_VERSION)
        inventory_container = MySqlContainer(MYSQL_VERSION)
        
        orders_container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        orders_container.with_env("MYSQL_DATABASE", "orders")
        inventory_container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        inventory_container.with_env("MYSQL_DATABASE", "inventory")

        orders_container.start()
        inventory_container.start()

        # Initialize databases
        orders_db = OrdersDatabase(orders_container)
        inventory_db = InventoryDatabase(inventory_container)
        dt = DistributedTransaction(orders_db, inventory_db)

        # Test successful transaction
        print("\nTesting successful transaction...")
        order_id = dt.process_order(product_id=1, quantity=10)
        print(f"Order {order_id} processed successfully")

        # Test failed transaction
        print("\nTesting failed transaction...")
        try:
            dt.process_order(product_id=2, quantity=100)
        except ValueError as e:
            print(f"Expected error: {e}")

        print("\nTest completed successfully!")

    except Exception as e:
        print(f"\nTest failed: {e}")
        raise
    finally:
        print("\nCleaning up...")
        try:
            if 'orders_db' in locals():
                orders_db.engine.dispose()
            if 'inventory_db' in locals():
                inventory_db.engine.dispose()
            if orders_container:
                orders_container.stop()
            if inventory_container:
                inventory_container.stop()
            print("Cleanup completed.")
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    run_distributed_test()
