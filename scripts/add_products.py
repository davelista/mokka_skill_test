import sqlite3
import pandas as pd

# DB connection
conn = sqlite3.connect('mokka.db')
cursor = conn.cursor()

# Load CSV
csv_file = "csv/products.csv"

# Create dataframe
df = pd.read_csv(csv_file)

# Check if price is numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Remove rows if model is duplicates
df = df.drop_duplicates(subset=['model'])

# Drop rows with missing value
df = df.dropna(subset=['model', 'price'])

# Insert products into DB
for index, row in df.iterrows():
    try:
        cursor.execute("""
                    INSERT INTO products (model, description, price) 
                    VALUES (?, ?, ?)
                """, (row['model'], row.get('description', ''), row['price']))
    except sqlite3.IntegrityError:
        print("ERROR: Product {} is skipped".format(row['model']))
        continue

print("All products added to database")
conn.commit()
conn.close()