# Example 7: Custom Docker Image

This example demonstrates how to use a custom Docker image with Testcontainers to test database functionality. Instead of using the default MySQL image, we create a custom Docker image with preloaded data and additional configurations.

## Features

- **Custom Docker Image**: Build and use a custom MySQL Docker image for testing.
- **Preloaded Data**: Automatically initialize the database with sample data using an SQL script.
- **Custom Configuration**: Add custom MySQL configurations to the container.
- **Automated Testing**: Verify the functionality of the custom image using pytest and Testcontainers.

## Directory Structure

```
07_custom_docker_image/
├── 07_custom_docker_image.py   # Main test file
├── Dockerfile                  # Dockerfile to build the custom image
├── init.sql                    # SQL script to initialize the database
├── conftest.py                 # Pytest configuration file
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation for this example
```

## Prerequisites

- **Docker**: Ensure Docker is installed and running on your system.
- **Python 3.7+**: Required for running the tests.
- **pip**: Python package manager for installing dependencies.

## Building the Custom Docker Image

Build the Docker image:
```bash
docker build -t custom-mysql:1.0 .
```
This command will create a Docker image named `custom-mysql:1.0` with the preloaded data and custom configurations.

## Installing Dependencies

Install the required Python dependencies using pip:
```bash
pip install -r requirements.txt
```
or
```bash
pip3 install -r requirements.txt
```
## Running the Tests

Run the tests using pytest:
```bash
python 07_custom_docker_image.py -v -s
```
or
```bash
python3 07_custom_docker_image.py -v -s
```
The `-v` flag enables verbose output, and the `-s` flag ensures that print statements are displayed in the console.

## Expected Output

If everything is set up correctly, you should see the following output:

![image](https://github.com/user-attachments/assets/46046a53-a270-4df1-9b5e-b47ed801455b)


## Key Takeaways

- **Custom Docker Images**: Allow for preloading data and applying custom configurations.
- **Testcontainers**: Makes it easy to integrate custom images into automated tests.
- **Preloaded Data**: Simplifies testing by providing a consistent starting state.

