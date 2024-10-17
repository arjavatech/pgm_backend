from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql

app = FastAPI()

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

class TicketInfo(BaseModel):
    company_id: str = None 
    ticket_type: str = None 
    name: str = None 
    phone_number: str = None 
    images: str = None 
    status: int = None 
    complain_raised_date : date = None 
    description: str = None 
    available_slots: str = None 
    rejected_reason: str = None 
    rejected_date: date = None 
    street: str = None 
    city: str = None 
    zip: int = None 
    state: str = None 
    is_active :bool
    last_modified_by: str =None

#Create Ticket
@app.post("/ticketinfo/create")
def create_ticket_info(ticketinfo: TicketInfo):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            sql = """CALL spCreateTicketInfo(
                %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s
            )"""  
            cursor.execute(sql, (
                ticketinfo.company_id, ticketinfo.ticket_type, ticketinfo.name, 
                ticketinfo.phone_number, ticketinfo.images, ticketinfo.status, 
                ticketinfo.complain_raised_date, ticketinfo.description, 
                ticketinfo.available_slots, ticketinfo.rejected_reason, 
                ticketinfo.rejected_date, ticketinfo.street, ticketinfo.city, 
                ticketinfo.zip, ticketinfo.state, ticketinfo.is_active,ticketinfo.last_modified_by
            ))
            connection.commit()
            return {"message": "Ticket info record added successfully"}
    except pymysql.MySQLError as err:
        raise HTTPException(status_code=500, detail=f"Error calling stored procedure: {err}")
    finally:
        connection.close()


#Get All Signup
@app.get("/ticketinfo/getall")
def get_all_ticketinfo():
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect with database"}
    
    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllTicketInfo()"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

#Get Signup by Id
@app.get("/ticketinfo/get/{id}")
def get_ticketinfo_by_id(id: int):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect with database"}
    
    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetTicketInfoById(%s)"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail="Signup not found")
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

#Update Signup
@app.put("/ticketinfo/update/{id}")
def update_signup(id: int, ticketinfo: TicketInfo):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}
    
    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateTicketInfo(%s,%s,%s,%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (
                id, ticketinfo.company_id,ticketinfo.ticket_type, ticketinfo.name, ticketinfo.phone_number, ticketinfo.images, ticketinfo.status,
                ticketinfo.complain_raised_date, ticketinfo.description, ticketinfo.available_slots, ticketinfo.rejected_reason, 
                ticketinfo.rejected_date, ticketinfo.street, ticketinfo.city, ticketinfo.zip, ticketinfo.state,ticketinfo.is_active ,ticketinfo.last_modified_by              
            ))
            connection.commit()
            return {"message": "Ticket Info updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()

#Delete Signup by id
@app.delete("/ticketinfo/delete/{id}")
def delete_ticketinfo_by_id(id: int):
    connection = connect_to_database()
    if not connection:
        return{"error": "Failed to connect with database"}
    
    try:
        with connection.cursor() as cursor:
            sql = "CALL spDeleteTicketInfo(%s)"
            cursor.execute(sql, (id))
            connection.commit()
            return {"message": "Ticket info deleted successfully"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        return {"error": str(err)}
    finally:
        connection.close()
        
        
