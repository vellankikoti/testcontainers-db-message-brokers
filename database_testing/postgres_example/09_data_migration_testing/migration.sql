-- Add a new table for payments
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    booking_id INTEGER REFERENCES bookings(booking_id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL
);
