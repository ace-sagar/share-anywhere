import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('file_sharing.db')
cursor = conn.cursor()

# Create the "users" table
cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

# Create the "files" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        remote_path TEXT,
        generated_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Create the "permissions" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS permissions (
        id INTEGER PRIMARY KEY,
        file_id INTEGER,
        user_id INTEGER,
        permission_type TEXT,
        FOREIGN KEY (file_id) REFERENCES files(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Tables created successfully.")
