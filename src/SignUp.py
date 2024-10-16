from http.client import HTTPException
from fastapi import Body, FastAPI, HTTPException
from fastapi.params import Body
import pymysql

from pydantic import BaseModel
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=[""], allow_credentials = True, allow_methods=[""], allow_headers=["*"]
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


class SignUp(BaseModel):
    company_id: str
    id: str
    login_type: str = None
    password: str= None
    approved_by: str = None
    signup_url: str = None
    is_employee: bool = None
    last_modified_by :str

# Create Sign Up API
@app.post("/sign_up/create")
async def create_sign_up(sign_up: SignUp = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = "CALL spCreateSignUp(%s,%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                sign_up.company_id, 
                sign_up.id, 
                sign_up.login_type, 
                sign_up.password, 
                sign_up.approved_by, 
                sign_up.signup_url, 
                sign_up.is_employee,
                sign_up.last_modified_by
            ))
            connection.commit()

            return {"message": "SignUp created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error creating SignUp: {err}")
        raise HTTPException(status_code=500, detail="SignUp creation failed (DB Error)")
    finally:
        if connection:
            connection.close()

# Get Sign Up by ID API
@app.get("/sign_up/get/{id}")
async def get_sign_up_by_id(id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetSignUpById(%s);"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()

            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail=f"SignUp with ID {id} not found")
    except pymysql.MySQLError as err:
        print(f"Error fetching SignUp: {err}")
        raise HTTPException(status_code=500, detail="Failed to retrieve SignUp")
    finally:
        if connection:
            connection.close()

# Get All Active Sign Ups API
@app.get("/sign_up/getall")
async def get_all_sign_ups():
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL GetAllSignUp();"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as err:
        print(f"Error fetching SignUp: {err}")
        raise HTTPException(status_code=500, detail="Failed to retrieve SignUps")
    finally:
        if connection:
            connection.close()

# Update Sign Up API
@app.put("/sign_up/update/{id}")
async def update_sign_up(id: str, sign_up: SignUp = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateSignUp(%s,%s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                id,
                sign_up.login_type,
                sign_up.password,
                sign_up.approved_by,
                sign_up.signup_url,
                sign_up.is_employee,
                sign_up.last_modified_by
            ))
            connection.commit()

            return {"message": f"SignUp with ID {id} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating SignUp: {err}")
        raise HTTPException(status_code=500, detail=f"Failed to update SignUp with ID {id}")
    finally:
        if connection:
            connection.close()

# Delete Sign Up API
@app.put("/sign_up/delete/{id}")
async def delete_sign_up(id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spDeleteSignUp(%s);"
            cursor.execute(sql, (id,))
            connection.commit()

            return {"message": f"SignUp with ID {id} deactivated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error deleting SignUp: {err}")
        raise HTTPException(status_code=500, detail=f"Failed to deactivate SignUp with ID {id}")
    finally:
        if connection:
            connection.close()