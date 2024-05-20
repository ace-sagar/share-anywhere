import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('file_sharing.db')
cursor = conn.cursor()

# Users
cursor.execute(
    '''
        INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
    ''',
    ("Sagar Panwar", "sagar.panwar@acelucid.com")
)
cursor.execute(
    '''
        INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
    ''',
    ("Shivam Rawat", "shivam.rawat@acelucid.com")
)
cursor.execute(
    '''
        INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
    ''',
    ("Himanshu Aswal", "himanshu.aswal@acelucid.com")
)
cursor.execute(
    '''
        INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
    ''',
    ("Robin Gusain", "birobin.gusain@acelucid.com")
)
cursor.execute(
    '''
        INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
    ''',
    ("Akash Rawat", "akash.rawat@acelucid.com")
)

# Files
cursor.execute(
    '''
        INSERT OR IGNORE INTO files (user_id, remote_path, generated_path) VALUES (?, ?, ?)
    ''',
    (2, "https://myshareanywhere.s3.ap-south-1.amazonaws.com/container/notes.png", "2/container/notes.png")
)
cursor.execute(
    '''
        INSERT OR IGNORE INTO files (user_id, remote_path, generated_path) VALUES (?, ?, ?)
    ''',
    (3, "https://myshareanywhere.s3.ap-south-1.amazonaws.com/container/dummy-1.pdf", "3/container/dummy-1.pdf")
)
cursor.execute(
    '''
        INSERT OR IGNORE INTO files (user_id, remote_path, generated_path) VALUES (?, ?, ?)
    ''',
    (5, "https://myshareanywhere.s3.ap-south-1.amazonaws.com/container/dummy-2.pdf", "3/container/dummy-2.pdf")
)
    
# Commit the changes and close the connection
conn.commit()
conn.close()

print("Tables populated successfully.")