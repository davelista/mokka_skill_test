import sqlite3
import pandas as pd

# DB connection
conn = sqlite3.connect('mokka.db')
cursor = conn.cursor()

# Load CSV
csv_file = "csv/orders.csv"

# Create dataframe
df = pd.read_csv(csv_file)

# Drop rows with missing value
df = df.dropna(subset=['id', 'user_id'])
# Remove rows if model is duplicates
df = df.drop_duplicates(subset=['id'])

# Insert products into DB
for index, row in df.iterrows():
    try:
        cursor.execute("""
        INSERT INTO orders(id, user_id, status, created_at, updated_at)  
        VALUES ( ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (row['id'], row['user_id'], row['status']))

    except sqlite3.IntegrityError:
        print("ERROR: Order {} is skipped".format(row['id']))
        continue

print("All orders added to database")
conn.commit()
conn.close()