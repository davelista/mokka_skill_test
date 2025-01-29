echo "Starting database scripts.."

# Create DB
echo "Creating DB..."
python scripts/create_db.py

# Insert users
echo "Inserting users..."
python scripts/add_users.py

# Insert products
echo "Inserting products..."
python scripts/add_products.py

# Insert orders
echo "Insert orders..."
python scripts/add_orders.py

# Insert order details
echo "Insert order details..."
python scripts/add_order_details.py

echo "DONE!"