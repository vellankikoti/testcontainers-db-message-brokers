# 🧼 Clean Tests with Testcontainers

## 🎯 Overview
Ensuring clean and well-structured tests is crucial when working with Testcontainers. Clean tests help in maintaining readability, reducing flakiness, and improving reliability.

## ✅ Best Practices for Writing Clean Tests

### 1️⃣ **Ensure Tests Are Isolated**
- Each test should run independently without dependencies on previous tests.
- Use unique database names, queues, or topics when testing databases or message brokers.
- Avoid shared state between test cases.

### 2️⃣ **Use Meaningful Naming Conventions**
- Clearly indicate what the test does.
- Example:
  ```python
  def test_should_return_200_on_successful_login():
      pass
  ```

### 3️⃣ **Follow Arrange-Act-Assert (AAA) Pattern**
- **Arrange**: Set up the environment and inputs.
- **Act**: Execute the function or operation being tested.
- **Assert**: Verify expected outcomes.
- Example:
  ```python
  def test_should_return_correct_user_data():
      # Arrange
      container = PostgreSQLContainer("postgres:13")
      container.start()
      db = get_database_connection(container)
      
      # Act
      result = db.fetch_user_data(1)
      
      # Assert
      assert result["name"] == "John Doe"
  ```

### 4️⃣ **Use Fixtures to Manage Setup and Teardown**
- Fixtures ensure containers are properly created and cleaned up.
- Example using `pytest`:
  ```python
  import pytest
  from testcontainers.postgres import PostgresContainer
  
  @pytest.fixture(scope="function")
  def postgres_container():
      container = PostgresContainer("postgres:13")
      container.start()
      yield container
      container.stop()
  ```

### 5️⃣ **Avoid Hardcoded Values**
- Use environment variables or configuration files instead of hardcoded values.
- Example:
  ```python
  DATABASE_URL = os.getenv("DATABASE_URL", "postgres://user:password@localhost/db")
  ```

### 6️⃣ **Implement Proper Teardown Logic**
- Ensure that Testcontainers stop after test execution to prevent resource leaks.
- Example:
  ```python
  def test_cleanup_container():
      container = MySQLContainer("mysql:8.0")
      try:
          container.start()
          # Run tests here
      finally:
          container.stop()
  ```

## 🚀 Conclusion
By following these clean test practices, you can create **maintainable, reliable, and efficient** test cases using Testcontainers. Clean tests result in **faster debugging, fewer false positives, and improved developer experience**.

