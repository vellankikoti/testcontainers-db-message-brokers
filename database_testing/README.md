# **Database Testing with Testcontainers 🏨**

Welcome to the **Database Testing** section! This guide provides a **comprehensive overview** of how to use **Testcontainers** with **three popular databases**: **MySQL, PostgreSQL, and MongoDB**. Each database is explored through **practical examples** that demonstrate various **real-world testing scenarios**.

---

## **Table of Contents**

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Databases](#databases)
  - [MySQL](#mysql)
  - [PostgreSQL](#postgresql)
  - [MongoDB](#mongodb)
- [Examples](#examples)
  - [01. Basic CRUD Operations](#01-basic-crud-operations)
  - [02. Schema Validation](#02-schema-validation)
  - [03. Data Integrity Testing](#03-data-integrity-testing)
  - [04. Performance Testing](#04-performance-testing)
  - [05. Field Constraints & Index Testing](#05-field-constraints--index-testing)
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

---

## **Overview**

This repository contains a **collection of examples** demonstrating how to use **Testcontainers** with **MySQL, PostgreSQL, and MongoDB** for **real-world database testing** in Python. Each example is designed to help you:
- **Understand database concepts**
- **Implement robust database tests**
- **Run containerized database tests efficiently**

Each section **follows a structured approach**, starting from **basic CRUD operations** to **advanced resilience, indexing, and transaction management**.

---

## **Getting Started**

### **Prerequisites**

- **Python 3.10** or later
- **Docker installed and running** on your system
- Required Python packages for each database:
  ```bash
  pip install pytest mysql-connector-python psycopg2-binary pymongo testcontainers
  ```

---

## **Databases**

### **MySQL**
MySQL is a widely used **relational database management system**. In this section, you will find examples that demonstrate how to **test various operations** using **Testcontainers with MySQL**.

### **PostgreSQL**
PostgreSQL is an **advanced, open-source relational database**. This section provides examples that showcase the capabilities of **PostgreSQL in a testing environment** using **Testcontainers**.

### **MongoDB**
MongoDB is a **NoSQL database** that uses a **document-oriented data model**. This section contains examples illustrating how to work with **MongoDB using Testcontainers** for testing purposes.

---

## **Examples**

### **01. Basic CRUD Operations**
- **Description**: Demonstrates **Create, Read, Update, and Delete (CRUD)** operations using **Testcontainers**.
- **Files**:
  - MySQL: `mysql_example/01_basic_crud_operations.py`
  - PostgreSQL: `postgresql_example/01_basic_crud_operations.py`
  - MongoDB: `mongodb_example/01_basic_crud_operations.py`

### **02. Schema Validation**
- **Description**: Ensures the database schema **adheres to constraints** such as **primary keys, foreign keys, and unique constraints**.
- **Files**:
  - MySQL: `mysql_example/02_schema_validation.py`
  - PostgreSQL: `postgresql_example/02_schema_validation.py`
  - MongoDB: `mongodb_example/02_schema_validation.py`

### **03. Data Integrity Testing** (Updated ✅)
- **Description**: Ensures the database maintains **data consistency** and enforces **constraints**.
  - **MySQL**: Tests unique constraints and referential integrity.
  - **PostgreSQL**: Tests **unique constraints, transaction atomicity, and foreign key constraints**.
  - **MongoDB**: Ensures **schema validation, unique constraints, and atomic transactions**.
- **Files**:
  - MySQL: `mysql_example/03_data_integrity_testing.py`
  - PostgreSQL: `postgresql_example/03_data_integrity_testing.py`
  - MongoDB: `mongodb_example/03_data_integrity_testing.py`

### **04. Performance Testing**
- **Description**: Simulates **high-load scenarios** to measure database performance and identify bottlenecks.
- **Files**:
  - MySQL: `mysql_example/04_performance_testing.py`
  - PostgreSQL: `postgresql_example/04_performance_testing.py`
  - MongoDB: `mongodb_example/04_performance_testing.py`

### **05. Field Constraints & Index Testing** (Updated ✅)
- **Description**: Ensures that the database enforces **correct data constraints** and **optimizes queries with indexes**.
  - **MySQL**: Tests **NOT NULL constraints, CHECK constraints, and indexing**.
  - **PostgreSQL**: Ensures **constraints and indexed query performance**.
  - **MongoDB**: Tests **unique indexes, field constraints, and query performance**.
- **Files**:
  - MySQL: `mysql_example/05_field_constraints_and_indexes.py`
  - PostgreSQL: `postgresql_example/05_field_constraints_and_indexes.py`
  - MongoDB: `mongodb_example/05_field_constraints_and_indexes.py`

---

## **How to Run the Examples**

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Or:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run an example**:
   ```bash
   python3 -m pytest <example-file>.py -v -s
   ```

4. **Check the `README.md` file inside each example folder** for further details.

---

## **Troubleshooting**

### **Common Issues and Fixes**

- **Docker Not Running**  
  ```bash
  docker ps
  ```

- **Port Conflicts**  
  ```bash
  docker ps | grep 5432  # PostgreSQL
  docker ps | grep 3306  # MySQL
  docker ps | grep 27017 # MongoDB
  ```

- **Missing Dependencies**  
  ```bash
  pip install -r requirements.txt
  ```

---

## **Contributing**

- Feel free to **add new examples, improve existing ones, or report issues**.
- Contributions are welcome in **writing documentation, adding test cases, or optimizing performance tests**.

---

## **🚀 Happy Testing!**

---
