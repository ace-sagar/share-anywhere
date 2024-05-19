import sqlite3
from typing import Any, Literal
import boto3

from app.utils.types import Message

class MockDataManger():

    def __init__(self, db_name) -> None:
        # Initialize the S3 client
        self.s3 = boto3.client('s3')

        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("Database connection established")

    def insert(self):
        # Users
        self.cursor.execute(
            '''
                INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
            ''',
            ("Sagar Panwar", "sagar.panwar@acelucid.com")
        )
        self.cursor.execute(
            '''
                INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
            ''',
            ("Shivam Rawat", "shivam.rawat@acelucid.com")
        )
        self.cursor.execute(
            '''
                INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
            ''',
            ("Himanshu Aswal", "himanshu.aswal@acelucid.com")
        )
        self.cursor.execute(
            '''
                INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
            ''',
            ("Robin Gusain", "birobin.gusain@acelucid.com")
        )
        self.cursor.execute(
            '''
                INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
            ''',
            ("Akash Rawat", "akash.rawat@acelucid.com")
        )

        # Files
        self.cursor.execute(
            '''
                INSERT OR IGNORE INTO files (file_path, storage_provider, user_id) VALUES (?, ?, ?)
            ''',
            ("container/shared image.png", "aws", 2)
        )
        self.cursor.execute(
            '''
                INSERT OR IGNORE INTO files (file_path, storage_provider, user_id) VALUES (?, ?, ?)
            ''',
            ("container/Paper+--+DRUMGAN+-+SYNTHESIS+OF+DRUM+SOUNDS+WITH+TIMBRAL+FEATURE+CONDITIONING+USING+GENERATIVE+ADVERSARIAL+NETWORKS.pdf", "aws", 3)
        )
    