from http.client import HTTPException
from fastapi import APIRouter, Body, FastAPI, HTTPException, Path
from fastapi.params import Body
import pymysql
from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime, date
import mangum
import yagmail
import shortuuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials = True, allow_methods=["*"], allow_headers=["*"]
)

def connect_to_database():
    try:
        connection = pymysql.connect(
            host="pgm.cxms2oikutcu.us-west-2.rds.amazonaws.com",
            port=3306,
            user="admin",
            password="AWSpass01#",
            database="pgm_test",
            cursorclass=pymysql.cursors.DictCursor 
        )
        return connection
    except pymysql.MySQLError as err:
        return None

@app.get("/test")
def get_test():
    return {"response": "Test get call successfully called"}

# AdminInfo Schema

class AdminInfo(BaseModel):
    email: str
    password: Optional[str] = None
    designation: Optional[str] = None
    apporved_by: Optional[str] = None
    is_active: Optional[bool] = None

# --------- Admin Info Endpoints ---------

@app.post("/admin_info/create")
async def create_admin_info(admin_info: AdminInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = "CALL spCreateAdminInfo(%s, %s, %s, %s);"
            cursor.execute(sql, (admin_info.email, admin_info.password, admin_info.designation, admin_info.apporved_by))
            connection.commit()

            return {"message": "AdminInfo created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        raise HTTPException(status_code=500, detail={"message": "AdminInfo creation Failed!!!"})
    finally:
        if connection:
            connection.close()

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

@app.put("/admin_info/update/{email_id}")
async def update_admin_info(email_id: str, admin_info: AdminInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateAdminInfo(%s, %s, %s, %s);"
            cursor.execute(sql, (email_id, admin_info.password, admin_info.designation, admin_info.apporved_by))
            connection.commit()

            return {"message": f"Admin Info with email_id {email_id} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating signup_info: {err}")
        raise HTTPException(status_code=500, detail={"error": f"Admin Info with email_id {email_id} update call failed (DB Error)"})
    finally:
        if connection:
            connection.close()

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


    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spDeleteAdmin(%s)"
            cursor.execute(sql, (id,))
            connection.commit()
            return {"message": "Admin deleted successfully"}

    except pymysql.MySQLError as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        connection.close()

class InviteInfo(BaseModel):
    email: str
    url: Optional[str] = None
    time_stamp: Optional[str] = None
    status: Optional[str] = None

# --------- Invite Info Endpoints ---------

@app.post("/invite_info/create")
async def create_invite_info(invite_info: InviteInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = "CALL spCreateInviteInfo(%s, %s, %s, %s);"
            cursor.execute(sql, (invite_info.email, invite_info.url, invite_info.time_stamp, invite_info.status))
            connection.commit()

            return {"message": "InviteInfo created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        raise HTTPException(status_code=500, detail={"message": "InviteInfo creation Failed!!!"})
    finally:
        if connection:
            connection.close()

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

@app.put("/invite_info/update/{email}")
async def update_invite_info(email: str, invite_info: InviteInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateInviteInfo(%s, %s, %s, %s);"
            cursor.execute(sql, (email, invite_info.url, invite_info.time_stamp, invite_info.status))
            connection.commit()

            return {"message": f"Invite Info with email {email} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating invite_info: {err}")
        raise HTTPException(status_code=500, detail={"error": f"Invite Info with email {email} update call failed (DB Error)"})
    finally:
        if connection:
            connection.close()

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

class CompanyInfo(BaseModel):
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    logo: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    state: Optional[str] = None

@app.post("/company/create")
async def create_company(company_info: CompanyInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            company_id = shortuuid.uuid()
            sql = "CALL spCreateCompany(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                company_id, 
                company_info.company_name, 
                company_info.logo, 
                company_info.phone_number, 
                company_info.email, 
                company_info.first_name, 
                company_info.last_name, 
                company_info.street, 
                company_info.city, 
                company_info.zip, 
                company_info.state
            ))
            connection.commit()

            return {"message": "Company created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error creating company: {err}")
        raise HTTPException(status_code=500, detail="Company creation failed (DB Error)")
    finally:
        if connection:
            connection.close()

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

@app.put("/company/update/{company_id}")
async def update_company(company_id: str, company_info: CompanyInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateCompany(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                company_id, 
                company_info.company_name, 
                company_info.logo, 
                company_info.phone_number, 
                company_info.email, 
                company_info.first_name, 
                company_info.last_name, 
                company_info.street, 
                company_info.city, 
                company_info.zip, 
                company_info.state
            ))
            connection.commit()

            return {"message": f"Company with ID {company_id} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating company: {err}")
        raise HTTPException(status_code=500, detail="Update company failed (DB Error)")
    finally:
        if connection:
            connection.close()

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

# Model for Sign Up
class SignUp(BaseModel):
    company_id: str
    id: Optional[str] = None
    login_type: Optional[str] = None
    password: Optional[str] = None
    approved_by: Optional[str] = None
    signup_url: Optional[str] = None
    is_employee: Optional[bool] = None

# Create Sign Up API
@app.post("/sign_up/create")
async def create_sign_up(sign_up: SignUp = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:
            sql = "CALL spCreate_Sign_Up(%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                sign_up.company_id, 
                sign_up.id, 
                sign_up.login_type, 
                sign_up.password, 
                sign_up.approved_by, 
                sign_up.signup_url, 
                sign_up.is_employee
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
            sql = "CALL spUpdateSignUp(%s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                id,
                sign_up.login_type,
                sign_up.password,
                sign_up.approved_by,
                sign_up.signup_url,
                sign_up.is_employee
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
                CALL spUpdateTicketInfo(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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

# Employee model
class Employee(BaseModel):
    company_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    invite_url: Optional[str] = None
    specialization: Optional[str] = None
    areas_covered: Optional[str] = None
    assigned_locations: Optional[str] = None
    employee_status: Optional[str] = None
    employee_no_of_completed_work: Optional[int] = 0
    no_of_pending_works: Optional[int] = 0
    street: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    skills: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[str] = None
    available: Optional[bool] = None
    photo: Optional[bytes] = None

# --------- Employee Endpoints ---------

# Create Employee
@app.post("/employee/create")
async def create_employee(employee: Employee = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            employee_id = shortuuid.uuid()
            sql = """
                CALL spCreateEmployee(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql, (
                employee_id, employee.company_id, employee.first_name, employee.last_name,
                employee.phone_number, employee.email, employee.invite_url, employee.specialization,
                employee.areas_covered, employee.assigned_locations, employee.employee_status,
                employee.employee_no_of_completed_work, employee.no_of_pending_works, employee.street,
                employee.city, employee.zip, employee.skills, employee.qualification, employee.experience,
                employee.available, employee.photo
            ))
            connection.commit()

            company_sql = "CALL spGetCompanyById(%s);"
            cursor.execute(company_sql, (employee.company_id,))
            result = cursor.fetchone()

            url = f"http://127.0.0.1:5501/signUp.html?invite_id_e={employee.company_id}"

            sender = 'pitchumaniece@gmail.com'
            app_password = 'oppv abhd hfwh kavm'
            subject = f"Welcome to {result["company_name"]} – Activate Your Account and Get Started!"



            html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
                    <div style="max-width: 500px; margin: auto; padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px;">
                        <p>Dear {employee.first_name+" "+employee.last_name},</p>
                        <p>Welcome to <strong>{result["company_name"]}</strong>! We are excited to have you as part of our team. Your registration process has been successfully completed, and you can now access your account using the button below.</p>
                        <p style="text-align: center;">
                            <a href="{url}" style="display: inline-block; padding: 10px 20px; margin: 10px 0; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Activate Your Account</a>
                        </p>
                        <p>If you have any questions or need further assistance during your onboarding process, please don't hesitate to reach out to your HR representative. We're here to ensure you have a smooth experience getting started at <strong>{result["company_name"]}</strong>.</p>
                        
                        <p>Thank you for being part of our journey, and we look forward to working together to achieve great things.</p>

                        <p>Best regards,<br>HR Support Team<br><strong>{result["company_name"]}</strong></p>
                    </div>
                </body>
                </html>
                """
            
            # Initialize Yagmail with the sender's Gmail credentials
            yag = yagmail.SMTP(user=sender, password=app_password)

            # Sending the email
            yag.send(to=employee.email, subject=subject, contents=html_content)


            return {"message": "Employee created successfully and mail sent done!!!!!"}
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
                CALL spUpdateEmployee(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql, (
                employee_id, employee.company_id, employee.first_name, employee.last_name,
                employee.phone_number, employee.email, employee.invite_url, employee.specialization,
                employee.areas_covered, employee.assigned_locations, employee.employee_status,
                employee.employee_no_of_completed_work, employee.no_of_pending_works, employee.street,
                employee.city, employee.zip, employee.skills, employee.qualification, employee.experience,
                employee.available, employee.photo
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

@app.post("/company_register/create")
async def company_register_call(company_info: CompanyInfo = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            company_id = shortuuid.uuid()

            sql = "CALL spCreateCompany(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                company_id, 
                company_info.company_name, 
                company_info.logo, 
                company_info.phone_number, 
                company_info.email, 
                company_info.first_name, 
                company_info.last_name, 
                company_info.street, 
                company_info.city, 
                company_info.zip, 
                company_info.state
            ))
            connection.commit()
            url = f"http://127.0.0.1:5501/signUp.html?invite_id_c={company_id}"

            current_datetime = datetime.now()

            invite_sql = "CALL spCreateInviteInfo(%s, %s, %s, %s);"
            cursor.execute(invite_sql, (company_info.email, url, current_datetime , "Pending"))
            connection.commit()

            company_name = "PG Mechanical"

            sender = 'pitchumaniece@gmail.com'
            app_password = 'oppv abhd hfwh kavm'
            subject = "Invitation to Create an Account for The PG Mechanical Scheduler App"

            # Email content in HTML
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
                <div style="max-width: 500px; margin: auto; padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px;">
                    <p>Dear {company_info.first_name+" "+company_info.last_name},</p>
                    <p>We hope this message finds you well. We wanted to confirm that we have received your recent request and appreciate the opportunity to assist you. Rest assured, our team is now reviewing the information you provided, and we are committed to addressing your needs as promptly as possible. Click the button to continue using our app,</p>
                    <p style="text-align: center;">
                        <a href="{url}" style="display: inline-block; padding: 10px 20px; margin: 10px 0; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Create Your Account</a>
                    </p>
                    <p>A dedicated representative will be in touch with you soon to provide further assistance and ensure all your queries are answered. In the meantime, if you have any additional questions or require further clarification, please do not hesitate to reach out to us. We are here to help and ensure you receive the best possible service.</p>
                    
                    <p>Thank you for choosing <strong>{company_name}</strong>. We look forward to working with you.</p>

                    <p>Best regards,<br>PG Support Team<br><strong>{company_name}</strong></p>
                </div>
            </body>
            </html>
            """
            # Initialize Yagmail with the sender's Gmail credentials
            yag = yagmail.SMTP(user=sender, password=app_password)

            # Sending the email
            yag.send(to=company_info.email, subject=subject, contents=html_content)

            return {"message": "Email sent successfully"}
    except pymysql.MySQLError as err:
        print(f"Error calling stored procedure: {err}")
        raise HTTPException(status_code=500, detail={"message": "Email sent failed"})
    finally:
        if connection:
            connection.close()

@app.get("/account_check/{email}")
async def account_check(email: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAdminInfo(%s);"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            if result:
                return {"isSuperAdmin": True}
            else:
                signup_sql = "CALL spGetSignUpById(%s);"
                cursor.execute(signup_sql, (email,))
                result = cursor.fetchone()

                if result:
                    if result["is_employee"]==True:
                        return {"isEmployee": True}
                    else:
                        return {"isadmin": True}
                else:
                    raise HTTPException(status_code=404, detail=f"User {email} not exist")
                
    except pymysql.MySQLError as err:
        print(f"Error creating SignUp: {err}")
        raise HTTPException(status_code=500, detail="User found api failed (DB Error)")
    finally:
        if connection:
            connection.close()
    
# Define the Ticket Status model
class TicketStatus(BaseModel):
    company_id: str
    employee_id: str
    ticket_id: int
    work_started_time: Optional[datetime] = None
    work_ended_time: Optional[datetime] = None
    photos: Optional[str] = None
    service_status: Optional[str] = None 
    rejected_reason: Optional[str] = None

@app.post("/ticket_status/create")
async def create_ticket_status(ticket_status: TicketStatus = Body(...)):
    connection = connect_to_database()
    if not connection:
        return {"error": "Failed to connect to database"}

    try:
        with connection.cursor() as cursor:

            ticket_token = shortuuid.uuid()

            sql = "CALL spCreateTicketStatus(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                ticket_token,
                ticket_status.company_id,
                ticket_status.employee_id,
                ticket_status.ticket_id,
                ticket_status.work_started_time,
                ticket_status.work_ended_time,
                ticket_status.photos,
                ticket_status.service_status,
                ticket_status.rejected_reason
            ))
            connection.commit()

            return {"message": "Ticket status created successfully"}
    except pymysql.MySQLError as err:
        print(f"Error creating ticket status: {err}")
        raise HTTPException(status_code=500, detail="Ticket status creation failed (DB Error)")
    finally:
        if connection:
            connection.close()

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

@app.put("/ticket_status/update/{ticket_token}")
async def update_ticket_status(ticket_token: str, ticket_status: TicketStatus = Body(...)):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateTicketStatus(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                ticket_token,
                ticket_status.company_id,
                ticket_status.employee_id,
                ticket_status.ticket_id,
                ticket_status.work_started_time,
                ticket_status.work_ended_time,
                ticket_status.photos,
                ticket_status.service_status,
                ticket_status.rejected_reason
            ))
            connection.commit()

            return {"message": f"Ticket status with ID {ticket_token} updated successfully"}
    except pymysql.MySQLError as err:
        print(f"Error updating ticket status: {err}")
        raise HTTPException(status_code=500, detail="Update ticket status failed (DB Error)")
    finally:
        if connection:
            connection.close()

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

@app.get("/tickets/rejected/{company_id}")
async def get_rejected_tickets(company_id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllRejectedTickets(%s);"
            cursor.execute(sql, (company_id,))
            result = cursor.fetchall()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail="No rejected tickets found")
    except pymysql.MySQLError as err:
        print(f"Error fetching rejected tickets: {err}")
        raise HTTPException(status_code=500, detail="Failed to fetch rejected tickets (DB Error)")
    finally:
        if connection:
            connection.close()

@app.get("/tickets/unassigned/{company_id}")
async def get_unassigned_tickets(company_id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllUnassignedTickets(%s);"
            cursor.execute(sql, (company_id,))
            result = cursor.fetchall()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail="No unassigned tickets found")
    except pymysql.MySQLError as err:
        print(f"Error fetching unassigned tickets: {err}")
        raise HTTPException(status_code=500, detail="Failed to fetch unassigned tickets (DB Error)")
    finally:
        if connection:
            connection.close()

@app.get("/tickets/inprogress/{company_id}")
async def get_inprogress_tickets(company_id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllInProgressTickets(%s);"
            cursor.execute(sql, (company_id,))
            result = cursor.fetchall()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail="No in-progress tickets found")
    except pymysql.MySQLError as err:
        print(f"Error fetching in-progress tickets: {err}")
        raise HTTPException(status_code=500, detail="Failed to fetch in-progress tickets (DB Error)")
    finally:
        if connection:
            connection.close()


@app.get("/tickets/completed/{company_id}")
async def get_completed_tickets(company_id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllCompletedTickets(%s);"
            cursor.execute(sql, (company_id,))
            result = cursor.fetchall()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail="No completed tickets found")
    except pymysql.MySQLError as err:
        print(f"Error fetching completed tickets: {err}")
        raise HTTPException(status_code=500, detail="Failed to fetch completed tickets (DB Error)")
    finally:
        if connection:
            connection.close()

            # ---------------Ticket & Employee count------------------
#count of employee
@app.get("/employee_count/{id}")
async def get_ticket_count(id: str):
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetEmployeeCount(%s);"
            cursor.execute(sql, (id,))
            result = cursor.fetchall()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail=f"Count for {id} company not found")
    except pymysql.MySQLError as err:
        print(f"Error fetching employee count: {err}")
        raise HTTPException(status_code=500, detail="Get employee count by status failed (DB Error)")
    finally:
        if connection:
            connection.close() 

#count of tickets
@app.get("/ticket_count")
async def get_ticket_count():
    connection = connect_to_database()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetTicketCount();"
            cursor.execute(sql, ())
            result = cursor.fetchall()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail=f"Count for ticket not found")
    except pymysql.MySQLError as err:
        print(f"Error fetching ticket count: {err}")
        raise HTTPException(status_code=500, detail="Get ticket count by status failed (DB Error)")
    finally:
        if connection:
            connection.close()   

handler=mangum.Mangum(app)
