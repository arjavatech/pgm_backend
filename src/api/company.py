from fastapi import Body, FastAPI, HTTPException
import pymysql
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import uuid  # Use UUID here

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
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

class Company(BaseModel):
    company_name: str
    logo: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    state: Optional[str] = None
    last_modified_by : str = None


# create the company
@app.post("/company/create")
async def create_company(company: Company = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    company_id = str(uuid.uuid4())  # Generate UUID for company_id
    # last_modified_by = "creator_name"  # Replace with the actual user performing the operation

    try:
        with connection.cursor() as cursor:
            sql = """
            CALL spCreateCompany(
               %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
            """
            cursor.execute(sql, (
                company_id,
                company.company_name,
                company.logo,
                company.phone_number,
                company.email,
                company.first_name,
                company.last_name,
                company.street,
                company.city,
                company.zip,
                company.state,
                company.last_modified_by
            ))
            connection.commit()

            return {"message": "Company created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error creating company: {err}")
        raise HTTPException(status_code=500, detail="Company creation failed")
    finally:
        if connection:
            connection.close()

# get the company by company id
@app.get("/company/get/{company_id}")
async def get_company_by_id(company_id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetCompanyById(%s);"
            cursor.execute(sql, (company_id,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail=f"Company with ID {company_id} not found")
    except pymysql.MySQLError as err:
        print(f"Error fetching company: {err}")
        raise HTTPException(status_code=500, detail="Get company by ID failed (DB Error)")
    finally:
        if connection:
            connection.close()

# get all company
@app.get("/company/getall")
async def get_all_active_companies():
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllActiveCompanies();"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as err:
        print(f"Error fetching all companies: {err}")
        raise HTTPException(status_code=500, detail="Get all companies failed (DB Error)")
    finally:
        if connection:
            connection.close()


# update company
@app.put("/company/update/{company_id}")
async def update_company(company_id: str, company: Company = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = """
            CALL spUpdateCompany(
                %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
            """
            cursor.execute(sql, (
                company_id,
                company.company_name,
                company.logo,
                company.phone_number,
                company.email,
                company.first_name,
                company.last_name,
                company.street,
                company.city,
                company.zip,
                company.state,
                company.last_modified_by
            ))
            connection.commit()

            return {"message": f"Company with ID {company_id} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating company: {err}")
        raise HTTPException(status_code=500, detail="Update company failed")
    finally:
        if connection:
            connection.close()

# delete company
@app.put("/company/delete/{company_id}")
async def delete_company(company_id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spDeleteCompany(%s);"
            cursor.execute(sql, (company_id,))
            connection.commit()

            return {"message": f"Company with ID {company_id} deleted (soft delete) successfully"}
    except pymysql.MySQLError as err:
        print(f"Error deleting company: {err}")
        raise HTTPException(status_code=500, detail="Delete company failed (DB Error)")
    finally:
        if connection:
            connection.close()
