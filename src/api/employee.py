from http.client import HTTPException
from fastapi import  Body, FastAPI, HTTPException
from fastapi.params import Body
import pymysql

from pydantic import BaseModel, constr
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


class Employee(BaseModel):
    company_id: str
    first_name: str
    last_name: str
    phone_number: str
    email: str
    invite_url: str
    specialization: str
    areas_covered: str
    assigned_locations: str
    employee_status: str
    employee_no_of_completed_work: int
    no_of_pending_works: int
    street: str
    city: str
    zip: str
    skills: str
    qualification: str
    experience: int
    available: bool
    photo: Optional[str]  
    last_modified_by: str




# Create Employee
@app.post("/employee/create")
async def create_employee(employee: Employee = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = """
                CALL spCreateEmployee(%s ,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql, (
                employee.employee_id, employee.company_id, employee.first_name, employee.last_name,
                employee.phone_number, employee.email, employee.invite_url, employee.specialization,
                employee.areas_covered, employee.assigned_locations, employee.employee_status,
                employee.employee_no_of_completed_work, employee.no_of_pending_works, employee.street,
                employee.city, employee.zip, employee.skills, employee.qualification, employee.experience,
                employee.available, employee.photo,employee.last_modified_by
            ))
            connection.commit()

            return {"message": "Employee created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        raise HTTPException(status_code=500, detail={"message": "Employee creation failed"})
    finally:
        if connection:
            connection.close()

# Get Employee by ID
@app.get("/employee/get/{employee_id}")
async def get_employee(employee_id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetByIdEmployee(%s);"
            cursor.execute(sql, (employee_id,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")
    except pymysql.MySQLError as err:
        print(f"Error fetching employee info: {err}")
        raise HTTPException(status_code=500, detail={"error": "Employee fetch call failed (DB Error)"})
    finally:
        if connection:
            connection.close()

# Get All Employees
@app.get("/employee/getall")
async def get_all_employees():
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllEmployees();"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as err:
        print(f"Error fetching employee info: {err}")
        raise HTTPException(status_code=500, detail={"error": "Employee fetch all call failed (DB Error)"})
    finally:
        if connection:
            connection.close()

# Update Employee
@app.put("/employee/update/{employee_id}")
async def update_employee(employee_id: str, employee: Employee = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = """
                CALL spUpdateEmployee(%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s);
            """
            cursor.execute(sql, (
                employee_id, employee.company_id, employee.first_name, employee.last_name,
                employee.phone_number, employee.email, employee.invite_url, employee.specialization,
                employee.areas_covered, employee.assigned_locations, employee.employee_status,
                employee.employee_no_of_completed_work, employee.no_of_pending_works, employee.street,
                employee.city, employee.zip, employee.skills, employee.qualification, employee.experience,
                employee.available, employee.photo,employee.last_modified_by
            ))
            connection.commit()

            return {"message": f"Employee with ID {employee_id} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating employee info: {err}")
        raise HTTPException(status_code=500, detail={"error": f"Employee with ID {employee_id} update call failed"})
    finally:
        if connection:
            connection.close()

# Delete Employee
@app.delete("/employee/delete/{employee_id}")
async def delete_employee(employee_id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spDeleteEmployee(%s);"
            cursor.execute(sql, (employee_id,))
            connection.commit()

            return {"message": f"Employee with ID {employee_id} deleted successfully"}
    except pymysql.MySQLError as err:
        print(f"Error deleting employee info: {err}")
        raise HTTPException(status_code=500, detail={"error": f"Employee with ID {employee_id} delete call failed"})
    finally:
        if connection:
            connection.close()

