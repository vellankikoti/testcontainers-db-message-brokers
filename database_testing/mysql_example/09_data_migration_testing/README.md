# Example 9: Data Migration Testing

This example demonstrates how to test database schema migrations using Python, pytest, and Testcontainers. It ensures that data integrity is maintained during migrations and validates rollback functionality in case of migration failures.

## Features

- **Schema Migration Testing**: Test schema changes such as adding columns, creating tables, and modifying existing structures.
- **Data Consistency Validation**: Ensure that data remains consistent and intact after migration.
- **Rollback Testing**: Verify that the database schema can be rolled back to its original state in case of migration failure.
- **Automated Testing**: Use pytest and Testcontainers to automate the migration testing process in an isolated environment.

## Prerequisites

- **Docker**: Ensure Docker is installed and running.
- **Python 3.7+**: Required for running the tests.
- **pip**: Python package manager for installing dependencies.

## Installation

1. Clone the repository or navigate to the `09_data_migration_testing` directory.
2. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    or
   ```bash
    pip3 install -r requirements.txt
    ```
## Directory Structure

```
09_data_migration_testing/
├── 09_data_migration_testing.py   # Main test file
├── conftest.py                    # Pytest configuration
├── requirements.txt               # Dependencies
└── README.md                      # Documentation
```

## Running the Tests

1. Run the tests using:
    ```bash
    python 09_data_migration_testing.py -v -s
    ```
    or
    ```bash
    python3 09_data_migration_testing.py -v -s
    ```

    - `-v`: Enables verbose output.
    - `-s`: Displays print statements in the console.

## Test Scenarios

1. **Schema Migration**  
   Adds a new column (`phone`) to the `users` table.  
   Creates a new table (`orders`) with a foreign key reference to the `users` table.

2. **Validation**  
   Ensures the new column and table exist after the migration.  
   Validates the integrity of the migrated schema.

3. **Rollback**  
   Drops the new table (`orders`) and removes the new column (`phone`) from the `users` table.  
   Validates that the schema is restored to its original state.

## Expected Output

If the tests run successfully, you should see output similar to this:

![image](https://github.com/user-attachments/assets/93ec2342-be5a-4b99-9b55-e38fec27a037)


## Key Takeaways

- **Data Migration Testing**: Ensures that schema changes are applied correctly and data integrity is maintained.
- **Rollback Functionality**: Critical for handling migration failures and restoring the database to a consistent state.
- **Testcontainers**: Provides an isolated and reproducible environment for testing database migrations.
