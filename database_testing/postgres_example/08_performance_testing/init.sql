-- Create tables
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL,
    guest_name VARCHAR(100) NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL
);

-- Insert sample data
INSERT INTO bookings (room_id, guest_name, check_in, check_out, total_price) VALUES
    (1, 'Alice', '2024-01-01', '2024-01-02', 100.00),
    (2, 'Bob', '2024-01-03', '2024-01-04', 200.00),
    (3, 'Charlie', '2024-01-05', '2024-01-06', 300.00);
