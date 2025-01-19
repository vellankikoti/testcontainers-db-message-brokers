# **PostgreSQL with Testcontainers**

This repository contains a comprehensive series of examples demonstrating how to use Testcontainers with PostgreSQL to test database operations effectively. Each example is self-contained and illustrates a unique testing scenario.

---

## **Table of Contents**

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Examples](#examples)
    - [01. Basic Guest Registration](#01-basic-guest-registration)
    - [02. Room Management](#02-room-management)
    - [03. Reservation System](#03-reservation-system)
    - [04. Occupancy Reports](#04-occupancy-reports)
    - [05. Extended Stays](#05-extended-stays)
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
6. [Key Concepts Demonstrated](#key-concepts-demonstrated)
7. [Best Practices](#best-practices)
8. [Next Steps](#next-steps)
9. [Need Help?](#need-help)

---

## **Overview**

Welcome to the **"Happy Hotel"** database testing series! This guide provides step-by-step instructions for using Testcontainers with PostgreSQL to test various scenarios, from basic CRUD operations to advanced use cases like distributed transactions and security testing.

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

Here’s the full list of examples included in this series:

### 01. Basic Guest Registration
**File**: `postgresql_example/01_basic_guests.py`  
**Description**: Implements a basic guest registration system.    
**README**: [README.md](01_basic_guests/README.md)

### 02. Room Management
**File**: `postgresql_example/02_room_management.py`  
**Description**: Manages room inventory and pricing.    
**README**: [README.md](02_room_management/README.md)

### 03. Reservation System
**File**: `postgresql_example/03_reservations.py`  
**Description**: Handles bookings with multiple tables.    
**README**: [README.md](03_reservations/README.md)

### 04. Occupancy Reports
**File**: `postgresql_example/04_occupancy_report.py`  
**Description**: Generates reports on room occupancy.    
**README**: [README.md](04_occupancy_report/README.md)

### 05. Extended Stays
**File**: `postgresql_example/05_extended_stays.py`  
**Description**: Updates booking durations for extended stays.    
**README**: [README.md](05_extended_stays/README.md)

### 06. Simulating Failures
**File**: `postgresql_example/06_simulating_failures.py`  
**Description**: Tests resilience by simulating container restarts.    
**README**: [README.md](06_simulating_failures/README.md)

### 07. Custom Docker Image
**File**: `postgresql_example/07_custom_docker_image.py`  
**Description**: Utilizes a custom Docker image for testing.    
**README**: [README.md](07_custom_docker_image/README.md)

### 08. Performance Testing
**File**: `postgresql_example/08_performance_testing.py`  
**Description**: Simulates high traffic and measures performance.    
**README**: [README.md](08_performance_testing/README.md)

### 09. Data Migration Testing
**File**: `postgresql_example/09_data_migration_testing.py`  
**Description**: Validates schema and data migrations.    
**README**: [README.md](09_data_migration_testing/README.md)

### 10. Testing with Multiple Containers
**File**: `postgresql_example/10_multiple_containers.py`  
**Description**: Tests interactions between PostgreSQL and Redis.    
**README**: [README.md](10_multiple_containers/README.md)

### 11. Simulating Network Interruptions
**File**: `postgresql_example/11_simulating_network_interruptions.py`  
**Description**: Tests resilience during network disruptions.    
**README**: [README.md](11_simulating_network_interruptions/README.md)

### 12. Distributed Transactions
**File**: `postgresql_example/12_distributed_transactions.py`  
**Description**: Ensures atomicity across multiple services.    
**README**: [README.md](12_distributed_transactions/README.md)

### 13. Testing with Mock Services
**File**: `postgresql_example/13_testing_with_mock_services.py`  
**Description**: Simulates external APIs for integration testing.    
**README**: [README.md](13_testing_with_mock_services/README.md)

### 14. Security Testing
**File**: `postgresql_example/14_security_testing.py`  
**Description**: Tests for SQL injection and security vulnerabilities.    
**README**: [README.md](14_security_testing/README.md)

---

## **How to Run Examples**

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required dependencies:
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

1. **Docker Not Running**  
   Ensure Docker is installed and running:
   ```bash
   docker ps
   ```

2. **Port Conflicts**  
   Check if another PostgreSQL instance is running:
   ```bash
   docker ps | grep 5432
   ```

3. **Missing Dependencies**  
   Install missing Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Key Concepts Demonstrated**

- Container lifecycle management
- Database operations (CRUD)
- Transaction handling and error recovery
- Simulating real-world scenarios (e.g., failures, network issues)
- Mocking external services
- Security testing against common vulnerabilities

---

## **Best Practices**

- Self-contained tests for repeatability
- Clean test environment for every execution
- Comprehensive assertions and meaningful outputs
- Use of realistic scenarios for better coverage

---

## **Next Steps**

- Extend the examples with more advanced scenarios.
- Explore Testcontainers features like custom networks and configurations.
- Implement your own test cases for complex business logic.

---

## **Need Help?**

If you encounter issues, check:

- Docker logs for the container:
  ```bash
  docker logs [container-id]
  ```

- Dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

---

## Happy Testing! 🏨✨

--- 
