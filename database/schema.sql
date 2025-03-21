CREATE TABLE IF NOT EXISTS  users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    security_question TEXT NOT NULL,
    security_answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vendors (
    id SERIAL PRIMARY KEY,
    service_id INT REFERENCES services(id),
    name VARCHAR(100) NOT NULL,
    location TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS slots (
    id SERIAL PRIMARY KEY,
    vendor_id INT NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
    slot_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    max_people INT NOT NULL DEFAULT 1,
    is_available BOOLEAN DEFAULT TRUE,
    price NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    slot_id INT NOT NULL REFERENCES slots(id) ON DELETE CASCADE,
    people_count INT NOT NULL DEFAULT 1,
    slot_time TIMESTAMP NOT NULL,
    status VARCHAR(20) CHECK (status IN ('confirmed', 'cancelled')) DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

