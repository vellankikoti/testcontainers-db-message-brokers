import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "custom_docker_image: mark test as using a custom Docker image"
    )
