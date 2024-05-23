import sqlite3
from typing import Any
import boto3

class PresignedURLManager():

    def __init__(self, bucket_name: str = "myshareanywhere", object_name: str = "dummy-2.pdf", db_name: str = "", region_name: str = 'ap-south-1', expiration: int = 3600) -> None:
        # Initialize the S3 client
        self.s3 = boto3.client('s3', region_name='ap-south-1')

        self.bucket_name = bucket_name
        self.object_name = object_name
        self.expiration = expiration

    def generate_presigned_url(self) -> (Any | None):
        """
        Generate a presigned URL for an S3 object

        :param bucket: Bucket name
        :param object_name: S3 object name
        :param expiration: Expiration time in seconds
        :return: Presigned URL as string. If error, returns None.
        """
        try:
            response = self.s3.generate_presigned_url('get_object',
                                                Params={'Bucket': self.bucket_name,
                                                        'Key': self.object_name},
                                                ExpiresIn=self.expiration)
        except Exception as e:
            print(e)
            return None

        return response
