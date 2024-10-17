from http.client import HTTPException
from fastapi import Body, FastAPI, HTTPException
from fastapi.params import Body
import pymysql

from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

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
    
class InviteInfo(BaseModel):
    email: str
    url: Optional[str] = None
    time_stamp: Optional[str] = None
    status: Optional[str] = None
    last_modified_by : str = None


# create invite_info
@app.post("/invite_info/create")
async def create_invite_info(invite_info: InviteInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = "CALL spCreateInviteInfo(%s,%s, %s, %s, %s);"
            cursor.execute(sql, (invite_info.email, invite_info.url, invite_info.time_stamp, invite_info.status,invite_info.last_modified_by))
            connection.commit()

            return {"message": "InviteInfo created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        raise HTTPException(status_code=500, detail={"message": "InviteInfo creation Failed!!!"})
    finally:
        if connection:
            connection.close()

# get invite_info get
@app.get("/invite_info/get/{email}")
async def get_invite_info(email: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetInviteInfo(%s);"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail=f"Invite Info with email {email} not found")
    except pymysql.MySQLError as err:
        print(f"Error fetching invite_info: {err}")
        raise HTTPException(status_code=500, detail={"error": "Invite Info get call failed (DB Error)"})
    finally:
        if connection:
            connection.close()

# get all invite 
@app.get("/invite_info/getall")
async def get_all_invite_info():
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllInviteInfo();"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as err:
        print(f"Error fetching invite_info: {err}")
        raise HTTPException(status_code=500, detail={"error": "Invite Info get_all call failed (DB Error)"})
    finally:
        if connection:
            connection.close()


# update invite 
@app.put("/invite_info/update/{email}")
async def update_invite_info(email: str, invite_info: InviteInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateInviteInfo(%s,%s, %s, %s, %s);"
            cursor.execute(sql, (email, invite_info.url, invite_info.time_stamp, invite_info.status,invite_info.last_modified_by))
            connection.commit()

            return {"message": f"Invite Info with email {email} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating invite_info: {err}")
        raise HTTPException(status_code=500, detail={"error": f"Invite Info with email {email} update call failed (DB Error)"})
    finally:
        if connection:
            connection.close()

# delete invite 
@app.put("/invite_info/delete/{email}")
async def delete_invite_info(email: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spDeleteInviteInfo(%s);"
            cursor.execute(sql, (email,))
            connection.commit()

            return {"message": f"Invite Info with email {email} deleted successfully"}
    except pymysql.MySQLError as err:
        print(f"Error deleting invite_info: {err}")
        raise HTTPException(status_code=500, detail={"error": f"Invite Info with email {email} delete call failed (DB Error)"})
    finally:
        if connection:
            connection.close()
