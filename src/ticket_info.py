# from datetime import date
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import pymysql

# app = FastAPI()

# # Database connection
# def connect_to_database():
#     try:
#         connection = pymysql.connect(
#             host="localhost",
#             port=3306,
#             user="root",
#             password="Rolex_Surya07",
#             database="pqm_final",
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         return connection
#     except pymysql.MySQLError as err:
#         return None

# @app.get("/test")
# def get_test():
#     return {"response": "Test get call successfully called"}


# # Pydantic model for signup
# class TicketInfo(BaseModel):
#     company_id: str = None 
#     ticket_type: str = None 
#     name: str = None 
#     phone_number: str = None 
#     images: str = None 
#     status: int = None 
#     complain_raised_date : date = None 
#     description: str = None 
#     available_slots: str = None 
#     rejected_reason: str = None 
#     rejected_date: date = None 
#     street: str = None 
#     city: str = None 
#     zip: int = None 
#     state: str = None 
#     last_modified_by: str =None

# #Create Ticket
# @app.post("/ticketinfo/create")
# def create_ticket_info(ticketinfo: TicketInfo):
#     connection = connect_to_database()
#     try:
#         with connection.cursor() as cursor:
#             # sql = """CALL spCreateTicketInfo(
#             #     %s, %s, %s, %s, %s, %s, %s, %s, %s, 
#             #     %s, %s, %s, %s, %s, %s, %s
#             # )"""  # Removed the trailing comma here
#             # cursor.execute(sql, (
#             #     ticketinfo.company_id, ticketinfo.ticket_type, ticketinfo.name, 
#             #     ticketinfo.phone_number, ticketinfo.images, ticketinfo.status, 
#             #     ticketinfo.complain_raised_date, ticketinfo.description, 
#             #     ticketinfo.available_slots, ticketinfo.rejected_reason, 
#             #     ticketinfo.rejected_date, ticketinfo.street, ticketinfo.city, 
#             #     ticketinfo.zip, ticketinfo.state, ticketinfo.last_modified_by
#             # ))

#             sql = """CALL spCreateTicketInfo(
#             %s, %s, %s, %s, %s, %s, %s, %s, %s, 
#             %s, %s, %s, %s, %s, %s  -- This should match exactly 15 placeholders
#         )"""

# # Ensure that you are passing only 15 arguments here
#             cursor.execute(sql, (
#                 ticketinfo.company_id, ticketinfo.ticket_type, ticketinfo.name, 
#                 ticketinfo.phone_number, ticketinfo.images, ticketinfo.status, 
#                 ticketinfo.complain_raised_date, ticketinfo.description, 
#                 ticketinfo.available_slots, ticketinfo.rejected_reason, 
#                 ticketinfo.rejected_date, ticketinfo.street, ticketinfo.city, 
#                 ticketinfo.zip, ticketinfo.state  # Ensure only 15 fields are passed
#             ))
#             connection.commit()
#             return {"message": "Ticket info record added successfully"}
#     except pymysql.MySQLError as err:
#         raise HTTPException(status_code=500, detail=f"Error calling stored procedure: {err}")
#     finally:
#         connection.close()


# #Get All Signup
# @app.get("/ticketinfo/getall")
# def get_all_ticketinfo():
#     connection = connect_to_database()
#     if not connection:
#         return {"error": "Failed to connect with database"}
    
#     try:
#         with connection.cursor() as cursor:
#             sql = "CALL spGetAllTicketInfo()"
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             return result
#     except pymysql.MySQLError as err:
#         print(f"Error calling stored procedure: {err}")
#         return {"error": str(err)}
#     finally:
#         connection.close()

# #Get Signup by Id
# @app.get("/ticketinfo/get/{id}")
# def get_ticketinfo_by_id(id: int):
#     connection = connect_to_database()
#     if not connection:
#         return {"error": "Failed to connect with database"}
    
#     try:
#         with connection.cursor() as cursor:
#             sql = "CALL spGetTicketInfoById(%s)"
#             cursor.execute(sql, (id,))
#             result = cursor.fetchone()
#             if result:
#                 return result
#             else:
#                 raise HTTPException(status_code=404, detail="Signup not found")
#     except pymysql.MySQLError as err:
#         print(f"Error calling stored procedure: {err}")
#         return {"error": str(err)}
#     finally:
#         connection.close()

# #Update Signup
# @app.put("/ticketinfo/update/{id}")
# def update_signup(id: int, ticketinfo: TicketInfo):
#     connection = connect_to_database()
#     if not connection:
#         return {"error": "Failed to connect to database"}
    
#     try:
#         with connection.cursor() as cursor:
#             sql = "CALL spUpdateTicketInfo(%s,%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#             cursor.execute(sql, (
#                 id, ticketinfo.ticket_type, ticketinfo.name, ticketinfo.phone_number, ticketinfo.images, ticketinfo.status,
#                 ticketinfo.complain_raised_date, ticketinfo.description, ticketinfo.available_slots, ticketinfo.rejected_reason, 
#                 ticketinfo.rejected_date, ticketinfo.street, ticketinfo.city, ticketinfo.zip, ticketinfo.state,ticketinfo.last_modified_by              
#             ))
#             connection.commit()
#             return {"message": "Ticket Info updated successfully"}
#     except pymysql.MySQLError as err:
#         print(f"Error calling stored procedure: {err}")
#         return {"error": str(err)}
#     finally:
#         connection.close()

# #Delete Signup by id
# @app.delete("/ticketinfo/delete/{id}")
# def delete_ticketinfo_by_id(id: int):
#     connection = connect_to_database()
#     if not connection:
#         return{"error": "Failed to connect with database"}
    
#     try:
#         with connection.cursor() as cursor:
#             sql = "CALL spDeleteTicketInfo(%s)"
#             cursor.execute(sql, (id))
#             connection.commit()
#             return {"message": "Ticket info deleted successfully"}
#     except pymysql.MySQLError as err:
#         print(f"Error calling stored procedure: {err}")
#         return {"error": str(err)}
#     finally:
#         connection.close()







from datetime import date
from typing import Optional
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel
import pymysql

app = FastAPI()

# Database connection
def connect_to_database():
    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Rolex_Surya07",
            database="pqm_final",
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as err:
        return None

@app.get("/test")
def get_test():
    return {"response": "Test get call successfully called"}


# Pydantic model for Ticket
class TicketInfo(BaseModel):
    company_id: Optional[str] = None
    ticket_type: Optional[str] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    images: Optional[str] = None
    status: Optional[int] = None
    complain_raised_date: Optional[date] = None
    description: Optional[str] = None
    available_slots: Optional[str] = None
    rejected_reason: Optional[str] = None
    rejected_date: Optional[date] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[int] = None
    
# Create a new Ticket
@app.post("/ticket/create")
async def create_ticket(ticket: TicketInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to the database"}

    try:
        with connection.cursor() as cursor:
            sql = """
                CALL spCreateTicketInfo(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            cursor.execute(sql, (
                ticket.company_id, 
                ticket.ticket_type, 
                ticket.name, 
                ticket.phone_number, 
                ticket.images, 
                ticket.status, 
                ticket.complain_raised_date, 
                ticket.description, 
                ticket.available_slots, 
                ticket.rejected_reason, 
                ticket.rejected_date, 
                ticket.street, 
                ticket.city, 
                ticket.zip, 
                ticket.state
            ))
            connection.commit()

            return {"message": "Ticket created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error creating Ticket: {err}")
        raise HTTPException(status_code=500, detail="Failed to create ticket (DB Error)")
    finally:
        if connection:
            connection.close()

# Retrieve Ticket by ticket_id
@app.get("/ticket/get/{ticket_id}")
async def get_ticket_by_id(ticket_id: int):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetTicketInfoById(%s);"
            cursor.execute(sql, (ticket_id,))
            result = cursor.fetchone()

            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail=f"Ticket with ID {ticket_id} not found")
    except pymysql.MySQLError as err:
        print(f"Error retrieving Ticket: {err}")
        raise HTTPException(status_code=500, detail="Failed to retrieve ticket")
    finally:
        if connection:
            connection.close()

# Retrieve all active Tickets
@app.get("/ticket/getall")
async def get_all_tickets():
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllTicketInfo();"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as err:
        print(f"Error fetching tickets: {err}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tickets")
    finally:
        if connection:
            connection.close()

# Update Ticket by ticket_id
@app.put("/ticket/update/{ticket_id}")
async def update_ticket(ticket_id: int, ticket: TicketInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        with connection.cursor() as cursor:
            sql = """
                CALL spUpdateTicketInfo(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql, (
                ticket_id,
                ticket.company_id,
                ticket.ticket_type,
                ticket.name,
                ticket.phone_number,
                ticket.images,
                ticket.status,
                ticket.complain_raised_date,
                ticket.description,
                ticket.available_slots,
                ticket.rejected_reason,
                ticket.rejected_date,
                ticket.street,
                ticket.city,
                ticket.zip,
                ticket.state
            ))
            connection.commit()

            return {"message": f"Ticket with ID {ticket_id} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating Ticket: {err}")
        raise HTTPException(status_code=500, detail=f"Failed to update ticket with ID {ticket_id}")
    finally:
        if connection:
            connection.close()

# Delete (Soft delete) Ticket by ticket_id
@app.put("/ticket/delete/{ticket_id}")
async def delete_ticket(ticket_id: int):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spDeleteTicketInfo(%s);"
            cursor.execute(sql, (ticket_id,))
            connection.commit()

            return {"message": f"Ticket with ID {ticket_id} deactivated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error deleting Ticket: {err}")
        raise HTTPException(status_code=500, detail=f"Failed to deactivate ticket with ID {ticket_id}")
    finally:
        if connection:
            connection.close()
