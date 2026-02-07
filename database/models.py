CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    role VARCHAR(20) NOT NULL CHECK (role IN ('client', 'driver')),
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_DRIVERS_TABLE = """
CREATE TABLE IF NOT EXISTS drivers (
    user_id BIGINT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    car_model VARCHAR(100) NOT NULL,
    car_number VARCHAR(20) NOT NULL
);
"""

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL REFERENCES users(id),
    people_count INT NOT NULL CHECK (people_count BETWEEN 1 AND 4),
    address TEXT NOT NULL,
    price INT NOT NULL,
    direction VARCHAR(50) NOT NULL CHECK (direction IN ('mangit_nukus', 'nukus_mangit')),
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'taken', 'cancelled')),
    driver_id BIGINT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INIT_DB = [
    CREATE_USERS_TABLE,
    CREATE_DRIVERS_TABLE,
    CREATE_ORDERS_TABLE
]