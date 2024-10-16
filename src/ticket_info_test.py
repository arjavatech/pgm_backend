from fastapi.testclient import TestClient
from ticket_info import app  # Ensure you have the correct module name and import

client = TestClient(app)


# Test the /test endpoint (if you have one, otherwise remove this test)
def test_get_test():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"response": "Test get call successfully called"}

# Test creating a ticket
def test_create_ticketinfo():
    ticket_info = {
       "company_id": "63567ab5-9108-4781-a9de-16eca798c767",
        "ticket_type": "updated",
        "name": "Smith",
        "phone_number": "12345",
        "images": "image2.png",
        "status": 2,
        "complain_raised_date": "2024-10-20",
        "description": "upgrade",
        "available_slots": "1:00 PM",
        "rejected_reason": "Not enough",
        "rejected_date": "2024-10-11",
        "street": "987 Another St",
        "city": "Elsewhere",
        "zip": 23145,
        "state": "OtherState",
    }
    response = client.post("/ticketinfo/create", json=ticket_info)
    assert response.status_code == 200
    assert response.json() == {"message": "Ticket info record added successfully"}

# Test getting all tickets
def test_get_all_ticketinfo():
    response = client.get("/ticketinfo/getall")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test getting a ticket by ID
def test_get_ticketinfo_by_id():
    ticket_id = 7  # Adjust the ID based on actual test data in your DB
    response = client.get(f"/ticketinfo/get/{ticket_id}")
    assert response.status_code == 200
    assert response.json() == {"id": ticket_id, "message": "Ticket info retrieved successfully"}

# Test updating a ticket
def test_update_ticketinfo():
    updated_ticket_info = {
        "company_id":"63567ab5-9108-4781-a9de-16eca798c767",
        "ticket_type": "updated ",
        "name": "Smith",
        "phone_number": "12345",
        "images": "image2.png",
        "status": 2,
        "complain_raised_date": "2024-10-20",
        "description": "upgrfde",
        "available_slots": "1:00 PM",
        "rejected_reason": "Not enough",
        "rejected_date": "2024-10-11",
        "street": "987 Another St",
        "city": "Elsewhere",
        "zip": 23145,
        "state": "OtherState"
    }
    ticket_id = 7  # Ensure this ID exists in your test data
    response = client.put(f"/ticketinfo/update/{ticket_id}", json=updated_ticket_info)
    assert response.status_code == 200
    assert response.json() == {"message": "Ticket Info updated successfully"}

# Test deleting a ticket
def test_delete_ticketinfo_by_id():
    ticket_id = 7  # Ensure this ID exists in your test data
    response = client.delete(f"/ticketinfo/delete/{ticket_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Ticket info deleted successfully"}
