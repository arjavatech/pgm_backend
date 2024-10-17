import pytest
from fastapi.testclient import TestClient
from invite_info import app, connect_to_database  # Adjust the import to your app's module

client = TestClient(app)

# Mocking the database connection for testing
def mock_connect_to_database():
    return None  # Simulate a database connection failure

app.dependency_overrides[connect_to_database] = mock_connect_to_database

def test_create_invite_info():
    invite_info = {
        "email": "tes@example.com",
        "url": "http://example.com",
        "time_stamp": "2024-10-12T12:00:00",
        "status": "pending",
        "last_modified_by": "user123"
    }
    response = client.post("/invite_info/create", json=invite_info)
    assert response.status_code == 200
    assert response.json() == {"message": "InviteInfo created successfully"}

def test_get_invite_info():
    response = client.get("/invite_info/get/tes@example.com")
    assert response.status_code == 200

def test_get_all_invite_info():
    response = client.get("/invite_info/getall")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Check that the response is a list

def test_update_invite_info():
    updated_info = {
        "email": "tes@example.com",
        "url": "http://updated-url.com",
        "time_stamp": "2024-10-12T12:00:00",
        "status": "accepted",
        "last_modified_by": "user456"
    }
    response = client.put("/invite_info/update/tes@example.com", json=updated_info)
    assert response.status_code == 200
    # assert response.json() == {"message": "Invite Info with email test@example.com updated successfully"}

def test_delete_invite_info():
    response = client.put("/invite_info/delete/tes@example.com")
    assert response.status_code == 200
    # assert response.json() == {"message": "Invite Info with email test@example.com deleted successfully"}
