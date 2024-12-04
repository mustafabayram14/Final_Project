from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_profile_picture_api(minio_client):
    """Test the API endpoint for uploading a profile picture."""
    response = client.post(
        "/upload-profile-picture/",
        files={"file": ("test.jpg", b"This is a test image", "image/jpeg")},
    )
    assert response.status_code == 200
    assert "profile_picture_url" in response.json()
