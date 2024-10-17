from http.client import HTTPException
from fastapi import  Body, FastAPI, HTTPException, Path
from fastapi.params import Body
import pymysql
from pydantic import BaseModel

from datetime import datetime
import shortuuid



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=[""], allow_credentials = True, allow_methods=[""], allow_headers=["*"]
)

def connect_to_database():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="Sandy@2025",  
            database="pgm",
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as err:
        return None

@app.get("/test")
def get_test():
    return {"response": "Test get call successfully called"}

class TicketStatus(BaseModel):
    company_id: str
    employee_id: str
    ticket_id: int
    work_started_time:datetime = None
    work_ended_time: datetime = None
    photos: str= None
    service_status: str= None 
    rejected_reason: str= None
    last_modified_by : str =None

# create tiket status
@app.post("/ticket_status/create")
async def create_ticket_status(ticket_status: TicketStatus = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            ticket_token = shortuuid.uuid()

            sql = "CALL spCreateTicketStatus(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                ticket_token,
                ticket_status.company_id,
                ticket_status.employee_id,
                ticket_status.ticket_id,
                ticket_status.work_started_time,
                ticket_status.work_ended_time,
                ticket_status.photos,
                ticket_status.service_status,
                ticket_status.rejected_reason,
                ticket_status.last_modified_by
            ))
            connection.commit()

            return {"message": "Ticket status created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error creating ticket status: {err}")
        raise HTTPException(status_code=500, detail="Ticket status creation failed (DB Error)")
    finally:
        if connection:
            connection.close()

# get ticket status by ticket_token
@app.get("/ticket_status/get/{ticket_token}")
async def get_ticket_status_by_id(ticket_token: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetTicketStatusById(%s);"
            cursor.execute(sql, (ticket_token,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail=f"Ticket status with ID {ticket_token} not found")
    except pymysql.MySQLError as err:
        print(f"Error fetching ticket status: {err}")
        raise HTTPException(status_code=500, detail="Get ticket status by ID failed (DB Error)")
    finally:
        if connection:
            connection.close()

# getall ticket status
@app.get("/ticket_status/getall")
async def get_all_active_ticket_statuses():
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllActiveTicketStatuses();"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as err:
        print(f"Error fetching all ticket statuses: {err}")
        raise HTTPException(status_code=500, detail="Get all ticket statuses failed (DB Error)")
    finally:
        if connection:
            connection.close()

# update ticket_status
@app.put("/ticket_status/update/{ticket_token}")
async def update_ticket_status(ticket_token: str, ticket_status: TicketStatus = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateTicketStatus(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                ticket_token,
                ticket_status.company_id,
                ticket_status.employee_id,
                ticket_status.ticket_id,
                ticket_status.work_started_time,
                ticket_status.work_ended_time,
                ticket_status.photos,
                ticket_status.service_status,
                ticket_status.rejected_reason,
                ticket_status.last_modified_by
            ))
            connection.commit()

            return {"message": f"Ticket status with ID {ticket_token} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating ticket status: {err}")
        raise HTTPException(status_code=500, detail="Update ticket status failed (DB Error)")
    finally:
        if connection:
            connection.close()

# delete ticket_status
@app.put("/ticket_status/delete/{ticket_token}")
async def delete_ticket_status(ticket_token: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spDeleteTicketStatus(%s);"
            cursor.execute(sql, (ticket_token,))
            connection.commit()

            return {"message": f"Ticket status with ID {ticket_token} deleted (soft delete) successfully"}
    except pymysql.MySQLError as err:
        print(f"Error deleting ticket status: {err}")
        raise HTTPException(status_code=500, detail="Delete ticket status failed (DB Error)")
    finally:
        if connection:
            connection.close()
