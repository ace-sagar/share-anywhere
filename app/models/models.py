"""
    To populate the mock data into the DB
"""
import sqlite3

def init_db():
    conn = sqlite3.connect('file_sharing.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT NOT NULL,
        storage_provider TEXT NOT NULL,
        owner_id INTEGER,
        FOREIGN KEY (owner_id) REFERENCES users (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS permissions (
        file_id INTEGER,
        user_id INTEGER,
        permission_type TEXT NOT NULL,
        FOREIGN KEY (file_id) REFERENCES files (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        PRIMARY KEY (file_id, user_id, permission_type)
    )
    ''')

    conn.commit()
    conn.close()

def insert_users_data():
    conn = sqlite3.connect('file_sharing.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO users (name, email) VALUES ('Sagar Panwar', 'sagar.panwar@acelucid.com')
        ''')
    cursor.execute('''
        INSERT OR IGNORE INTO users (name, email) VALUES ('Sagar Panwar Gmail', 'sagarpanwar0123@gmail.com')
        ''')
    
    conn.commit()
    conn.close()


def insert_file_data():
    conn = sqlite3.connect('file_sharing.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO files (file_path, storage_provider, owner_id) VALUES ("container/Paper+--+DRUMGAN+-+SYNTHESIS+OF+DRUM+SOUNDS+WITH+TIMBRAL+FEATURE+CONDITIONING+USING+GENERATIVE+ADVERSARIAL+NETWORKS.pdf", 'aws', 1)
        ''')
    cursor.execute('''
        INSERT OR IGNORE INTO files (file_path, storage_provider, owner_id) VALUES ('container/shared image.png', 'aws', 2)
        ''')
    
    conn.commit()
    conn.close()

# init_db()
# insert_users_data()
# insert_file_data()