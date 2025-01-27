# **PostgreSQL with Testcontainers**

This repository contains a comprehensive series of examples demonstrating how to use **Testcontainers with PostgreSQL** to test database operations effectively. Each example is self-contained and illustrates a unique testing scenario.

---

## **Table of Contents**

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Examples](#examples)
    - [01. Basic CRUD Operations](#01-basic-crud-operations)
    - [02. Indexing and Performance](#02-indexing-and-performance)
    - [03. Data Integrity Testing](#03-data-integrity-testing)
    - [04. Aggregation Queries](#04-aggregation-queries)
    - [05. Field Constraints & Index Testing](#05-field-constraints--index-testing)
    - [06. Simulating Failures](#06-simulating-failures)
    - [07. Custom Docker Image](#07-custom-docker-image)
    - [08. Performance Testing](#08-performance-testing)
    - [09. Data Migration Testing](#09-data-migration-testing)
    - [10. Testing with Multiple Containers](#10-testing-with-multiple-containers)
    - [11. Simulating Network Interruptions](#11-simulating-network-interruptions)
    - [12. Distributed Transactions](#12-distributed-transactions)
    - [13. Testing with Mock Services](#13-testing-with-mock-services)
    - [14. Security Testing](#14-security-testing)
4. [How to Run Examples](#how-to-run-examples)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)
7. [Next Steps](#next-steps)
8. [Need Help?](#need-help)

---

## **Overview**

This guide provides **step-by-step instructions** for using **Testcontainers with PostgreSQL** to test various scenarios, from **basic CRUD operations** to **advanced use cases** like **distributed transactions and security testing**.

---

## **Prerequisites**

Before starting, ensure you have the following:

- **Python 3.10** or later
- **Docker** installed and running
- Required Python packages:
  ```bash
  pip install pytest testcontainers psycopg2-binary sqlalchemy redis requests
  ```

---

## **Examples**

### **01. Basic CRUD Operations**
**File**: `postgresql_example/01_basic_crud_operations.py`  
**Description**: Implements basic **Create, Read, Update, and Delete (CRUD) operations** in PostgreSQL.  
**README**: [README.md](01_basic_crud_operations/README.md)

### **02. Indexing and Performance**
**File**: `postgresql_example/02_indexing_and_performance.py`  
**Description**: Demonstrates how to create and use **indexes** to optimize query performance.  
**README**: [README.md](02_indexing_and_performance/README.md)

### **03. Data Integrity Testing** (Updated ✅)
**File**: `postgresql_example/03_data_integrity_testing.py`  
**Description**: Ensures that PostgreSQL **enforces data integrity** by testing:  
- **Unique Constraints**: Prevents duplicate records.  
- **Transaction Atomicity**: Ensures all-or-nothing execution.  
- **Foreign Key Constraints**: Prevents orphaned records.  
**README**: [README.md](03_data_integrity_testing/README.md)

### **04. Aggregation Queries**
**File**: `postgresql_example/04_aggregation_queries.py`  
**Description**: Demonstrates the use of **aggregation functions** for data analysis.  
**README**: [README.md](04_aggregation_queries/README.md)

### **05. Field Constraints & Index Testing** (Updated ✅)
**File**: `postgresql_example/05_field_constraints_and_indexes.py`  
**Description**: Tests **PostgreSQL constraints and indexing**:
- **NOT NULL Constraints**: Ensures required fields cannot be `NULL`.
- **CHECK Constraints**: Prevents invalid values (e.g., negative ages).
- **Indexes**: Ensures indexed queries execute efficiently.
**README**: [README.md](05_field_constraints_and_indexes/README.md)

### **06. Simulating Failures**
**File**: `postgresql_example/06_simulating_failures.py`  
**Description**: Tests database **resilience** by simulating **container restarts**.  
**README**: [README.md](06_simulating_failures/README.md)

### **07. Custom Docker Image**
**File**: `postgresql_example/07_custom_docker_image.py`  
**Description**: Uses a **custom Docker image** for PostgreSQL testing.  
**README**: [README.md](07_custom_docker_image/README.md)

### **08. Performance Testing**
**File**: `postgresql_example/08_performance_testing.py`  
**Description**: Measures performance under **high-load scenarios**.  
**README**: [README.md](08_performance_testing/README.md)

### **09. Data Migration Testing**
**File**: `postgresql_example/09_data_migration_testing.py`  
**Description**: Validates **schema and data migrations**.  
**README**: [README.md](09_data_migration_testing/README.md)

### **10. Testing with Multiple Containers**
**File**: `postgresql_example/10_multiple_containers.py`  
**Description**: Verifies **interactions between PostgreSQL and other services**.  
**README**: [README.md](10_multiple_containers/README.md)

### **11. Simulating Network Interruptions**
**File**: `postgresql_example/11_simulating_network_interruptions.py`  
**Description**: Tests resilience during **network disruptions**.  
**README**: [README.md](11_simulating_network_interruptions/README.md)

### **12. Distributed Transactions**
**File**: `postgresql_example/12_distributed_transactions.py`  
**Description**: Ensures **atomicity across multiple services**.  
**README**: [README.md](12_distributed_transactions/README.md)

### **13. Testing with Mock Services**
**File**: `postgresql_example/13_testing_with_mock_services.py`  
**Description**: Simulates **external APIs for integration testing**.  
**README**: [README.md](13_testing_with_mock_services/README.md)

### **14. Security Testing**
**File**: `postgresql_example/14_security_testing.py`  
**Description**: Tests for **SQL injection and security vulnerabilities**.  
**README**: [README.md](14_security_testing/README.md)

---

## **How to Run Examples**

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run an example:
   ```bash
   python -m pytest <example-file>.py -v
   ```

---

## **Troubleshooting**

### Common Issues and Fixes

- **Docker Not Running**
  ```bash
  docker ps
  ```

- **Port Conflicts**
  ```bash
  docker ps | grep 5432
  ```

- **Missing Dependencies**
  ```bash
  pip install -r requirements.txt
  ```

---

## **Best Practices**

- **Use Clean Test Environments**: Containers ensure each test runs in an isolated database.
- **Validate Constraints Early**: Enforce constraints (e.g., `NOT NULL`, `UNIQUE`, `FOREIGN KEY`) during schema design.
- **Use Indexing Wisely**: Index performance tests help optimize query speeds.

---

## **Need Help?**

For issues, check:
```bash
docker logs [container-id]
```

---

## **🚀 Happy Testing!**

---
