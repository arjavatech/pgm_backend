# test_sign_up.py
import pytest
from fastapi.testclient import TestClient
from SignUp import app, connect_to_database  # Replace 'sign_up' with the actual module name where your app is defined

client = TestClient(app)

# Mock the database connection for testing
def mock_connect_to_database():
    return None

app.dependency_overrides[connect_to_database] = mock_connect_to_database

# Test creating a sign up
def test_create_sign_up():
    new_sign_up = {
        "company_id": "C001",
        "id": "U002",
        "login_type": "user",
        "password": "passwod123",
        "approved_by": "admin",
        "signup_url": "http://example.com/signup",
        "is_employee": True,
        "last_modified_by": "admin"
    }
    response = client.post("/sign_up/create", json=new_sign_up)
    assert response.status_code == 200
    assert response.json() == {"message": "SignUp created successfully"}

# Test getting a sign up by ID
def test_get_sign_up_by_id():
    sign_up_id = "U002"  # Use the ID of the sign-up you created above
    response = client.get(f"/sign_up/get/{sign_up_id}")
    assert response.status_code == 200

# Test getting all sign ups
def test_get_all_sign_ups():
    response = client.get("/sign_up/getall")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of sign-ups

# Test updating a sign up
def test_update_sign_up():
    updated_info = {
        "company_id": "C001",  # Add the required field
        "id": "U001",          # Add the required field
        "login_type": "admin",
        "password": "newpassword123",
        "approved_by": "admin",
        "signup_url": "http://example.com/signup",
        "is_employee": False,
        "last_modified_by": "admin"
    }
    sign_up_id = "U001"
    response = client.put(f"/sign_up/update/{sign_up_id}", json=updated_info)

    assert response.status_code == 200
    assert response.json() == {"message": f"SignUp with ID {sign_up_id} updated successfully"}

# Test deleting a sign up
def test_delete_sign_up():
    sign_up_id = "U001"  # Use the ID of the sign-up you created above
    response = client.put(f"/sign_up/delete/{sign_up_id}")
    assert response.status_code == 200
    # assert response.json() == {"message": f"SignUp with ID {sign_up_id} deactivated successfully"}