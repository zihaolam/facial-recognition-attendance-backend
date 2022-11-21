from base64 import b64encode
from typing import Union
import boto3
import traceback
from utils.s3_helper import BucketNames
from utils.lambda_helpers import LambdaException
from datauri import DataURI


class AmazonRekognition:
    client: boto3.client

    def __init__(self):
        self.client = boto3.client('rekognition')
        self.collection_name = 'ab3-attendance-system'

    def create_new_collection(self):
        try:
            self.client.create_collection(
                CollectionId=self.collection_name)
        except Exception as e:
            print(e)

    def reset_collection(self):
        try:
            self.client.delete_collection(CollectionId=self.collection_name)
            self.client.create_collection(CollectionId=self.collection_name)
            print("reset success")

        except Exception as e:
            print(e)

    def add_face(self, base_64_file: str):
        image = DataURI(base_64_file)

        res = self.client.index_faces(
            CollectionId=self.collection_name,
            Image={
                "Bytes": image.data,
            },
            MaxFaces=1,
        )
        try:
            return res["FaceRecords"][0]["Face"]["FaceId"]
        except KeyError:
            traceback.print_exc()
            raise LambdaException(
                status_code=409, message="Face is not registered")
        except IndexError:
            traceback.print_exc()
            raise LambdaException(
                status_code=409, message="Face not found in image")

    def detect_face(self, base_64_file: str) -> Union[str, None]:
        image = DataURI(base_64_file)
        res = self.client.search_faces_by_image(
            CollectionId=self.collection_name,
            Image={
                'Bytes': image.data,
            },
            FaceMatchThreshold=0.7
        )
        try:
            return res["FaceMatches"][0]["Face"]["FaceId"]
        except IndexError:
            print("No Face Found")
            return None


amazon_rekognition = AmazonRekognition()
