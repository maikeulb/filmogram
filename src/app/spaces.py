import boto3
import botocore
from config import Config
session = boto3.session.Session()

client = session.client(
    "s3",
    region_name=Config.FLASKS3_REGION,
    endpoint_url=Config.FLASKS3_ENDPOINT_URL,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
)


def upload_file(file, filename, bucket_name=Config.FLASKS3_BUCKET_NAME):
    if (bucket_name in [space['Name'] for space in client.list_buckets()['Buckets']]):
        client.upload_file(file, bucket_name, filename, ExtraArgs={
                           'ContentType': 'image/jpg', 'ACL': "public-read"})


def create_bucket(bucket_name=Config.FLASKS3_BUCKET_NAME):
    if (bucket_name not in [space['Name'] for space in client.list_buckets()['Buckets']]):
        client.create_bucket(Bucket=bucket_name)
