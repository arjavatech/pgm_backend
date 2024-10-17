import pytest
from fastapi.testclient import TestClient
from ticket_info import app, connect_to_database  # Replace 'your_module_name' with the actual module name where your app is defined

client = TestClient(app)

# Mock the database connection for testing
def mock_connect_to_database():
    return None

app.dependency_overrides[connect_to_database] = mock_connect_to_database

# Test creating a ticket
def test_create_ticket():
    new_ticket = {
        "company_id": "C001",
        "ticket_type": "Bug",
        "name": "suryarish",
        "phone_number": "12322267890",
        "images": "http://example.com/image.jpg",
        "status": 1,
        "complain_raised_date": "2024-10-10",
        "description": "Sample bug description",
        "available_slots": "10:00 AM - 12:00 PM",
        "rejected_reason": "None",
        "rejected_date": "2024-10-10",
        "street": "123 Main St",
        "city": "Metropolis",
        "zip": 12345,
        "state": "NY",
        "is_active": True,
        "last_modified_by": "admin"
    }
    response = client.post("/ticketinfo/create", json=new_ticket)
    assert response.status_code == 200
    assert response.json() == {"message": "Ticket info record added successfully"}

# Test getting a ticket by ID
def test_get_ticket_by_id():
    ticket_id = 1  # Replace with a valid ticket ID created earlier
    response = client.get(f"/ticketinfo/get/{ticket_id}")
    assert response.status_code == 200
    assert "name" in response.json()  # Check if the response contains ticket information

# Test getting all tickets
def test_get_all_tickets():
    response = client.get("/ticketinfo/getall")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of tickets

# Test updating a ticket
def test_update_ticket():
    updated_ticket_info = {
        "company_id": "C001",
        "ticket_type": "Feature Request",
        "name": "arish",
        "phone_number": "1234333890",
        "images": "http://example.com/new_image.jpg",
        "status": 2,
        "complain_raised_date": "2024-10-10",
        "description": "Updated feature request description",
        "available_slots": "1:00 PM - 3:00 PM",
        "rejected_reason": "None",
        "rejected_date": "2024-10-10",
        "street": "123 Main St",
        "city": "Metropolis",
        "zip": 12345,
        "state": "NY",
        "is_active": True,
        "last_modified_by": "admin"
    }
    ticket_id = 1  # Replace with a valid ticket ID to update
    response = client.put(f"/ticketinfo/update/{ticket_id}", json=updated_ticket_info)

    assert response.status_code == 200
    assert response.json() == {"message": "Ticket Info updated successfully"}

# Test deleting a ticket
def test_delete_ticket():
    ticket_id = 1  # Replace with a valid ticket ID to delete
    response = client.delete(f"/ticketinfo/delete/{ticket_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Ticket info deleted successfully"}
