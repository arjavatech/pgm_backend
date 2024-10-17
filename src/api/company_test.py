# test_company_info.py
import pytest
from fastapi.testclient import TestClient
from company import app, connect_to_database

client = TestClient(app)

# Mock the database connection for testing
def mock_connect_to_database():
    return None
app.dependency_overrides[connect_to_database] = mock_connect_to_database

def test_create_company():
    company_info = {
        "company_name": "Test Company7",
        "logo": "test_logo.png",
        "phone_number": "1234567899",
        "email": "testcompany7@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "street": "123 Test St",
        "city": "Test City",
        "zip": "12345",
        "state": "Test State",
        "last_modified_by": "admin"
    }
    response = client.post("/company/create", json=company_info)
    assert response.status_code == 200
    assert response.json() == {"message": "Company created successfully"}

def test_get_company():
    company_id = "C007"  
    response = client.get(f"/company/get/{company_id}")
    assert response.status_code == 200
    assert response.json()["company_name"] == "Tech Innovations Inc."

def test_get_all_active_companies():
    response = client.get("/company/getall")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_company():
    updated_info = {
        "company_name": "Updated Company",
        "logo": "updated_logo.png",
        "phone_number": "0997654321",
        "email": "updatedcompany1@example.com",
        "first_name": "Jane",
        "last_name": "De",
        "street": "456 Updated St",
        "city": "Updated City",
        "zip": "54321",
        "state": "Updated State",
        "last_modified_by": "admin"
    }
    company_id = "C001"  # Replace with a valid company ID
    response = client.put(f"/company/update/{company_id}", json=updated_info)
    assert response.status_code == 200
    assert response.json() == {"message": f"Company with ID {company_id} updated successfully"}

def test_delete_company():
    company_id = "C001"  # Replace with a valid company ID
    response = client.put(f"/company/delete/{company_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Company with ID {company_id} deleted (soft delete) successfully"}
