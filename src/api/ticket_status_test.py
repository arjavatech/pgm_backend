import pytest
from fastapi.testclient import TestClient
from ticket_status import app, connect_to_database  # Replace with your actual module name

client = TestClient(app)

# Mock the database connection for testing purposes
def mock_connect_to_database():
    return None

# Override the original DB connection with the mock for testing
app.dependency_overrides[connect_to_database] = mock_connect_to_database

# Sample TicketStatus data for testing
new_ticket_status = {
        "company_id": "C002",
        "employee_id": "E002",
        "ticket_id": 1002,
        "work_started_time": "2024-10-11T09:00:00",
        "work_ended_time": "2024-10-11T11:00:00",
        "photos": "https://example.com/photo2.jpg",
        "service_status": "pending",
        "rejected_reason": "Client request",
        "last_modified_by": "manager"
}

# Test creating a new ticket status
def test_create_ticket_status():
    response = client.post("/ticket_status/create", json=new_ticket_status)
    assert response.status_code == 200
    assert response.json() == {"message": "Ticket status created successfully"}

# Test getting a ticket status by token
def test_get_ticket_status_by_id():
    ticket_token = "test-token"  # Replace with a valid token
    response = client.get(f"/ticket_status/get/{ticket_token}")
    if response.status_code == 200:
        assert "ticket_id" in response.json()
    else:
        assert response.status_code == 404

# Test getting all active ticket statuses
def test_get_all_active_ticket_statuses():
    response = client.get("/ticket_status/getall")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list of ticket statuses

# Test updating an existing ticket status
def test_update_ticket_status():
    updated_status = {
        "company_id": "C002",
        "employee_id": "E002",
        "ticket_id": 1002,
        "work_started_time": "2024-10-11T09:00:00",
        "work_ended_time": "2024-10-11T11:00:00",
        "photos": "https://example.com/photo2.jpg",
        "service_status": "pending",
        "rejected_reason": "Client request",
        "last_modified_by": "manager"
    }
    ticket_token = "test-token"  # Replace with a valid token
    response = client.put(f"/ticket_status/update/{ticket_token}", json=updated_status)
    assert response.status_code == 200
    assert response.json() == {"message": f"Ticket status with ID {ticket_token} updated successfully"}

# Test deleting a ticket status (soft delete)
def test_delete_ticket_status():
    ticket_token = "test-token"  # Replace with a valid token
    response = client.put(f"/ticket_status/delete/{ticket_token}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Ticket status with ID {ticket_token} deleted (soft delete) successfully"}
