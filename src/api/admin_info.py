from http.client import HTTPException
from fastapi import Body, FastAPI, HTTPException, Path
from fastapi.params import Body
import pymysql

from pydantic import BaseModel
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials = True, allow_methods=["*"], allow_headers=["*"]
)

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
        print(f"Error connecting to database: {e}")
        return None

@app.get("/test")
def get_test():
    return {"response": "Test get call successfully called"}

class AdminInfo(BaseModel):
    email_id: str
    password: Optional[str] = None
    designation: Optional[str] = None
    apporved_by: Optional[str] = None
    is_active: Optional[bool] = None
    last_modified_by: Optional[str] = None 

# create the admin_info
@app.post("/admin_info/create")
async def create_admin_info(admin_info: AdminInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = """
            CALL `spCreateAdminInfo`(
                %s, %s, %s, %s, %s
            );
            """
            cursor.execute(sql, (
                admin_info.email_id,
                admin_info.password,
                admin_info.designation,
                admin_info.apporved_by,  
                admin_info.last_modified_by
            ))

            connection.commit()

            return {"message": "AdminInfo created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        raise HTTPException(status_code=500, detail="AdminInfo creation failed")
    finally:
        if connection:
            connection.close()

# get admin by email 
@app.get("/admin_info/get/{email_id}")
async def get_admin_info(email_id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAdminInfo(%s);"
            cursor.execute(sql, (email_id,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail=f"Admin Info with email_id {email_id} not found")
    except pymysql.MySQLError as err:
        print(f"Error fetching signup_info: {err}")
        raise HTTPException(status_code=500, detail={"error": "Admin Info get call failed (DB Error)"})
    finally:
        if connection:
            connection.close()


# get all admin
@app.get("/admin_info/getall")
async def get_all_admin_info():
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllAdminInfo();"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as err:
        print(f"Error fetching signup_info: {err}")
        raise HTTPException(status_code=500, detail={"error": "Admin Info get_all call failed (DB Error)"})
    finally:
        if connection:
            connection.close()

# update admin info
@app.put("/admin_info/update/{email_id}")
async def update_admin_info(email_id: str, admin_info: AdminInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = """
            CALL spUpdateAdminInfo(
                %s, %s, %s, %s, %s
            );
            """
            cursor.execute(sql, (
                email_id,
                admin_info.password,
                admin_info.designation,
                admin_info.apporved_by,
                admin_info.last_modified_by  
            ))
            connection.commit()

            return {"message": f"Admin Info with email_id {email_id} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating admin_info: {err}")
        raise HTTPException(status_code=500, detail=f"Admin Info with email_id {email_id} update failed")
    finally:
        if connection:
            connection.close()
            
# delete admin info
@app.put("/admin_info/delete/{email_id}")
async def delete_admin_info(email_id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spDeleteAdminInfo(%s);"
            cursor.execute(sql, (email_id,))
            connection.commit()

            return {"message": f"SignUpInfo with email_id {email_id} deleted successfully (soft delete)"}
    except pymysql.MySQLError as err:
        print(f"Error deleting signup_info: {err}")
        raise HTTPException(status_code=500, detail={"error": f"Admin Info with email_id {email_id} delete call failed (DB Error)"})
    finally:
        if connection:
            connection.close()


    