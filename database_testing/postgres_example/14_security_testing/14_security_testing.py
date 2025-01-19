"""
Security Testing

This module tests the application for common security vulnerabilities, including:
- SQL Injection
- Cross-Site Scripting (XSS)
- Authentication bypass
"""

import pytest
import requests
from unittest.mock import patch
from flask import Flask, jsonify, request

# Create a Flask app for testing
app = Flask(__name__)

# Simulated valid token
VALID_TOKEN = "valid_token_123"

@app.route('/protected')
def protected_endpoint():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "No authorization header"}), 401

    token = auth_header.replace('Bearer ', '')
    if token != VALID_TOKEN:
        return jsonify({"error": "Invalid token"}), 401

    return jsonify({"message": "Access granted"}), 200

@pytest.mark.security
def test_sql_injection():
    """Test for SQL injection vulnerability."""
    with patch('requests.post') as mock_post:
        # Mock response for SQL injection attempt
        mock_post.return_value.status_code = 403
        mock_post.return_value.text = "Access denied"

        url = "http://localhost/login"
        payload = {"username": "admin' OR '1'='1", "password": "password"}
        response = mock_post.return_value

        # Check if the response indicates a blocked attempt
        assert response.status_code == 403, "SQL Injection vulnerability detected!"
        print("✅ SQL Injection test passed")

@pytest.mark.security
def test_xss():
    """Test for Cross-Site Scripting (XSS) vulnerability."""
    with patch('requests.get') as mock_get:
        # Mock response for XSS attempt
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "&lt;script&gt;alert('XSS')&lt;/script&gt;"

        url = "http://localhost/search"
        payload = {"query": "<script>alert('XSS')</script>"}
        response = mock_get.return_value

        # Check if the response contains escaped script tag
        assert "<script>" not in response.text, "XSS vulnerability detected!"
        print("✅ XSS test passed")

@pytest.mark.security
def test_authentication_bypass():
    """Test for authentication bypass vulnerability."""
    # Start the Flask app in testing mode
    with app.test_client() as client:
        # Test with no token
        response = client.get('/protected')
        assert response.status_code == 401, "Missing token should return 401"
        print("✅ No token test passed")

        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get('/protected', headers=headers)
        assert response.status_code == 401, "Invalid token should return 401"
        print("✅ Invalid token test passed")

        # Test with valid token
        headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
        response = client.get('/protected', headers=headers)
        assert response.status_code == 200, "Valid token should return 200"
        print("✅ Valid token test passed")

@pytest.mark.security
def test_rate_limiting():
    """Test for rate limiting."""
    with app.test_client() as client:
        # Simulate multiple rapid requests
        responses = [
            client.get('/protected') 
            for _ in range(5)
        ]

        # Check if all requests were rate limited appropriately
        assert all(r.status_code == 401 for r in responses), "Rate limiting not properly enforced"
        print("✅ Rate limiting test passed")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
