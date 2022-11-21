import logging
import os
from typing import Tuple
import boto3
from pathlib import Path
from datauri import DataURI
from uuid import uuid4
import config


class BucketNames:
    USER_BUCKET = "ab3-attendance-user-bucket"


class S3:
    s3_client: boto3.client
    bucket_name: str

    def __init__(self, bucket_name):
        self.s3_endpoint = "https://s3.ap-east-1.amazonaws.com" if config.is_prod else "http://localhost:4569"
        s3_config = dict(
            endpoint_url=self.s3_endpoint,
            aws_access_key_id=None if config.is_prod else "S3RVER",
            aws_secret_access_key=None if config.is_prod else "S3RVER"
        )
        self.s3_client = boto3.client(
            "s3",
            **s3_config
        )
        self.bucket_name = bucket_name

    def generate_presigned_url(
        self, file_name: str = None, resource_url: str = None
    ):
        """generate presigned url for s3 objects
        Args:
            file_name (str): file name
            resource_url (str): if resource_url attached, parse bucket_name and file_name
        Returns:
            str: presigned url of s3 resource
        """
        if not config.is_prod:
            return f"{self.s3_endpoint}/{self.bucket_name}/{file_name}"
        if resource_url is not None:
            resource_url = resource_url.split("/")
            file_name = resource_url[-1]
        return self.s3_client.generate_presigned_url(
            "get_object", ExpiresIn=1200, Params={"Bucket": self.bucket_name, "Key": file_name}
        )

    def upload(self, file_data: str, file_name: str = None) -> str:
        """writes to file from encoded data uri
        Args:
            file_data (str): encoded data uri
            file_name (str): file name to name file to be stored in s3 bucket
        Returns:
            str: file_url
        """
        uri = DataURI(file_data)
        extension = uri.mimetype.split("/")[1]
        file_name = (
            f"{uuid4()}.{extension}" if file_name is None else f"{file_name}.{extension}"
        )
        file_path = os.path.join("tmp", file_name)
        file = Path(file_path)
        file.write_bytes(uri.data)
        self.s3_client.upload_file(file_path, self.bucket_name, file_name)
        file.unlink()

        object_url: str = self.generate_presigned_url(
            file_name)
        object_url = object_url.split("?")[
            0
        ]  # remove query parameters to get absolute path
        return object_url

    def delete(self, file_name: str = None, resource_url: str = None) -> Tuple[str, str]:
        """deletes a file from s3 bucket
        Args:
            bucket_name (str): s3 bucket name
            file_name (str): file to delete name
        Returns:
            Tuple[str, str]: bucket_name, file_name
        """
        if resource_url is not None:
            parsed_resource_url = resource_url.split('/')
            bucket_name, file_name = parsed_resource_url[-2], parsed_resource_url[-1]
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name, Key=file_name)
        except:
            logging.error(
                f"Error deleting object from s3 bucket, bucket name: {bucket_name}, file name: {file_name}")

        return bucket_name, file_name
