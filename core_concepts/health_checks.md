# **Health Checks in Testcontainers**

## **Overview**
Health checks are used to determine whether a containerized service is ready to accept requests or perform its intended function. Testcontainers provides mechanisms to ensure that containers are healthy before running tests.

---

## **Why Health Checks Are Important**
1. **Ensure Readiness**: Verify that the containerized service is fully initialized and ready to handle requests.
2. **Avoid Failures**: Prevent tests from running against an unready or unhealthy container.
3. **Improve Reliability**: Ensure consistent test results by waiting for the container to be healthy.

---

## **How to Use Health Checks**

### **Step 1: Using Built-in Health Checks**
Some Docker images, like PostgreSQL, come with built-in health checks. Testcontainers automatically waits for these health checks to pass before proceeding.

#### **Example Code**
```python
# builtin_health_check.py
from testcontainers.postgres import PostgresContainer
import time

def test_builtin_health_check():
    print("\n=== PostgreSQL Built-in Health Check Test ===")

    try:
        print("Starting PostgreSQL container with built-in health check...")
        # PostgreSQL image has built-in health checks
        postgres = PostgresContainer(
            "postgres:15.3",
            username="testuser",
            password="testpass",
            dbname="testdb"
        )

        # Start container - this will wait for built-in health check
        postgres.start()

        # Get container details
        container_id = postgres.get_wrapped_container().id
        port = postgres.get_exposed_port(5432)

        print(f"\nContainer started successfully!")
        print(f"Container ID: {container_id}")
        print(f"Mapped Port: {port}")

        # Keep container running briefly
        print("\nContainer will stay running for 30 seconds...")
        time.sleep(30)

        # Clean up
        postgres.stop()
        print("\nContainer stopped and removed.")

    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    test_builtin_health_check()
```
#### **Example output**
![image](https://github.com/user-attachments/assets/52131174-63b1-45e1-98eb-cc1b85ce332f)


#### **Explanation**
- The PostgreSQL image includes a built-in health check that verifies:
    - The database process is running.
    - Port 5432 is accepting connections.
    - Basic SQL queries can be executed.
- Testcontainers automatically waits for this health check to pass before proceeding.
---

### **Step 2: Adding Custom Health Checks**
If the built-in health checks are not sufficient, you can define your own custom health checks to verify specific functionality or application requirements.

#### **Example Code**
```python
# custom_health_check.py
from testcontainers.postgres import PostgresContainer
import psycopg2
import time

def test_custom_health_check():
    print("\n=== PostgreSQL Custom Health Check Test ===")

    try:
        # Start PostgreSQL container
        with PostgresContainer(
            "postgres:15.3",
            username="testuser",
            password="testpass",
            dbname="testdb"
        ) as postgres:
            # Get container details
            container_id = postgres.get_wrapped_container().id
            port = postgres.get_exposed_port(5432)

            print("\nContainer Details:")
            print(f"Container ID: {container_id}")
            print(f"Port: {port}")

            # Custom health check implementation
            max_retries = 5
            retry_delay = 2

            for attempt in range(max_retries):
                try:
                    print(f"\nHealth check attempt {attempt + 1}/{max_retries}")

                    # Try to connect and run test query
                    conn = psycopg2.connect(
                        dbname="testdb",
                        user="testuser",
                        password="testpass",
                        host="localhost",
                        port=port
                    )

                    cursor = conn.cursor()

                    # Test basic connectivity
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()[0]
                    print("✓ Basic connectivity test passed")

                    cursor.close()
                    conn.close()

                    print("\nAll health checks passed!")
                    print(f"PostgreSQL Version: {version}")
                    break

                except Exception as e:
                    print(f"Health check failed: {str(e)}")
                    if attempt < max_retries - 1:
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        raise Exception("Max retries reached, health check failed")

            # Keep container running for testing
            print("\nContainer will stay running for 30 seconds...")
            time.sleep(30)

    except Exception as e:
        print(f"\nError: {str(e)}")

    print("\nContainer stopped and removed.")

if __name__ == "__main__":
    test_custom_health_check()

```

#### **Example output**
![image](https://github.com/user-attachments/assets/329d36a8-a42f-4e33-9ff3-ed54721f307f)


#### **Explanation**
- This example implements a custom health check that:
    - Tests basic connectivity to the database.
    - Verifies that the database is ready to accept queries.
- Includes a retry mechanism to handle delays in container initialization.

---
### **Step 3: Comprehensive Health Checks**
Comprehensive health checks go beyond basic connectivity and built-in health checks by verifying additional functionality, such as table creation, data insertion, and query execution. These checks ensure that the database is fully operational and ready for application-specific use cases.

#### **Example Code**
```python
# comprehensive_health_check.py
from testcontainers.postgres import PostgresContainer
import psycopg2
import time

def test_comprehensive_health_check():
    print("\n=== PostgreSQL Comprehensive Health Check Test ===")

    try:
        # Start PostgreSQL container
        with PostgresContainer(
            "postgres:15.3",
            username="testuser",
            password="testpass",
            dbname="testdb"
        ) as postgres:
            # Get container details
            container_id = postgres.get_wrapped_container().id
            port = postgres.get_exposed_port(5432)

            print("\nContainer Details:")
            print(f"Container ID: {container_id}")
            print(f"Port: {port}")

            # Comprehensive health check implementation
            max_retries = 5
            retry_delay = 2

            for attempt in range(max_retries):
                try:
                    print(f"\nHealth check attempt {attempt + 1}/{max_retries}")

                    # Try to connect and run test queries
                    conn = psycopg2.connect(
                        dbname="testdb",
                        user="testuser",
                        password="testpass",
                        host="localhost",
                        port=port
                    )

                    cursor = conn.cursor()

                    # Test basic connectivity
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()[0]
                    print("✓ Basic connectivity test passed")

                    # Test table creation
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS health_check (
                            id SERIAL PRIMARY KEY,
                            status TEXT
                        );
                    """)
                    print("✓ Table creation test passed")

                    # Test data insertion
                    cursor.execute("""
                        INSERT INTO health_check (status) 
                        VALUES ('healthy');
                    """)
                    print("✓ Data insertion test passed")

                    # Test data retrieval
                    cursor.execute("SELECT * FROM health_check;")
                    rows = cursor.fetchall()
                    assert len(rows) > 0, "No data found in health_check table"
                    print("✓ Data retrieval test passed")

                    cursor.close()
                    conn.close()

                    print("\nAll comprehensive health checks passed!")
                    print(f"PostgreSQL Version: {version}")
                    break

                except Exception as e:
                    print(f"Health check failed: {str(e)}")
                    if attempt < max_retries - 1:
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        raise Exception("Max retries reached, health check failed")

            # Keep container running for testing
            print("\nContainer will stay running for 5 minutes...")
            print("Connection Details:")
            print(f"Host: localhost")
            print(f"Port: {port}")
            print(f"Database: testdb")
            print(f"Username: testuser")
            print(f"Password: testpass")

            try:
                for i in range(300, 0, -1):
                    print(f"\rTime remaining: {i} seconds...", end="", flush=True)
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\nStopping container early...")

    except Exception as e:
        print(f"\nError: {str(e)}")

    print("\nContainer stopped and removed.")

if __name__ == "__main__":
    test_comprehensive_health_check()
```
#### **Example output**
![image](https://github.com/user-attachments/assets/ed8c6547-a1dc-4f17-a3a9-2980fb614f7d)

---

#### **Explanation**
**1. Comprehensive Health Check:**

- This example goes beyond basic connectivity and built-in health checks by verifying:
    - **Basic Connectivity:** Ensures the database is running and accepting connections.
    - **Table Creation:** Verifies that the database can execute DDL (Data Definition Language) queries.
    - **Data Insertion:** Confirms that data can be inserted into the database.
    - **Data Retrieval:** Ensures that data can be queried and retrieved successfully.

**2. Retry Mechanism:** 
- The script includes a retry mechanism with configurable attempts (**`max_retries`**) and delay (**`retry_delay`**) to handle delays in container initialization.
---

## **Common Issues with Health Checks**
1. **Timeouts**: If the health check takes too long, the container may be marked as unhealthy.
   - **Solution**: Increase the timeout or retries in the health check configuration.
2. **Incorrect Commands**: Ensure that the health check command is valid and works inside the container.
   - **Solution**: Test the command manually inside the container before adding it as a health check.

---

## **Key Takeaways**
- Health checks ensure that containers are ready before running tests.
- Testcontainers automatically waits for built-in health checks to pass.
- You can define custom health checks for containers that do not include them.
- Properly configured health checks improve test reliability and prevent failures.
