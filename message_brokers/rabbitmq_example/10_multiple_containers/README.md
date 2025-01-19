# Example 10: Multiple Containers

This example demonstrates how to manage multiple containers using a message broker, focusing on coordinating communication between different services. The example covers:

- Setting up multiple containers for different services.
- Sending messages between containers.
- Handling inter-service communication and error management.

---

## Features

### Multi-Container Setup

- Use Docker Compose to define and run multiple containers for different services (e.g., web service, message broker, database).
- Ensure that all services can communicate with each other.

### Inter-Service Communication

- Send messages between services using the message broker.
- Confirm successful message delivery and processing.

### Error Management

- Handle errors that may occur during inter-service communication.
- Implement retry mechanisms and logging for failed messages.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

For RabbitMQ:
```bash
pip install pika
```
or
```bash
pip3 install pika
```

For Kafka:
```bash
pip install kafka-python
```
or
```bash
pip3 install kafka-python
```

For Redis:
```bash
pip install redis
```
or
```bash
pip3 install redis
```

---

### 2. Set Up Docker Compose

Create a `docker-compose.yml` file to define the services:

```yaml
version: '3'
services:
  message-broker:
    image: rabbitmq:3
    ports:
      - "5672:5672"
  web-service:
    build: ./web-service
    depends_on:
      - message-broker
  database:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
```

---

### 3. Run the Multi-Container Setup

Start the services using Docker Compose:
```bash
docker-compose up -d
```

---

### 4. Run the Test

Execute the test file using pytest:
```bash
python -m pytest 10_multiple_containers.py -v -s
```
or
```bash
python3 -m pytest 10_multiple_containers.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/03080db2-cccb-4317-bbc6-6aa154c3c904)
