import boto3
import botocore
from config import Config
session = boto3.session.Session()

client = session.client(
    "s3",
    region_name='nyc3',
    endpoint_url=Config.S3_ENDPOINT_URL,
    aws_access_key_id=Config.S3_KEY,
    aws_secret_access_key=Config.S3_SECRET
)


def upload_photo(file, bucket_name, acl="public-read"):
    client.upload_fileobj(file, bucket_name, file.filename)


def create_bucket(bucket_name):
    client.create_bucket(Bucket=bucket_name)
