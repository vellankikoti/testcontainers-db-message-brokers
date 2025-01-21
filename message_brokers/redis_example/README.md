# **Redis with Testcontainers**

## **Overview**
This repository contains a collection of examples demonstrating how to use Testcontainers for testing various scenarios with Redis. Each example is accompanied by a detailed README file to help you understand the concepts and implementation.

---

## **Table of Contents**
1. [Getting Started](#getting-started)
2. [Examples](#examples)
    - [01. Basic Pub/Sub](#01-basic-pub-sub)
    - [02. Message Persistence](#02-message-persistence)
    - [03. Message Acknowledgements](#03-message-acknowledgements)
    - [04. Performance Testing](#04-performance-testing)
    - [05. Resilience Testing](#05-resilience-testing)
    - [06. Simulating Failures](#06-simulating-failures)
    - [07. Custom Docker Image](#07-custom-docker-image)
    - [08. Expiry and TTL](#08-expiry-and-ttl)
    - [09. Data Migration Testing](#09-data-migration-testing)
    - [10. Multiple Containers](#10-multiple-containers)
    - [11. Simulating Network Interruptions](#11-simulating-network-interruptions)
    - [12. Distributed Transactions](#12-distributed-transactions)
    - [13. Testing with Mock Services](#13-testing-with-mock-services)
    - [14. Security Testing](#14-security-testing)
3. [How to Run the Examples](#how-to-run-the-examples)
4. [Troubleshooting](#troubleshooting)
5. [Conftest.py](#conftestpy)

---

## **Getting Started**
### **Prerequisites**
- Python 3.10 or later
- Docker installed and running on your system
- Required Python packages:
  ```bash
  pip install testcontainers redis pytest
  ```

---

## **Examples**

### 01. Basic Pub/Sub
**Description**: Demonstrates a basic Redis publish-subscribe messaging pattern using Testcontainers.  
**File**: `01_basic_pubsub.py`  
**README**: [README.md](01_basic_pubsub/README.md)

### 02. Message Persistence
**Description**: Ensures that Redis persists messages even if the server restarts.  
**File**: `02_message_persistence.py`  
**README**: [README.md](02_message_persistence/README.md)

### 03. Message Acknowledgements
**Description**: Validates Redis Streams message acknowledgement and delivery guarantees.  
**File**: `03_message_acknowledgements.py`  
**README**: [README.md](03_message_acknowledgements/README.md)

### 04. Performance Testing
**Description**: Measures Redis’ throughput and latency under high-load conditions.  
**File**: `04_performance_testing.py`  
**README**: [README.md](04_performance_testing/README.md)

### 05. Resilience Testing
**Description**: Tests how Redis handles failures and recovers from crashes.  
**File**: `05_resilience_testing.py`  
**README**: [README.md](05_resilience_testing/README.md)

### 06. Simulating Failures
**Description**: Simulates Redis server failures and recovery scenarios.  
**File**: `06_simulating_failures.py`  
**README**: [README.md](06_simulating_failures/README.md)

### 07. Custom Docker Image
**Description**: Creates and tests a custom Redis Docker image with specific configurations.  
**File**: `07_custom_docker_image.py`  
**Dockerfile**: `Dockerfile`  
**README**: [README.md](07_custom_docker_image/README.md)

### 08. Expiry and TTL
**Description**: Tests Redis key expiration, TTL settings, and eviction policies.  
**File**: `08_expiry_ttl.py`  
**README**: [README.md](08_expiry_ttl/README.md)

### 09. Data Migration Testing
**Description**: Uses Redis for migrating and syncing data between different systems.  
**File**: `09_data_migration_testing.py`  
**README**: [README.md](09_data_migration_testing/README.md)

### 10. Multiple Containers
**Description**: Simulates and tests Redis in a multi-container setup with other services.  
**File**: `10_multiple_containers.py`  
**README**: [README.md](10_multiple_containers/README.md)

### 11. Simulating Network Interruptions
**Description**: Tests Redis’ ability to recover from network disruptions.  
**File**: `11_simulating_network_interruptions.py`  
**README**: [README.md](11_simulating_network_interruptions/README.md)

### 12. Distributed Transactions
**Description**: Implements distributed transactions across multiple Redis instances.  
**File**: `12_distributed_transactions.py`  
**README**: [README.md](12_distributed_transactions/README.md)

### 13. Testing with Mock Services
**Description**: Mocks external services that interact with Redis for better test control.  
**File**: `13_testing_with_mock_services.py`  
**README**: [README.md](13_testing_with_mock_services/README.md)

### 14. Security Testing
**Description**: Tests Redis’ authentication, authorization, and encryption mechanisms.  
**File**: `14_security_testing.py`  
**README**: [README.md](14_security_testing/README.md)

---

## **How to Run the Examples**

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
   python <example-file>.py
   ```

4. View the README file for detailed information about each example.

---

## **Troubleshooting**

### Common Issues
1. **Docker Not Running**: Ensure Docker is installed and running on your system.
2. **ModuleNotFoundError**: Install the required Python packages using:
   ```bash
   pip install testcontainers redis pytest
   ```
3. **Redis Container Not Starting**: Ensure sufficient system resources (memory, CPU) are available for Docker to start Redis.

For more troubleshooting tips, refer to the troubleshooting guide.

---

## **Conftest.py**
The `conftest.py` file is used to define fixtures that can be shared across multiple test files. It typically contains setup code for Testcontainers, allowing you to initialize and manage Redis container instances for testing purposes.

---

## **Contributing**
Feel free to contribute by adding new examples, improving existing ones, or reporting issues.

---

## 🚀 Happy Testing with Redis and Testcontainers! 🎉

