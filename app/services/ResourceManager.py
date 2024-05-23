import sqlite3
from typing import Literal

from app.utils.types import Message

import uuid

class ResourceManager():

    def __init__(self, db_name) -> None:
        # DB Config
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.isolation_level = None  # Enable autocommit mode
            self.cursor = self.conn.cursor()
            print("Database connection established - Resource")
        except sqlite3.Error as e:
            print("Resource - Error connecting to the database:", e)

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed - Resource")
    
    def share_file(self, file_id: int, owner_id: int, recipient_id: int, permission_type: str) -> Literal[Message.PERMISSION_DENIED, Message.DENIED_ACTION, Message.NOT_FOUND, Message.SHARED_SUCCESS]:
        try:
            # # Verify owner permissions
            self.cursor.execute('SELECT * FROM files WHERE id=? AND user_id=?', (file_id, owner_id))
            isOwner = self.cursor.fetchone()
            if not isOwner:
                return Message.PERMISSION_DENIED.value
            
            # Verify if permission is already exists
            self.cursor.execute('SELECT * FROM permissions WHERE file_id=? AND user_id=?', (file_id, recipient_id))
            permissionAlreadyExist = self.cursor.fetchone()
            if permissionAlreadyExist:
                return Message.FILE_ALREADY_SHARED.value
            
            # Grant permission
            self.cursor.execute('''INSERT OR IGNORE INTO permissions (file_id, user_id, permission_type) VALUES (?, ?, ?)''', 
                                (file_id, recipient_id, permission_type))

            return Message.SHARED_SUCCESS.value
        except sqlite3.Error as e:
            # Rollback transaction on error
            self.conn.rollback()
            print('Share file Exception: ', e)
            return Message.ERROR.value
   
    def check_access(self, user_id: int, file_id: int, required_permission: str) -> (bool | Literal[Message.ERROR]):
        try:
            # Check if the user has the required permission
            self.cursor.execute('''
            SELECT * FROM permissions WHERE file_id=? AND user_id=? AND permission_type=?
            ''', (file_id, user_id, required_permission))

            has_permission = (self.cursor.fetchone()) is not None

            return has_permission
        except Exception as e:
            print('Check Access Exception: ', e)
            return Message.ERROR.value

    def access_file(self, user_id: int, file_id: int, action: str):
        try:
            # Fetch file details
            self.cursor.execute('SELECT file_path, storage_provider FROM files WHERE id=?', (file_id,))
            file = self.cursor.fetchone()
            if not file:
                return Message.NOT_FOUND.value

            file_path, storage_provider = file

            # Check user permissions
            if not self.check_access(user_id, file_id, action):
                return Message.DENIED_ACTION.value

            # Generate presigned URL for file access
            bucket = file_path.split('/')[0]
            object_name = '/'.join(file_path.split('/')[1:])
            presigned_url = self.generate_presigned_url(bucket, object_name)

            return presigned_url if presigned_url else "Error generating presigned URL"
        except Exception as e:
            print('Access File Exception: ', e)
            return Message.ERROR.value

    def get_file_id(self, file_id: str, owner_id: int, remote_path: str, generated_path: str):
        try:
            # Fetch file details
            self.cursor.execute('SELECT id FROM files WHERE id=? AND user_id=?', (file_id, owner_id))
            file = self.cursor.fetchone()

            # If file info not found insert it
            # if not file:
            #     self.cursor.execute(
            #         '''
            #             INSERT OR IGNORE INTO files (user_id, remote_path, generated_path) VALUES (?, ?, ?)
            #         ''',
            #         (owner_id, remote_path, generated_path)
            #     )
            #     file_id = self.cursor.lastrowid

            #     return file_id
            # else:
            #     return file[0]
            return file[0] if file else Message.NOT_FOUND.value
        except Exception as e:
            print('Get File Id Exception: ', e)
            return Message.ERROR.value
        
    def getUserFiles(self, user_id):
        try:
            # Fetch file details
            self.cursor.execute('SELECT * FROM permissions WHERE user_id=?', (user_id,))
            permissions = self.cursor.fetchall()
            file_ids = [p[1] for p in permissions]

            placeholders = ','.join(['?' for _ in range(len(file_ids))])
            query = f'SELECT * FROM files WHERE id IN ({placeholders})'
            self.cursor.execute(query, file_ids)
            user_files = self.cursor.fetchall()

            return user_files
        except Exception as e:
            print('Get User Files Exception: ', e)
            return Message.ERROR.value
        

    def generate_token(self):
        return str(uuid.uuid4())
    
    def get_token(self, email, token):
        try:
            self.cursor.execute('''SELECT * FROM tokens WHERE email=? AND token=?''', (email, token))
            token = self.cursor.fetchone()
            return token
        
        except Exception as e:
            print('Get token Exception: ', e)
            return Message.ERROR
    
    def is_token_already_exists(self, email, token):
        try:
            self.cursor.execute('''SELECT * FROM tokens WHERE email=? AND token=?''', (email, token))
            getToken = self.cursor.fetchone()

            tokenExists = getToken is not None
            if not tokenExists:
                return True
            return False
        except Exception as e:
            print('Is Token Already Exists Exception: ', e)
            return Message.ERROR
    
    def store_token(self, email, token):
        try:
            # Store the token and email mapping in a database (e.g., DynamoDB, RDS, etc.)
            self.cursor.execute('''SELECT * FROM tokens WHERE email=? AND token=?''', (email, token))

            getToken = self.cursor.fetchone()
            tokenAlreadyExists = getToken is not None

            if not tokenAlreadyExists:
                self.cursor.execute('''INSERT OR IGNORE INTO tokens (email, token) VALUES (?, ?)''', (email, token))
                token_id = self.cursor.lastrowid
                self.conn.commit()

                return token_id
            
            return getToken
        except Exception as e:
            print('Store Token Exception: ', e)
            return Message.ERROR
    