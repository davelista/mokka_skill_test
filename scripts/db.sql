-- users(id:pk, email, username, name, lastname, password, is_admin)

CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    email VARCHAR(320) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin INTEGER NOT NULL CHECK(is_admin IN (0,1)) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ensure the trigger does not exist before creating it
DROP TRIGGER IF EXISTS update_users_timestamp;

-- Trigger to automatically update the "updated_at" field when a user is modified
CREATE TRIGGER update_users_timestamp
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- products(id:pk, model, description, price)
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    model TEXT UNIQUE NOT NULL,
    description TEXT,
    price REAL NOT NULL CHECK (price >= 0)
);

-- orders(id:pk, user_id: fk, status, created_at:, updated_at)
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    status TEXT CHECK(status in ('pending', 'shipped', 'delivered', 'cancelled')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Ensure the trigger does not exist before creating it
DROP TRIGGER IF EXISTS update_orders_timestamp;

-- Trigger to automatically update the "updated_at" field when a product is modified
CREATE TRIGGER update_orders_timestamp
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    UPDATE orders SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- order_details(id:pk, order_id:fk, product_id:fk, quantity, price)
CREATE TABLE IF NOT EXISTS order_details (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    price REAL NOT NULL CHECK(price >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);