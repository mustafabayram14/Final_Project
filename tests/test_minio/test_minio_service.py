import boto3
import pytest
from moto import mock_s3

@pytest.fixture
def minio_client():
    """Fixture to create a mock Minio (S3) client."""
    with mock_s3():
        client = boto3.client(
            's3',
            endpoint_url='http://localhost:9000',
            aws_access_key_id='your_access_key',
            aws_secret_access_key='your_secret_key',
        )
        yield client

def test_bucket_creation(minio_client):
    """Test that a bucket can be created in Minio."""
    bucket_name = "test-bucket"
    minio_client.create_bucket(Bucket=bucket_name)
    response = minio_client.list_buckets()
    bucket_names = [bucket["Name"] for bucket in response["Buckets"]]
    assert bucket_name in bucket_names

def test_file_upload(minio_client):
    """Test that a file can be uploaded to Minio."""
    bucket_name = "test-bucket"
    minio_client.create_bucket(Bucket=bucket_name)

    file_name = "test.txt"
    file_content = b"This is a test file"
    minio_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

    # Verify the file exists
    response = minio_client.list_objects(Bucket=bucket_name)
    file_names = [obj["Key"] for obj in response["Contents"]]
    assert file_name in file_names
