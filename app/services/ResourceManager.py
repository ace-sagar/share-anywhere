import sqlite3
from app.utils.helper_functions import generate_token
from app.utils.types import Message

import os
from dotenv import load_dotenv
load_dotenv()

class ResourceManager():
    
    def __init__(self) -> None:
        # DB Config
        self.db_name = os.getenv("DATABASE_NAME")
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
    
    def grant_access(
            self,
            owner_email: str, 
            recipient_email: str, 
            file_name: str,
            container: str, 
            bucket_name: str, 
            provider: str,
            permission: str
    ) -> list[str]:
        try:
            # Verify if permission is already exists
            self.cursor.execute('''SELECT * FROM resources WHERE owner_email=? AND recipient_email=? AND file_name=?''', 
                (owner_email, recipient_email, file_name))
            isFileAlreadyShared = self.cursor.fetchone()

            if isFileAlreadyShared:
                if isFileAlreadyShared[9] == 1:
                    return [Message.ALREADY_SHARED.value]
                elif isFileAlreadyShared[9] == 0:
                    # Update the permission
                    self.cursor.execute('''UPDATE resources SET is_active=? WHERE owner_email=? AND recipient_email=? AND file_name=?''', 
                        (1, owner_email, recipient_email, file_name)
                    )
                    return [Message.PERMISSION_UPDATED.value]
            else:
                # Grant permission
                token = generate_token()
                self.cursor.execute('''
                    INSERT OR IGNORE INTO resources (owner_email, recipient_email, file_name, container, bucket_name, provider, permission, token, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (owner_email, recipient_email, file_name, container, bucket_name, provider, permission, token, 1)
                )
                
                # Purpose: To verify the outcome of a successful SQL operation.
                if self.cursor.lastrowid:
                    return [Message.SHARED.value, token]
                else:
                    return [Message.ERROR.value]
        except sqlite3.Error as e:
            # Purpose: To handle any exceptions or errors that occur during the execution of the SQL operation. Rollback transaction on error.
            self.conn.rollback()
            print('Exception on share file: ', e)
            return [Message.ERROR.value]

    def get_resource_details(self, token):
        try:
            token = str(token)
            self.cursor.execute('''SELECT file_name FROM resources WHERE token=?''', (token, ))
            result = self.cursor.fetchone()
            
            return result if result else None        
        except Exception as e:
            print('Get token Exception: ', e)
            return Message.ERROR
    
    def is_valid_token(self, token: str):
        try:
            token = str(token)
            self.cursor.execute('''SELECT * FROM resources WHERE token=? AND is_active=?''', (token, 1))

            return True if self.cursor.fetchone() else False
        except Exception as e:
            print('Is Token Exists Exception: ', e)
            return Message.ERROR
        

    def remove_access(self, token: str):
        try:
            token = str(token)
            self.cursor.execute('''SELECT * FROM resources WHERE token=?''', (token,))
            if not self.cursor.fetchone():
                return Message.TOKEN_NOT_FOUND.value

            self.cursor.execute('''UPDATE resources SET is_active=? WHERE token=?''', (0, token))
            
            return Message.PERMISSION_REMOVED.value if self.cursor.rowcount > 0 else None       
        except Exception as e:
            print('Remove token Exception: ', e)
            return Message.ERROR