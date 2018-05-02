import os
import uuid
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


def upload_file(file, filename=None, bucket_name=Config.FLASKS3_BUCKET_NAME,
                content_type='image/jpg'):
    if filename == None:
        _, ext = os.path.splitext(file.filename)
        filename = str(uuid.uuid4()) + ext
        content_type = file.content_type

    if (bucket_name in [space['Name'] for space in client.list_buckets()['Buckets']]):
        file = client.upload_fileobj(file, bucket_name, filename, ExtraArgs={
            'ContentType': content_type, 'ACL': "public-read"})
        return "{}{}".format(Config.FLASKS3_BUCKET_DOMAIN, filename)


def create_bucket(bucket_name=Config.FLASKS3_BUCKET_NAME):
    if (bucket_name not in [space['Name'] for space in client.list_buckets()['Buckets']]):
        client.create_bucket(Bucket=bucket_name)
