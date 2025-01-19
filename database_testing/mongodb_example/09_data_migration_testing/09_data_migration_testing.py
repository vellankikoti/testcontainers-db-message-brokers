"""
09_data_migration_testing.py - Data Migration Testing with MongoDB

This example demonstrates testing data migration scenarios using MongoDB and Testcontainers.
"""

import pytest
from pymongo import MongoClient
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_source_data(source_db):
    """Set up sample data in source database."""
    # Old schema: Combined name field
    source_data = [
        {
            "customer_id": "C001",
            "name": "John Doe",
            "email": "john@example.com",
            "created_date": datetime(2024, 1, 1)
        },
        {
            "customer_id": "C002",
            "name": "Jane Smith",
            "email": "jane@example.com",
            "created_date": datetime(2024, 1, 2)
        }
    ]
    source_db.customers.insert_many(source_data)
    logger.info("Source data inserted")

def migrate_data(source_db, target_db):
    """Migrate data from source to target with schema transformation."""
    for customer in source_db.customers.find():
        # Check if the name field is None
        if customer["name"] is None:
            logger.warning(f"Skipping customer with ID {customer['customer_id']} due to None name.")
            continue  # Skip this record

        # Split name into first_name and last_name
        name_parts = customer["name"].split()
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        # New schema
        new_customer = {
            "customer_id": customer["customer_id"],
            "first_name": first_name,
            "last_name": last_name,
            "email": customer["email"],
            "created_date": customer["created_date"],
            "migration_date": datetime.now()
        }

        # Check if the customer already exists in the target database
        if target_db.customers.find_one({"customer_id": new_customer["customer_id"]}):
            logger.warning(f"Customer with ID {new_customer['customer_id']} already exists in target. Skipping.")
            continue  # Skip if already exists

        target_db.customers.insert_one(new_customer)
        logger.info(f"Migrated customer: {new_customer}")

    logger.info("Data migration completed")

def test_data_migration(source_client, target_client):
    """Test the data migration process."""
    source_db = source_client.migration_test
    target_db = target_client.migration_test

    # Clean up any existing data
    source_db.customers.delete_many({})
    target_db.customers.delete_many({})

    # Set up source data
    setup_source_data(source_db)

    # Perform migration
    migrate_data(source_db, target_db)

    # Verify migration results
    source_count = source_db.customers.count_documents({})
    target_count = target_db.customers.count_documents({})
    assert source_count == target_count, "Record count mismatch"

    # Verify data transformation
    target_customer = target_db.customers.find_one({"customer_id": "C001"})
    assert target_customer["first_name"] == "John"
    assert target_customer["last_name"] == "Doe"
    assert "migration_date" in target_customer

def test_incremental_migration(source_client, target_client):
    """Test incremental data migration."""
    source_db = source_client.migration_test
    target_db = target_client.migration_test

    # Clean up any existing data
    source_db.customers.delete_many({})
    target_db.customers.delete_many({})

    # Set up initial source data
    setup_source_data(source_db)

    # Add new record to source
    new_customer = {
        "customer_id": "C003",
        "name": "Alice Brown",
        "email": "alice@example.com",
        "created_date": datetime(2024, 1, 3)
    }
    source_db.customers.insert_one(new_customer)
    logger.info(f"Inserted new customer for incremental migration: {new_customer}")

    # Perform migration
    migrate_data(source_db, target_db)

    # Verify incremental migration
    assert target_db.customers.count_documents({}) == 3, f"Expected 3 customers, found {target_db.customers.count_documents({})}"
    migrated_customer = target_db.customers.find_one({"customer_id": "C003"})
    assert migrated_customer["first_name"] == "Alice"
    assert migrated_customer["last_name"] == "Brown"

def test_migration_rollback(source_client, target_client):
    """Test migration rollback capability."""
    source_db = source_client.migration_test
    target_db = target_client.migration_test

    # Clean up any existing data
    source_db.customers.delete_many({})
    target_db.customers.delete_many({})

    # Set up initial source data
    setup_source_data(source_db)

    # Save current state
    original_count = target_db.customers.count_documents({})

    try:
        # Simulate failed migration
        new_customer = {
            "customer_id": "C004",
            "name": None,  # This will cause an error
            "email": "invalid@example.com",
            "created_date": datetime(2024, 1, 4)
        }
        source_db.customers.insert_one(new_customer)

        # This should fail
        migrate_data(source_db, target_db)
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        # Verify no partial migration occurred
        current_count = target_db.customers.count_documents({})
        assert current_count == original_count, "Rollback failed"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
