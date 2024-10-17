# test_employee_info.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import true
from employee import app, connect_to_database  # Replace 'your_module' with the actual module name

client = TestClient(app)

# Mock the database connection for testing
def mock_connect_to_database():
    return None

app.dependency_overrides[connect_to_database] = mock_connect_to_database

# Test creating an employee
def test_create_employee():
    updated_info = {
        "employee_id": "E008",
        "company_id": "C001",
        "first_name": "Jon",
        "last_name": "Dooe",
        "phone_number": "53678920176",
        "email": "john8.doe@example.com",
        "invite_url": "http://example.com/invite",
        "specialization": "Engineer",
        "areas_covered": "Are1",
        "assigned_locations": "Location 1",
        "employee_status": "Active",
        "employee_no_of_completed_work": 5,
        "no_of_pending_works": 2,
        "street": "123 Main St",
        "city": "Sample City",
        "zip": "12345",
        "skills": "Python, FastAPI",
        "qualification": "BSc Computer Science",
        "experience": 3,
        "available": True,
        "photo": None,  # Set to None instead of a string "None"
        "last_modified_by": "admin"
    }
    employee_id = "E008"
    response = client.put(f"/employee/update/{employee_id}", json=updated_info)
    assert response.status_code == 200
    assert response.json() == {"message": f"Employee with ID {employee_id} updated successfully"}


# Test getting an employee by ID
def test_get_employee():
    employee_id = "E005"  # Use the ID of the employee you created above
    response = client.get(f"/employee/get/{employee_id}")
    assert response.status_code == 200
    # assert response.json()["first_name"] == "John"
    # assert response.json()["last_name"] == "Doe"

# Test getting all employees
def test_get_all_employees():
    response = client.get("/employee/getall")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of employees

# Test updating an employee
def test_update_employee():
    updated_info = {
        "company_id": "C001",
        "first_name": "Jon",
        "last_name": "Dooe",
        "phone_number": "53678920176",
        "email": "john8.doe@example.com",
        "invite_url": "http://example.com/invite",
        "specialization": "Engineer",
        "areas_covered": "Are1",
        "assigned_locations": "Location 1",
        "employee_status": "Active",
        "employee_no_of_completed_work": 5,
        "no_of_pending_works": 2,
        "street": "123 Main St",
        "city": "Sample City",
        "zip": "12345",
        "skills": "Python, FastAPI",
        "qualification": "BSc Computer Science",
        "experience": 3,
        "available": True,
        "photo": "None",  
        "last_modified_by": "admin"
    }
    employee_id = "E008"
    response = client.put(f"/employee/update/{employee_id}", json=updated_info)

    print(response.status_code)
    print(response.json())  # Print response details

    assert response.status_code == 200
    assert response.json() == {"message": f"Employee with ID {employee_id} updated successfully"}
    
    
def test_delete_employee():
    employee_id = "E004"  # Use the ID of the employee you created above
    response = client.delete(f"/employee/delete/{employee_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Employee with ID {employee_id} deleted successfully"}