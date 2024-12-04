import boto3
from botocore.exceptions import ClientError
from settings.config import MinioSettings

class MinioService:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=f"http{'s' if MinioSettings.MINIO_SECURE else ''}://{MinioSettings.MINIO_ENDPOINT}",
            aws_access_key_id=MinioSettings.MINIO_ACCESS_KEY,
            aws_secret_access_key=MinioSettings.MINIO_SECRET_KEY,
        )
        self.bucket_name = MinioSettings.MINIO_BUCKET_NAME

    def create_bucket(self):
        try:
            self.client.create_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            print(f"Bucket creation failed: {e}")

    def upload_file(self, file_obj, filename):
        try:
            self.client.upload_fileobj(
                file_obj,
                self.bucket_name,
                filename,
                ExtraArgs={'ACL': 'public-read'}
            )
            return f"http{'s' if MinioSettings.MINIO_SECURE else ''}://{MinioSettings.MINIO_ENDPOINT}/{self.bucket_name}/{filename}"
        except ClientError as e:
            print(f"File upload failed: {e}")
            return None
