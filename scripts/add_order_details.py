import sqlite3
import pandas as pd

# DB connection
conn = sqlite3.connect('mokka.db')
cursor = conn.cursor()

# Load CSV
csv_file = "csv/order_details.csv"

# Create dataframe
df = pd.read_csv(csv_file)

# Check if quantity is numeric
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
# Check if quantity is numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Drop rows with missing value
df = df.dropna(subset=['order_id', 'quantity', 'price'])
# Remove rows if model is duplicates
df = df.drop_duplicates(subset=['order_id'])

# Insert products into DB
for index, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO order_details (id, order_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?, ?) 
        """, (row['id'], row['order_id'], row['product_id'], row['quantity'], row['price']))

    except sqlite3.IntegrityError:
        print("ERROR: Order details {} is skipped".format(row['order_id']))
        continue

print("All order details added to database")
conn.commit()
conn.close()