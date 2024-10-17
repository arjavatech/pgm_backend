
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel
import pymysql

app = FastAPI()

# Database connection
def connect_to_database():
    try:
        return pymysql.connect(
            host="localhost",
            user="root",
            password="Sandy@2025",
            database="pgm",
            cursorclass=pymysql.cursors.DictCursor

        )
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to database: {e}")

@app.get("/test")
def get_test():
    return {"response": "Test get call successfully called"}



# to get active employee
@app.get("/completedTickets/getall")
def get_all_ticketinfo():
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect with database"}
    
    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetTicketStatusAndInfoByToken()"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()
        
        
class TicketUpdateRequest(BaseModel):
    company_id: str
    ticket_id: int
    employee_id: str

# Update Ticket Status and Ticket Info in a single API
@app.put("/ticket/updateStatus")
async def update_ticket_and_status(ticket_update: TicketUpdateRequest = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateTicketAndStatus(%s, %s, %s)"
            cursor.execute(sql, (ticket_update.company_id, ticket_update.ticket_id, ticket_update.employee_id))
            connection.commit()

            return {"message": "Ticket status and info updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error executing stored procedure: {err}")
        raise HTTPException(status_code=500, detail="Update failed")
    finally:
        if connection:
            connection.close()

# Endpoint to update ticket and employee status via path parameters
@app.put("/update-status/{company_id}/{ticket_id}/{employee_id}")
async def update_status(company_id: str, ticket_id: int, employee_id: str):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.callproc('spUpdateTicketAndEmployeeStatus', [company_id, ticket_id, employee_id])
            connection.commit() 
        return {"message": "Status updated successfully"}
    except Exception as e:
        connection.rollback() 
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        connection.close()


# to get info for ready to invoice
@app.get("/tickets")
async def get_ticket_details():
    try:
        # Connect to the database
        connection = connect_to_database()
        with connection.cursor() as cursor:
            # Call the stored procedure
            cursor.execute("CALL GetTicketDetails()")
            result = cursor.fetchall()

        connection.close()
        return {"tickets": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# for rejected tickets //completed tickets

@app.put("/reject-ticket/{ticket_id}/{company_id}/{employee_id}")
async def reject_ticket(ticket_id: int, company_id: str, employee_id: str):
    try:
        connection = connect_to_database()
        with connection.cursor() as cursor:
          reject_ticket_query = "CALL RejectTicket(%s, %s, %s)"
          cursor.execute(reject_ticket_query, (ticket_id, company_id, employee_id))
          connection.commit()
        return {"message": "Ticket rejected successfully"}

    except pymysql.MySQLError as e:
        connect_to_database.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()


# for reassign employee
@app.post("/employee/reassign/{old_employee_id}/{new_employee_id}/{old_ticket_token}/{new_ticket_token}")
async def reassign_employee(
    old_employee_id: str,
    new_employee_id: str,
    old_ticket_token: str,
    new_ticket_token: str
):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}
     
    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateEmployeeOnReassign(%s, %s, %s, %s);"
            cursor.execute(sql, (old_employee_id, new_employee_id, old_ticket_token, new_ticket_token))
            connection.commit()

            return {"message": "Employee reassignment and ticket update successful"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        raise HTTPException(status_code=500, detail="Employee reassignment failed")
    finally:
        if connection:
            connection.close()
