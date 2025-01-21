# **Kafka with Testcontainers**

## **Overview**
This repository contains a collection of examples demonstrating how to use Testcontainers for testing various Kafka-related scenarios in Python. Each example is accompanied by a detailed README file to help you understand the concepts and implementation.

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
    - [08. Schema Evolution](#08-schema-evolution)
    - [09. Data Migration Testing](#09-data-migration-testing)
    - [10. Multi-Broker Clusters](#10-multi-broker-clusters)
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
  pip install testcontainers kafka-python pytest
  ```

---

## **Examples**

### 01. Basic Pub/Sub
**Description**: Demonstrates a basic Kafka producer-consumer workflow using a publish-subscribe model.  
**File**: `01_basic_pubsub.py`  
**README**: [README.md](01_basic_pubsub/README.md)

### 02. Message Persistence
**Description**: Ensures that Kafka persists messages even if a consumer crashes.  
**File**: `02_message_persistence.py`  
**README**: [README.md](02_message_persistence/README.md)

### 03. Message Acknowledgements
**Description**: Validates Kafka’s at-least-once and exactly-once message delivery guarantees.  
**File**: `03_message_acknowledgements.py`  
**README**: [README.md](03_message_acknowledgements/README.md)

### 04. Performance Testing
**Description**: Measures Kafka’s throughput and latency under high-load conditions.  
**File**: `04_performance_testing.py`  
**README**: [README.md](04_performance_testing/README.md)

### 05. Resilience Testing
**Description**: Tests how Kafka handles producer and consumer failures.  
**File**: `05_resilience_testing.py`  
**README**: [README.md](05_resilience_testing/README.md)

### 06. Simulating Failures
**Description**: Simulates Kafka broker failures and network disruptions.  
**File**: `06_simulating_failures.py`  
**README**: [README.md](06_simulating_failures/README.md)

### 07. Custom Docker Image
**Description**: Creates and tests a custom Kafka Docker image with specific configurations.  
**File**: `07_custom_docker_image.py`  
**Dockerfile**: `Dockerfile`  
**README**: [README.md](07_custom_docker_image/README.md)

### 08. Schema Evolution
**Description**: Tests Kafka schema evolution using Avro or Protobuf.  
**File**: `08_schema_evolution.py`  
**README**: [README.md](08_schema_evolution/README.md)

### 09. Data Migration Testing
**Description**: Uses Kafka for migrating data between different database systems.  
**File**: `09_data_migration_testing.py`  
**README**: [README.md](09_data_migration_testing/README.md)

### 10. Multi-Broker Clusters
**Description**: Simulates and tests Kafka running in a multi-broker cluster setup.  
**File**: `10_multi_broker_clusters.py`  
**README**: [README.md](10_multi_broker_clusters/README.md)

### 11. Simulating Network Interruptions
**Description**: Tests Kafka’s ability to recover from network disruptions.  
**File**: `11_simulating_network_interruptions.py`  
**README**: [README.md](11_simulating_network_interruptions/README.md)

### 12. Distributed Transactions
**Description**: Implements distributed transactions across multiple Kafka topics.  
**File**: `12_distributed_transactions.py`  
**README**: [README.md](12_distributed_transactions/README.md)

### 13. Testing with Mock Services
**Description**: Mocks external services that interact with Kafka for better test control.  
**File**: `13_testing_with_mock_services.py`  
**README**: [README.md](13_testing_with_mock_services/README.md)

### 14. Security Testing
**Description**: Tests Kafka’s authentication, authorization, and encryption mechanisms.  
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
   pip install testcontainers kafka-python pytest
   ```
3. **Kafka Container Not Starting**: Ensure sufficient system resources (memory, CPU) are available for Docker to start Kafka.

For more troubleshooting tips, refer to the troubleshooting guide.

---

## **Conftest.py**
The `conftest.py` file is used to define fixtures that can be shared across multiple test files. It typically contains setup code for Testcontainers, allowing you to initialize and manage Kafka container instances for testing purposes.

---

## **Contributing**
Feel free to contribute by adding new examples, improving existing ones, or reporting issues.

---

## 🚀 Happy Testing with Kafka and Testcontainers! 🎉

