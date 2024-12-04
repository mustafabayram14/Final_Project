import boto3
import os

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "your_access_key")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "your_secret_key")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "profile-pictures")

def setup_minio_bucket():
    client = boto3.client(
        "s3",
        endpoint_url=f"http{'s' if os.getenv('MINIO_SECURE', 'false').lower() == 'true' else ''}://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )
    try:
        client.head_bucket(Bucket=MINIO_BUCKET_NAME)
        print(f"Bucket '{MINIO_BUCKET_NAME}' already exists.")
    except Exception:
        print(f"Creating bucket '{MINIO_BUCKET_NAME}'...")
        client.create_bucket(Bucket=MINIO_BUCKET_NAME)

if __name__ == "__main__":
    setup_minio_bucket()