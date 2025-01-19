# Example 9: Data Migration Testing (MongoDB)

This example demonstrates how to use Testcontainers to test data migration scenarios in MongoDB. It covers:

- Migrating data between collections.
- Validating data integrity after migration.
- Testing schema changes during migration.
- Handling migration errors.

---

## Overview

The test simulates a data migration scenario for a MongoDB-based hotel management system. It performs the following operations:

- **Data Migration**: Move data from one collection to another.
- **Schema Changes**: Modify the structure of documents during migration.
- **Data Validation**: Ensure data integrity after migration.
- **Error Handling**: Test the system's ability to handle migration errors.

---

## Features

### Data Migration

- Move data between collections.
- Transform data during migration.
- Test migration scripts.

### Schema Changes

- Add or remove fields.
- Modify field types.
- Validate schema changes.

### Data Validation

- Verify data integrity after migration.
- Check for missing or corrupted data.
- Test data consistency.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers pymongo
```

or

```bash
pip3 install pytest testcontainers pymongo
```

### 2. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 09_data_migration_testing.py -v -s
```

or

```bash
python3 -m pytest 09_data_migration_testing.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/ff36842d-114a-422f-ba9e-3141661a2365)


---

## Code Walkthrough

### 1. Data Migration

Migrate data from `old_guests` to `new_guests`:

```python
old_guests = db.get_collection("old_guests")
new_guests = db.get_collection("new_guests")

for guest in old_guests.find():
    transformed_guest = {
        "full_name": f"{guest['first_name']} {guest['last_name']}",
        "email": guest["email"],
        "phone": guest["phone"],
        "status": "migrated"
    }
    new_guests.insert_one(transformed_guest)
```

- Moves data from one collection to another.
- Transforms data during migration.

---

### 2. Schema Changes

Add a new field `status` to all documents:

```python
new_guests.update_many({}, {"$set": {"status": "active"}})
```

- Adds or modifies fields in documents.
- Tests schema changes during migration.

---

### 3. Data Validation

Validate data integrity after migration:

```python
assert new_guests.count_documents({}) == old_guests.count_documents({})
```

- Verifies that all data was migrated successfully.
- Ensures no data was lost or corrupted.

---

## Key Takeaways

### MongoDB Benefits

- Flexible schema for data migration.
- Powerful update and transformation capabilities.
- Efficient handling of large datasets.

### Testing Practices

- Validate data integrity.
- Test schema changes.
- Handle migration errors.
- Ensure proper cleanup.

### Data Migration Testing

- Test migration scripts.
- Validate schema transformations.
- Ensure data consistency.
- Handle edge cases.

---

## Common Issues and Solutions

### 1. Data Loss

- Validate data counts before and after migration.
- Handle missing fields during transformation.
- Test for corrupted data.

### 2. Schema Changes

- Test schema transformations.
- Validate new field values.
- Handle type mismatches.

### 3. Migration Errors

- Log errors during migration.
- Implement retry mechanisms.
- Test for partial migrations.

---

## Future Enhancements

### Planned Features

- Automated migration scripts.
- Real-time migration monitoring.
- Rollback mechanisms for failed migrations.
- Integration with schema validation tools.

### Testing Improvements

- Larger datasets.
- Complex schema transformations.
- Multi-collection migrations.
- Performance testing during migration.

---
