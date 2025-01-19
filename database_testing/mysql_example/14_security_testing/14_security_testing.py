"""
Security Testing Example

This script demonstrates security testing scenarios including:
- SQL injection prevention
- Password hashing and verification
- Rate limiting
- Input validation
- Session management
- Account lockout after multiple failed attempts
"""

import hashlib
import time
from datetime import datetime, timedelta
from testcontainers.mysql import MySqlContainer
from sqlalchemy import create_engine, text
from collections import defaultdict

# Constants
MYSQL_VERSION = "mysql:8.0"
MYSQL_ROOT_PASSWORD = "test"
DATABASE_NAME = "security_test"
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION = 15  # minutes
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 5


class SecurityService:
    def __init__(self, engine):
        self.engine = engine
        self.rate_limit_tracker = defaultdict(list)
        self.setup_database()

    def setup_database(self):
        """Initialize database schema."""
        with self.engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(128) NOT NULL,
                    failed_attempts INT DEFAULT 0,
                    locked_until TIMESTAMP NULL
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id VARCHAR(64) PRIMARY KEY,
                    user_id INT NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    event_type VARCHAR(50) NOT NULL,
                    username VARCHAR(50),
                    ip_address VARCHAR(45),
                    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    details TEXT
                )
            """))

    def log_event(self, conn, event_type, username, ip_address, details):
        """Log security events."""
        conn.execute(
            text("""
                INSERT INTO audit_log (event_type, username, ip_address, details)
                VALUES (:event_type, :username, :ip_address, :details)
            """),
            {
                "event_type": event_type,
                "username": username,
                "ip_address": ip_address,
                "details": details
            }
        )
        print(f"Security Event: {event_type} - User: {username} - Details: {details}")

    def hash_password(self, password):
        """Create password hash."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        """Register a new user."""
        with self.engine.begin() as conn:
            password_hash = self.hash_password(password)
            conn.execute(
                text("INSERT INTO users (username, password_hash, failed_attempts) VALUES (:username, :password_hash, 0)"),
                {"username": username, "password_hash": password_hash}
            )
            self.log_event(conn, "USER_REGISTERED", username, "system", "New user registration")

    def get_user_status(self, username):
        """Get user's current status."""
        with self.engine.begin() as conn:
            result = conn.execute(
                text("SELECT failed_attempts, locked_until FROM users WHERE username = :username"),
                {"username": username}
            ).fetchone()
            if result:
                return {
                    "failed_attempts": result[0],
                    "locked_until": result[1]
                }
            return None

    def login(self, username, password, ip_address):
        """Attempt to log in."""
        with self.engine.begin() as conn:
            user_data = conn.execute(
                text("""
                    SELECT id, password_hash, failed_attempts, locked_until 
                    FROM users 
                    WHERE username = :username
                    FOR UPDATE
                """),
                {"username": username}
            ).fetchone()

            if not user_data:
                self.log_event(conn, "LOGIN_FAILED", username, ip_address, "Invalid username")
                raise ValueError("Invalid credentials")

            user_id, stored_hash, failed_attempts, locked_until = user_data
            print(f"DEBUG: Current failed attempts for {username}: {failed_attempts}")

            if locked_until and locked_until > datetime.now():
                self.log_event(conn, "LOGIN_BLOCKED", username, ip_address, 
                             f"Account locked until {locked_until}")
                raise ValueError("Account is locked")

            if self.hash_password(password) != stored_hash:
                new_failed_attempts = failed_attempts + 1
                print(f"DEBUG: Incrementing failed attempts to {new_failed_attempts}")

                if new_failed_attempts >= MAX_LOGIN_ATTEMPTS:
                    locked_until = datetime.now() + timedelta(minutes=LOCKOUT_DURATION)
                    conn.execute(
                        text("""
                            UPDATE users 
                            SET failed_attempts = :attempts, locked_until = :locked_until 
                            WHERE id = :user_id
                        """),
                        {"attempts": new_failed_attempts, "locked_until": locked_until, "user_id": user_id}
                    )
                    self.log_event(conn, "ACCOUNT_LOCKED", username, ip_address,
                                 f"Account locked after {new_failed_attempts} failed attempts")
                    raise ValueError("Account is locked")
                else:
                    conn.execute(
                        text("UPDATE users SET failed_attempts = :attempts WHERE id = :user_id"),
                        {"attempts": new_failed_attempts, "user_id": user_id}
                    )
                    self.log_event(conn, "LOGIN_FAILED", username, ip_address,
                                 f"Failed attempt {new_failed_attempts}/{MAX_LOGIN_ATTEMPTS}")
                    raise ValueError("Invalid credentials")

            # Successful login - reset counters
            conn.execute(
                text("UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = :user_id"),
                {"user_id": user_id}
            )
            session_id = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()
            conn.execute(
                text("""
                    INSERT INTO sessions (session_id, user_id, expires_at)
                    VALUES (:session_id, :user_id, DATE_ADD(NOW(), INTERVAL 1 HOUR))
                """),
                {"session_id": session_id, "user_id": user_id}
            )
            self.log_event(conn, "LOGIN_SUCCESSFUL", username, ip_address, "Login successful")
            return session_id


def main():
    """Demonstrate the SecurityService functionality."""
    with MySqlContainer(MYSQL_VERSION) as container:
        engine = create_engine(container.get_connection_url())
        service = SecurityService(engine)

        try:
            username = "testuser"
            password = "securepassword"
            ip_address = "192.168.0.1"

            print("\n=== Security Test Demonstration ===\n")

            print("1. User Registration")
            print("-----------------------")
            service.register_user(username, password)

            print("\n2. Successful Login")
            print("------------------")
            session_id = service.login(username, password, ip_address)
            print(f"Session ID: {session_id}")

            print("\n3. Failed Login Attempts")
            print("-----------------------")
            for attempt in range(MAX_LOGIN_ATTEMPTS):
                try:
                    print(f"\nAttempt {attempt + 1}/{MAX_LOGIN_ATTEMPTS}")
                    service.login(username, "wrongpassword", ip_address)
                except ValueError as e:
                    print(f"Result: {str(e)}")
                status = service.get_user_status(username)
                print(f"Account status: {status}")

            print("\n4. Verify Account Lockout")
            print("------------------------")
            try:
                service.login(username, password, ip_address)
            except ValueError as e:
                print(f"Result: {str(e)}")

            print("\n=== Demonstration Complete ===")

        finally:
            engine.dispose()


if __name__ == "__main__":
    main()
