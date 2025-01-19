# Example 07: Custom Docker Image

This example demonstrates how to create and use a custom Docker image for a message broker, focusing on configuring the environment for specific application needs. The example covers:

- Building a custom Docker image for the message broker.
- Running the custom image in a containerized environment.
- Testing the integration with the application.

---

## Features

### Custom Docker Image Creation

- Create a Dockerfile to define the custom image for the message broker.
- Build the Docker image with specific configurations and dependencies.

### Running the Custom Image

- Run the custom Docker image in a container.
- Ensure that the message broker is accessible and functioning as expected.

### Integration Testing

- Test the integration of the application with the custom Docker image.
- Validate that messages are sent and received correctly.

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

### 2. Build the Custom Docker Image

Navigate to the directory containing the `Dockerfile` and run:
```bash
docker build -t your_custom_rabbitmq_image:latest .
```

---

### 3. Run the Custom Docker Image

Run the Docker container:
```bash
docker run -d --name message-broker -p 5672:5672 your_custom_rabbitmq_image:latest
```

---

### 4. Run the Test

Execute the test file using pytest:
```bash
python -m pytest 07_custom_docker_image.py -v -s
```
or
```bash
python3 -m pytest 07_custom_docker_image.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/a5de6ad5-a88a-498f-8cd3-51945640e4ce)
