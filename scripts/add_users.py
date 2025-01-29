import sqlite3
import pandas as pd
import bcrypt

# Function to hash a password
def hash(plain_password):
    salt = bcrypt.gensalt()  # Generate a salt
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)  # Hash password
    return hashed.decode('utf-8')  # Convert bytes to string for storage

# DB connection
conn = sqlite3.connect('mokka.db')
cursor = conn.cursor()

# Load CSV
csv_file = "csv/users.csv"

# Create dataframe
df = pd.read_csv(csv_file)

df = df.drop_duplicates(subset=['email'])

df = df.dropna(subset=['email'])

for index, row in df.iterrows():
    try:
        hashed = hash(row['password'])
        cursor.execute("""
            INSERT INTO users (email, username, firstname, lastname, password, is_admin, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (row['email'], row['username'], row['firstname'], row['lastname'], hashed, row['is_admin']))

    except sqlite3.IntegrityError:
        print("ERROR: User {} is skipped".format(row['email']))
        continue

print("All users added to database")
conn.commit()
conn.close()