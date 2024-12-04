from app.services.user_service import upload_profile_picture

def test_upload_profile_picture(minio_client):
    """Test uploading a profile picture."""
    file_name = "profile.jpg"
    file_content = b"This is a profile picture"
    bucket_name = "profile-pictures"

    # Ensure bucket exists
    minio_client.create_bucket(Bucket=bucket_name)

    # Upload the profile picture
    file_url = upload_profile_picture(minio_client, bucket_name, file_name, file_content)

    # Verify the file URL
    assert file_url.endswith(file_name)
