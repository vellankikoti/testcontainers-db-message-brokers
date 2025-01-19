-- Create tables
CREATE TABLE hotels (
    hotel_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5)
);

CREATE TABLE amenities (
    amenity_id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(hotel_id),
    name VARCHAR(50) NOT NULL,
    description TEXT
);

-- Insert sample data
INSERT INTO hotels (name, location, rating) VALUES
    ('Grand Hotel', 'New York', 5),
    ('Seaside Resort', 'Miami', 4),
    ('Mountain Lodge', 'Denver', 4);

INSERT INTO amenities (hotel_id, name, description) VALUES
    (1, 'Swimming Pool', 'Heated indoor pool'),
    (1, 'Spa', 'Full-service spa with massage'),
    (2, 'Beach Access', 'Private beach access'),
    (3, 'Ski Storage', 'Heated ski storage room');
