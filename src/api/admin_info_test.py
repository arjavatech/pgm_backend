# test_admin_info
import pytest
from fastapi.testclient import TestClient
from admin_info import app, connect_to_database

client = TestClient(app)
def mock_connect_to_database():
    return None  
app.dependency_overrides[connect_to_database] = mock_connect_to_database

def test_get_test():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"response": "Test get call successfully called"}

def test_create_admin_info():
    admin_info = {
        "email_id": "test5@example.com",
        "password": "password111",
        "designation": "Admin",
        "apporved_by": "Admin1",
        "last_modified_by": "Admin1"
    }
    response = client.post("/admin_info/create", json=admin_info)
    assert response.status_code == 200
    assert response.json() == {"message": "AdminInfo created successfully"}

def test_get_admin_info():
    response = client.get("/admin_info/get/test2@example.com")
    assert response.status_code == 200
    assert response.json()["email_id"] == "test2@example.com"

def test_update_admin_info():
    updated_info = {
        "email_id": "test5@example.com",
        "password": "newpassword125",
        "designation": "Updated Admin",
        "apporved_by": "Admin1",
        "last_modified_by": "Admin2"
    }
    response = client.put("/admin_info/update/test@example.com", json=updated_info)
    assert response.status_code == 200
    assert response.json() == {"message": "Admin Info with email_id test@example.com updated successfully"}

def test_delete_admin_info():
    response = client.put("/admin_info/delete/test@example.com")
    assert response.status_code == 200
    assert response.json() == {"message": "SignUpInfo with email_id test@example.com deleted successfully (soft delete)"}




