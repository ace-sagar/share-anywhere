import sqlite3
from typing import Any, Literal
import boto3

from app.utils.types import Message

class ResourceManage():

    def __init__(self, db_name) -> None:
        # Initialize the S3 client
        self.s3 = boto3.client('s3')

        # DB Config
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.isolation_level = None  # Enable autocommit mode
            self.cursor = self.conn.cursor()
            print("Database connection established")
        except sqlite3.Error as e:
            print("Error connecting to the database:", e)

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def share_file(self, file_id: int, owner_id: int, recipient_id: int, permission_type: str) -> Literal[Message.PERMISSION_DENIED, Message.DENIED_ACTION, Message.NOT_FOUND, Message.SHARED_SUCCESS]:
        try:
            # # Verify owner permissions
            self.cursor.execute('SELECT * FROM files WHERE id=? AND user_id=?', (file_id, owner_id))
            isOwner = self.cursor.fetchone()
            if not isOwner:
                return Message.PERMISSION_DENIED
            
            # Verify if permission is already exists
            self.cursor.execute('SELECT * FROM permissions WHERE file_id=? AND user_id=?', (file_id, recipient_id))
            permissionAlreadyExist = self.cursor.fetchone()
            if permissionAlreadyExist:
                return Message.FILE_ALREADY_SHARED
            
            # Grant permission
            self.cursor.execute('''INSERT OR IGNORE INTO permissions (file_id, user_id, permission_type) VALUES (?, ?, ?)''', 
                                (file_id, recipient_id, permission_type))

            return Message.SHARED_SUCCESS
        except sqlite3.Error as e:
            # Rollback transaction on error
            self.conn.rollback()
            print('Exception: ', e)
            return Message.ERROR
   
    def generate_presigned_url(self, bucket, object_name, expiration=3600) -> (Any | None):
        """Generate a presigned URL for an S3 object

        :param bucket: Bucket name
        :param object_name: S3 object name
        :param expiration: Expiration time in seconds
        :return: Presigned URL as string. If error, returns None.
        """
        try:
            response = self.s3.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket,
                                                        'Key': object_name},
                                                ExpiresIn=expiration)
        except Exception as e:
            print(e)
            return None

        return response

    def check_access(self, user_id: int, file_id: int, required_permission: str) -> (bool | Literal[Message.ERROR]):
        try:
            # Check if the user has the required permission
            self.cursor.execute('''
            SELECT * FROM permissions WHERE file_id=? AND user_id=? AND permission_type=?
            ''', (file_id, user_id, required_permission))

            has_permission = (self.cursor.fetchone()) is not None

            return has_permission
        except Exception as e:
            print('Exception: ', e)
            return Message.ERROR

    def access_file(self, user_id: int, file_id: int, action: str):
        try:
            # Fetch file details
            self.cursor.execute('SELECT file_path, storage_provider FROM files WHERE id=?', (file_id,))
            file = self.cursor.fetchone()
            if not file:
                return "File not found"

            file_path, storage_provider = file

            # Check user permissions
            if not self.check_access(user_id, file_id, action):
                return Message.DENIED_ACTION

            # Generate presigned URL for file access
            bucket = file_path.split('/')[0]
            object_name = '/'.join(file_path.split('/')[1:])
            presigned_url = self.generate_presigned_url(bucket, object_name)

            return presigned_url if presigned_url else "Error generating presigned URL"
        except Exception as e:
            print('Exception: ', e)
            return Message.ERROR

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
            return file[0]
        except Exception as e:
            print('Exception: ', e)
            return Message.ERROR
        
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
            print('Exception: ', e)
            return Message.ERROR