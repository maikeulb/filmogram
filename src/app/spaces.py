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

print(Config.FLASKS3_REGION)
print(Config.FLASKS3_BUCKET_DOMAIN)
print(Config.AWS_ACCESS_KEY_ID)
print(Config.AWS_SECRET_ACCESS_KEY)
print(Config.FLASKS3_BUCKET_NAME)


def upload_photo(file, bucket_name, acl="public-read"):
    client.upload_fileobj(file, bucket_name, file.filename)


def create_bucket():
    if (Config.FLASKS3_BUCKET_NAME not in [space['Name'] for space in
                                           client.list_buckets()['Buckets']]):
        client.create_bucket(Bucket=Config.FLASKS3_BUCKET_NAME)
