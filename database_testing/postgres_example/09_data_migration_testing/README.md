# Example 9: Data Migration Testing

## Overview
This example demonstrates how to test database migrations using Testcontainers and pytest.

## Features
- Verify schema changes after applying migrations.
- Ensure data consistency after migrations.
- Test new functionality introduced by migrations.

## Code Structure
- `09_data_migration_testing.py`: Main test file.
- `Dockerfile`: Custom Dockerfile for PostgreSQL.
- `init.sql`: SQL script to initialize the database with the initial schema.
- `migration.sql`: SQL script to apply the migration.
- `conftest.py`: Pytest configuration file for custom markers.

## How to Run
1. Build the Docker image:
```bash
docker build -t custom-postgres:1.0 .
```

2. Run the tests:
```bash
python -m pytest 09_data_migration_testing.py -v
```
or 
```bash
python3 -m pytest 09_data_migration_testing.py -v
```
## Expected Output
- Initial schema is verified.
- Migration is applied successfully.
- Data consistency is maintained.
- New functionality is tested successfully.

## Key Takeaways
- Database migrations should be tested to ensure schema changes are applied correctly.
- Testcontainers makes it easy to test migrations in isolated environments.

---

### **Steps to Run**

1. **Build the Docker Image**:
```bash
docker build -t custom-postgres:1.0 .
```

2. **Run the Tests**:
```bash
python -m pytest 09_data_migration_testing.py -v
```
or
```bash
python3 -m pytest 09_data_migration_testing.py -v
```

### Expected Output
If everything is set up correctly, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/3c817f24-4538-443f-a814-1443830d879b)


## For more detailed output use -s flag
```bash
python -m pytest 09_data_migration_testing.py -v -s
```
or
```bash
python3 -m pytest 09_data_migration_testing.py -v -s
```
### Expected Output
If everything is set up correctly, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/428f0fc4-c8ca-4749-8d12-e173662fabc1)
