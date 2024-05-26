import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('file_sharing.db')
cursor = conn.cursor()

# Create the "users" table
cursor.execute(''' CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY,
        owner_email TEXT,
        recipient_email TEXT,
        file_name TEXT,
        container TEXT,
        bucket_name TEXT, 
        provider TEXT,
        permission TEXT,
        token TEXT,
        is_active INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table created successfully.")
