import sqlite3

# DB connection
conn = sqlite3.connect("mokka.db")
cursor = conn.cursor()

# Read the SQL script file
with open("scripts/db.sql", "r") as f:
    sql_script = f.read()

# Execute the SQL script
cursor.executescript(sql_script)

print("Database successfully created")
conn.commit()
conn.close()