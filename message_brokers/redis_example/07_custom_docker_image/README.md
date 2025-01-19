# Example 07: Custom Docker Image

This example demonstrates how to create a custom Docker image for the reservation system using Redis as the data store. It focuses on packaging the application and its dependencies into a Docker image for easy deployment. The example covers:

- Creating a Dockerfile for the application.
- Building the Docker image.
- Running the application in a Docker container.

## Features

### Custom Docker Image

- Define a Dockerfile that specifies the application environment and dependencies.
- Build a Docker image using the Docker CLI.
- Run the application in a containerized environment.

### Error Handling

- Handle errors during the image build process.
- Provide appropriate error messages for failed builds or container runs.

## How to Run the Test

### 1. Install Dependencies

Ensure you have Docker installed on your machine. You can download it from [Docker's official website](https://www.docker.com/get-started).

### 2. Build the Docker Image

Navigate to the directory containing the Dockerfile and run the following command:

```bash
docker build -t custom-redis-image .
```

### 3. Run the Tests

Execute the test file using pytest inside the container:

For Redis:
```bash
python -m pytest 07_custom_docker_image.py -v -s
```

or
```bash
python3 -m pytest 07_custom_docker_image.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/16fd3050-b945-4177-840c-69dc23aa8b62)

