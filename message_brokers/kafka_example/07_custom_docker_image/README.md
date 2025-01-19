# Example 07: Custom Docker Image

This example demonstrates how to use a custom Docker image with Kafka as the message broker. It focuses on building and running a custom image that includes the necessary dependencies for your application. The example covers:

- Creating a custom Docker image for the application.
- Running the Kafka service using the custom image.
- Verifying the functionality of the application with the custom setup.

## Features

### Custom Docker Image

- Build a custom Docker image that includes your application and its dependencies.
- Use the custom image to run Kafka and your application in a containerized environment.

### Verification

- Confirm that the application works correctly with the custom Docker image.
- Ensure that all necessary services are running as expected.

## How to Run the Test

### 1. Build the Custom Docker Image

Create the Docker image using the following command:

```bash
docker build -t custom-kafka-app .
```

### 2. Run the Custom Docker Container

Run the container using the custom image:

```bash
docker run -d --name kafka-app -p 9092:9092 custom-kafka-app
```

### 3. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

For Kafka:
```bash
pip install kafka-python
```

or
```bash
pip3 install kafka-python
```

### 4. Run the Test

Execute the test file using pytest:

For Kafka:
```bash
python -m pytest 07_custom_docker_image.py -v -s
```

or
```bash
python3 -m pytest 07_custom_docker_image.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/ddf318c1-c20c-4777-9175-144f1410ed80)

