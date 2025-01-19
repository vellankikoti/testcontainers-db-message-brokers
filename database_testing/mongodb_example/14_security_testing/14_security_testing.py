"""
14_security_testing.py - Security Testing Example

This example demonstrates how to perform security testing on a web application,
focusing on common vulnerabilities such as SQL injection, password hashing,
and input validation.
"""

import pytest
import hashlib
import re

# Function to hash passwords
def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# Function to validate user input
def validate_input(user_input):
    """Validate user input to prevent SQL injection."""
    if re.search(r"[;'\"]", user_input):
        raise ValueError("Invalid input detected.")
    return True

# Test function for password hashing
def test_password_hashing():
    password = "securePassword123"
    hashed = hash_password(password)
    assert hashed == "4dbd5e49147b5102ee2731ac03dd0db7decc3b8715c3df3c1f3ddc62dcbcf86d"  # Correct SHA-256 hash of "securePassword123"

# Test function for valid input
def test_valid_input():
    user_input = "validInput"
    assert validate_input(user_input) is True

# Test function for SQL injection prevention
def test_sql_injection_prevention():
    user_input = "invalidInput'; DROP TABLE users; --"
    with pytest.raises(ValueError, match="Invalid input detected."):
        validate_input(user_input)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
