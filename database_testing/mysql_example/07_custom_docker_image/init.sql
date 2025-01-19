-- Create a table for guests
CREATE TABLE IF NOT EXISTS guests (
    guest_id INT AUTO_INCREMENT PRIMARY KEY,
    guest_name VARCHAR(50) NOT NULL,
    room_number INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL
);

-- Insert sample data
INSERT INTO guests (guest_name, room_number, check_in, check_out) VALUES
('Alice', 101, '2024-12-20', '2024-12-25'),
('Bob', 102, '2024-12-22', '2024-12-27'),
('Charlie', 103, '2024-12-23', '2024-12-28');
