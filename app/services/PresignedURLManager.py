from typing import Any
import boto3

from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file

class PresignedURLManager():
    # AWS credentials
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    REGION_NAME = os.getenv("REGION_NAME")
    BUCKET_NAME = os.getenv("BUCKET_NAME")

    def __init__(self) -> None:
        # Initialize the S3 client
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region_name=self.REGION_NAME
        )

    def generate_presigned_url(self, object_name: str, expiration: int = 3600) -> (Any | None):
        """
        Generate a presigned URL for an S3 object

        :param bucket: Bucket name
        :param object_name: S3 object name
        :param expiration: Expiration time in seconds
        :return: Presigned URL as string. If error, returns None.
        """
        try:
            response = self.s3.generate_presigned_url('get_object',
                                                Params={'Bucket': self.BUCKET_NAME,
                                                        'Key': object_name},
                                                ExpiresIn=expiration)
        except Exception as e:
            print(e)
            return None

        return response
