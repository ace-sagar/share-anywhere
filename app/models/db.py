# from datetime import datetime
# from sqlalchemy import DateTime, ForeignKey, create_engine, Column, Integer, String, inspect
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import relationship

# # Database Config
# SQLALCHEMY_DATABASE_URL = "sqlite:///./file_sharing.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, 
#                     execution_options={
#                         "sqlite_raw_colnames": True,
#                         "sqlite_foreign_keys": True,
#                     })
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Tables list

# class Users(Base):
#     __table__ = "Users"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     name = Column(String, index=True)
#     email = Column(String, index=True)

# class Files(Base):
#     __tablename__ = "Files"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     ownerId = Column(Integer, ForeignKey("Users.id"))

#     users = relationship("Files", back_populates="Users")

# class Permissions(Base):
#     __tablename__ = "Permissions"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     ownerId = Column(Integer, ForeignKey("Users.id"))
#     fileId = Column(Integer, ForeignKey("Files.id"))
#     permission = Column(String, index=True)

#     users = relationship("Permissions", back_populates="Users")

# def create_tables():
#     print("Creating table(s) ...")
#     Base.metadata.create_all(bind=engine)


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
        file_path TEXT,
        storage_provider TEXT,
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
