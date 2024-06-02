import sqlite3

# Replace 'database.db' with the desired path and filename for your database
db_path = 'database.db'

# Connect to the database (this will create it if it doesn't exist)
conn = sqlite3.connect(db_path)
conn.close()
