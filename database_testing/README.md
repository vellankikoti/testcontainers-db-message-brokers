# Database Testing with Testcontainers 🏨

Welcome to the Database Testing section! This guide provides a comprehensive overview of how to use Testcontainers with three popular databases: MySQL, PostgreSQL, and MongoDB. Each database is explored through a series of practical examples that demonstrate various testing scenarios.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Databases](#databases)
  - [MySQL](#mysql)
  - [PostgreSQL](#postgresql)
  - [MongoDB](#mongodb)
- [Examples](#examples)
  - [01. Basic CRUD Operations](#01-basic-crud-operations)
  - [02. Schema Validation](#02-schema-validation)
  - [03. Transaction Management](#03-transaction-management)
  - [04. Performance Testing](#04-performance-testing)
  - [05. Resilience Testing](#05-resilience-testing)
  - [06. Simulating Failures](#06-simulating-failures)
  - [07. Custom Docker Image](#07-custom-docker-image)
  - [08. Performance Testing](#08-performance-testing)
  - [09. Data Migration Testing](#09-data-migration-testing)
  - [10. Multiple Containers](#10-multiple-containers)
  - [11. Simulating Network Interruptions](#11-simulating-network-interruptions)
  - [12. Distributed Transactions](#12-distributed-transactions)
  - [13. Testing with Mock Services](#13-testing-with-mock-services)
  - [14. Security Testing](#14-security-testing)
- [How to Run the Examples](#how-to-run-the-examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

This repository contains a collection of examples demonstrating how to use Testcontainers with MySQL, PostgreSQL, and MongoDB for testing various scenarios in Python. Each example is designed to help you understand the concepts and implementation of database testing in a containerized environment.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Docker installed and running on your system
- Required Python packages for each database:
  ```bash
  pip install pytest mysql-connector-python psycopg2-binary pymongo testcontainers
  ```

## Databases

### MySQL

MySQL is a widely used relational database management system. In this section, you will find examples that demonstrate how to perform various operations using Testcontainers with MySQL.

### PostgreSQL

PostgreSQL is an advanced, open-source relational database. This section provides examples that showcase the capabilities of PostgreSQL in a testing environment using Testcontainers.

### MongoDB

MongoDB is a NoSQL database that uses a document-oriented data model. Here, you will find examples that illustrate how to work with MongoDB using Testcontainers for testing purposes.

## Examples

### 01. Basic CRUD Operations
- **Description**: Demonstrates fundamental operations like Create, Read, Update, and Delete (CRUD) using the respective database and Testcontainers.
- **Files**:
  - MySQL: `mysql_example/01_basic_crud_operations.py`
  - PostgreSQL: `postgresql_example/01_basic_crud_operations.py`
  - MongoDB: `mongodb_example/01_basic_crud_operations.py`

### 02. Schema Validation
- **Description**: Validates database schema, ensuring it matches expected structures and adheres to constraints such as primary keys, foreign keys, and unique constraints.
- **Files**:
  - MySQL: `mysql_example/02_schema_validation.py`
  - PostgreSQL: `postgresql_example/02_schema_validation.py`
  - MongoDB: `mongodb_example/02_schema_validation.py`

### 03. Transaction Management
- **Description**: Tests the atomicity of database transactions, verifying that operations either fully succeed or fully fail, including rollback and commit behavior.
- **Files**:
  - MySQL: `mysql_example/03_transaction_management.py`
  - PostgreSQL: `postgresql_example/03_transaction_management.py`
  - MongoDB: `mongodb_example/03_transaction_management.py`

### 04. Performance Testing
- **Description**: Simulates high-load scenarios to measure database performance and identify bottlenecks.
- **Files**:
  - MySQL: `mysql_example/04_performance_testing.py`
  - PostgreSQL: `postgresql_example/04_performance_testing.py`
  - MongoDB: `mongodb_example/04_performance_testing.py`

### 05. Resilience Testing
- **Description**: Simulates database failures, such as container restarts or network interruptions, to ensure applications can recover and reconnect seamlessly.
- **Files**:
  - MySQL: `mysql_example/05_resilience_testing.py`
  - PostgreSQL: `postgresql_example/05_resilience_testing.py`
  - MongoDB: `mongodb_example/05_resilience_testing.py`

### 06. Simulating Failures
- **Description**: Simulates database connection failures and resilience testing.
- **Files**:
  - MySQL: `mysql_example/06_simulating_failures.py`
  - PostgreSQL: `postgresql_example/06_simulating_failures.py`
  - MongoDB: `mongodb_example/06_simulating_failures.py`

### 07. Custom Docker Image
- **Description**: Builds and uses a custom Docker image with preloaded data.
- **Files**:
  - MySQL: `mysql_example/07_custom_docker_image.py`
  - PostgreSQL: `postgresql_example/07_custom_docker_image.py`
  - MongoDB: `mongodb_example/07_custom_docker_image.py`

### 08. Performance Testing
- **Description**: Measures performance under high-load scenarios.
- **Files**:
  - MySQL: `mysql_example/08_performance_testing.py`
  - PostgreSQL: `postgresql_example/08_performance_testing.py`
  - MongoDB: `mongodb_example/08_performance_testing.py`

### 09. Data Migration Testing
- **Description**: Validates schema and data migrations.
- **Files**:
  - MySQL: `mysql_example/09_data_migration_testing.py`
  - PostgreSQL: `postgresql_example/09_data_migration_testing.py`
  - MongoDB: `mongodb_example/09_data_migration_testing.py`

### 10. Multiple Containers
- **Description**: Verifies interactions between the database and another container (e.g., Redis).
- **Files**:
  - MySQL: `mysql_example/10_multiple_containers.py`
  - PostgreSQL: `postgresql_example/10_multiple_containers.py`
  - MongoDB: `mongodb_example/10_multiple_containers.py`

### 11. Simulating Network Interruptions
- **Description**: Tests resilience during network disruptions.
- **Files**:
  - MySQL: `mysql_example/11_simulating_network_interruptions.py`
  - PostgreSQL: `postgresql_example/11_simulating_network_interruptions.py`
  - MongoDB: `mongodb_example/11_simulating_network_interruptions.py`

### 12. Distributed Transactions
- **Description**: Ensures atomicity across services in a distributed system.
- **Files**:
  - MySQL: `mysql_example/12_distributed_transactions.py`
  - PostgreSQL: `postgresql_example/12_distributed_transactions.py`
  - MongoDB: `mongodb_example/12_distributed_transactions.py`

### 13. Testing with Mock Services
- **Description**: Simulates a mocked payment service for integration tests.
- **Files**:
  - MySQL: `mysql_example/13_testing_with_mock_services.py`
  - PostgreSQL: `postgresql_example/13_testing_with_mock_services.py`
  - MongoDB: `mongodb_example/13_testing_with_mock_services.py`

### 14. Security Testing
- **Description**: Validates database security configurations.
- **Files**:
  - MySQL: `mysql_example/14_security_testing.py`
  - PostgreSQL: `postgresql_example/14_security_testing.py`
  - MongoDB: `mongodb_example/14_security_testing.py`

## How to Run the Examples

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run an example:**
   ```bash
   python <example-file>.py
   ```
   Or:
   ```bash
   python3 <example-file>.py
   ```

4. **View the README file for detailed information about each example.**

## Troubleshooting

### Common Issues

- **Docker Not Running**: Ensure Docker is installed and running on your system.
- **ModuleNotFoundError**: Install the required Python packages using:
  ```bash
  pip install pytest mysql-connector-python psycopg2-binary pymongo testcontainers
  ```
- **Insufficient Resources**: Allocate more CPU and memory to Docker if containers fail to start.

## Contributing

Feel free to contribute by adding new examples, improving existing ones, or reporting issues.

Happy Testing! 🏨✨

