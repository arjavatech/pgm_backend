CREATE DATABASE pgm_test;

USE pgm_test;

CREATE TABLE `admin_info` (
  `email_id` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `designation` varchar(255) DEFAULT NULL,
  `apporved_by` varchar(255) DEFAULT NULL,
  `is_active` BOOLEAN DEFAULT TRUE,
  PRIMARY KEY (`email_id`)
);

DELIMITER //

CREATE PROCEDURE `spCreateAdminInfo`(
    IN p_email_id VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_designation VARCHAR(255),
    IN p_apporved_by VARCHAR(255)
)
BEGIN
    INSERT INTO admin_info (email_id, password, designation, apporved_by, is_active)
    VALUES (p_email_id, p_password, p_designation, p_apporved_by, TRUE);
END //


DELIMITER //

CREATE PROCEDURE `spDeleteAdminInfo`(
    IN p_email_id VARCHAR(255)
)
BEGIN
    UPDATE admin_info
    SET is_active = FALSE
    WHERE 
        email_id = p_email_id;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE `spGetAdminInfo`(
    IN p_email_id VARCHAR(255)
)
BEGIN
    SELECT * FROM admin_info
    WHERE email_id = p_email_id AND is_active = TRUE;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spGetAllAdminInfo`()
BEGIN
    SELECT * FROM admin_info
    WHERE is_active = TRUE;
END //

DELIMITER ;

DELIMITER //


CREATE PROCEDURE `spUpdateAdminInfo`(
    IN p_email_id VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_designation VARCHAR(255),
    IN p_apporved_by VARCHAR(255)
)
BEGIN
    UPDATE admin_info
    SET 
        password = COALESCE(p_password, password),
        designation = COALESCE(p_designation, designation),
        apporved_by = COALESCE(p_apporved_by, apporved_by)
    WHERE 
        email_id = p_email_id AND is_active = TRUE;
END //

DELIMITER ;

call pgm_test.spCreateAdminInfo('pitchumaniece@gmail.com', '', '', '');


CREATE TABLE `invite_info` (
  `email` varchar(255) NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `time_stamp` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`email`)
);


DELIMITER //

CREATE PROCEDURE `spCreateInviteInfo`(
    IN p_email VARCHAR(255),
    IN p_url VARCHAR(255),
    IN p_time_stamp VARCHAR(255),
    IN p_status VARCHAR(255)
)
BEGIN
    INSERT INTO invite_info (email, url, time_stamp, status)
    VALUES (p_email, p_url, p_time_stamp, p_status);
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spDeleteInviteInfo`(
    IN p_email VARCHAR(255)
)
BEGIN
    DELETE FROM invite_info
    WHERE email = p_email;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `spGetInviteInfo`(
    IN p_email VARCHAR(255)
)
BEGIN
    SELECT * FROM invite_info
    WHERE email = p_email;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE `spGetAllInviteInfo`()
BEGIN
    SELECT * FROM invite_info;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE `spUpdateInviteInfo`(
    IN p_email VARCHAR(255),
    IN p_url VARCHAR(255),
    IN p_time_stamp VARCHAR(255),
    IN p_status VARCHAR(255)
)
BEGIN
    UPDATE invite_info
    SET 
        url = COALESCE(p_url, url),
        time_stamp = COALESCE(p_time_stamp, time_stamp),
        status = COALESCE(p_status, status)
    WHERE 
        email = p_email;
END //

DELIMITER ;

CREATE TABLE company (
    company_id VARCHAR(255) NOT NULL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    logo TEXT,
    phone_number VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    street VARCHAR(255),
    city VARCHAR(100),
    zip VARCHAR(20),
    state VARCHAR(100),
    isactive BOOLEAN DEFAULT TRUE
);

DELIMITER //

CREATE PROCEDURE `spCreateCompany`(
    IN p_company_id VARCHAR(255),
    IN p_company_name VARCHAR(255),
    IN p_logo TEXT,
    IN p_phone_number VARCHAR(20),
    IN p_email VARCHAR(255),
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_street VARCHAR(255),
    IN p_city VARCHAR(100),
    IN p_zip VARCHAR(20),
    IN p_state VARCHAR(100)
)
BEGIN
    INSERT INTO company (company_id, company_name, logo, phone_number, email, first_name, last_name, street, city, zip, state, isactive)
    VALUES (p_company_id, p_company_name, p_logo, p_phone_number, p_email, p_first_name, p_last_name, p_street, p_city, p_zip, p_state, TRUE);
END //

DELIMITER //

CREATE PROCEDURE `spGetCompanyById`(
    IN p_company_id VARCHAR(255)
)
BEGIN
    SELECT * FROM company
    WHERE company_id = p_company_id AND isactive = TRUE;
END //

DELIMITER //

CREATE PROCEDURE `spGetAllActiveCompanies`()
BEGIN
    SELECT * FROM company
    WHERE isactive = TRUE;
END //

DELIMITER //

CREATE PROCEDURE `spUpdateCompany`(
    IN p_company_id VARCHAR(255),
    IN p_company_name VARCHAR(255),
    IN p_logo TEXT,
    IN p_phone_number VARCHAR(20),
    IN p_email VARCHAR(255),
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_street VARCHAR(255),
    IN p_city VARCHAR(100),
    IN p_zip VARCHAR(20),
    IN p_state VARCHAR(100)
)
BEGIN
    UPDATE company
    SET 
        company_name = COALESCE(p_company_name, company_name),
        logo = COALESCE(p_logo, logo),
        phone_number = COALESCE(p_phone_number, phone_number),
        email = COALESCE(p_email, email),
        first_name = COALESCE(p_first_name, first_name),
        last_name = COALESCE(p_last_name, last_name),
        street = COALESCE(p_street, street),
        city = COALESCE(p_city, city),
        zip = COALESCE(p_zip, zip),
        state = COALESCE(p_state, state)
    WHERE company_id = p_company_id AND isactive = TRUE;
END //

DELIMITER //

CREATE PROCEDURE `spDeleteCompany`(
    IN p_company_id VARCHAR(255)
)
BEGIN
    UPDATE company
    SET isactive = FALSE
    WHERE company_id = p_company_id;
END //

DELIMITER //



CREATE TABLE sign_up(
	company_id VARCHAR(255),
    id VARCHAR(255) PRIMARY KEY,
    login_type VARCHAR(100),
    password VARCHAR(100),
    approved_by VARCHAR(100),
    signup_url VARCHAR(255),
    is_employee BOOLEAN,    
    is_active BOOLEAN DEFAULT TRUE,    
    FOREIGN KEY(company_id) REFERENCES company(company_id)
);

-- Stored Procedures for Sign Up

DELIMITER //

CREATE PROCEDURE spCreate_Sign_Up(
    p_company_id VARCHAR(255),
    p_id VARCHAR(255),
    p_login_type VARCHAR(100),
    p_password VARCHAR(100),
    p_approved_by VARCHAR(100),
    p_signup_url VARCHAR(255),
    p_is_employee BOOLEAN
)
BEGIN
    INSERT INTO sign_up (company_id, id, login_type, password, approved_by, signup_url, is_employee, is_active)
    VALUES (p_company_id, p_id, p_login_type, p_password, p_approved_by, p_signup_url, p_is_employee, TRUE);
END //

DELIMITER //

CREATE PROCEDURE spGetSignUpById(
    p_id VARCHAR(255)
)
BEGIN
    SELECT * FROM sign_up WHERE id = p_id AND is_active = TRUE;
END //

DELIMITER //

CREATE PROCEDURE GetAllSignUp()
BEGIN
    SELECT * FROM sign_up WHERE is_active = TRUE;
END //

DELIMITER //

CREATE PROCEDURE spUpdateSignUp(
    p_id VARCHAR(255),
    p_login_type VARCHAR(100),
    p_password VARCHAR(100),
    p_approved_by VARCHAR(100),
    p_signup_url VARCHAR(255),
    p_is_employee BOOLEAN
)
BEGIN
    UPDATE sign_up
    SET login_type = COALESCE(p_login_type, login_type),
        password = COALESCE(p_password, password),
        approved_by = COALESCE(p_approved_by, approved_by),
        signup_url = COALESCE(p_signup_url, signup_url),
        is_employee = COALESCE(p_is_employee, is_employee)
    WHERE id = p_id;
END //

DELIMITER //

CREATE PROCEDURE spDeleteSignUp(
    p_id VARCHAR(255)
)
BEGIN
    UPDATE sign_up 
    SET is_active = FALSE 
    WHERE id = p_id;
END //

DELIMITER //

-- Ticket Info Table Creation
CREATE TABLE ticket_info(
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,    -- Changed from issue_id to ticket_id
    company_id VARCHAR(255),
    ticket_type VARCHAR(100),                    -- Changed from issue_type to ticket_type
    name VARCHAR(100),
    phone_number VARCHAR(50) DEFAULT NULL,
    images VARCHAR(100) DEFAULT NULL,
    status INT DEFAULT 1,
    complain_raised_date DATE DEFAULT NULL,
    description VARCHAR(100) DEFAULT NULL,
    available_slots VARCHAR(100) DEFAULT NULL,
    rejected_reason VARCHAR(100) DEFAULT NULL,
    rejected_date DATE DEFAULT NULL,
    street VARCHAR(100) DEFAULT NULL,
    city VARCHAR(100) DEFAULT NULL,
    zip INT DEFAULT NULL,
    state VARCHAR(100) DEFAULT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY(company_id) REFERENCES company(company_id)
);

-- Stored Procedure: Create a new ticket
DELIMITER //
CREATE PROCEDURE spCreateTicketInfo(
    IN p_company_id VARCHAR(255),
    IN p_ticket_type VARCHAR(100),               -- Changed from issue_type to ticket_type
    IN p_name VARCHAR(100),
    IN p_phone_number VARCHAR(50),
    IN p_images VARCHAR(100),
    IN p_status INT,
    IN p_complain_raised_date DATE,
    IN p_description VARCHAR(100),
    IN p_available_slots VARCHAR(100),
    IN p_rejected_reason VARCHAR(100),
    IN p_rejected_date DATE,
    IN p_street VARCHAR(100),
    IN p_city VARCHAR(100),
    IN p_zip INT,
    IN p_state VARCHAR(100)
)
BEGIN
    INSERT INTO ticket_info (company_id, ticket_type, name, phone_number, images,  status, complain_raised_date, description, available_slots, rejected_reason, rejected_date, street, city, zip, state, is_active)
    VALUES (p_company_id, p_ticket_type, p_name, p_phone_number, p_images, p_status, p_complain_raised_date, p_description, p_available_slots, p_rejected_reason, p_rejected_date, p_street, p_city, p_zip, p_state, TRUE);
END //
DELIMITER ;

-- Stored Procedure: Retrieve a ticket by ticket_id
DELIMITER //
CREATE PROCEDURE spGetTicketInfoById(
    IN p_ticket_id INT                            -- Changed from issue_id to ticket_id
)
BEGIN
    SELECT * FROM ticket_info WHERE ticket_id = p_ticket_id AND is_active = TRUE;
END //
DELIMITER ;

-- Stored Procedure: Retrieve all tickets
DELIMITER //
CREATE PROCEDURE spGetAllTicketInfo()
BEGIN
    SELECT * FROM ticket_info WHERE is_active = TRUE;
END //
DELIMITER ;

-- Stored Procedure: Update ticket information
DELIMITER //
CREATE PROCEDURE spUpdateTicketInfo(
    IN p_ticket_id INT,                          -- Changed from issue_id to ticket_id
    IN p_company_id VARCHAR(255),
    IN p_ticket_type VARCHAR(100),               -- Changed from issue_type to ticket_type
    IN p_name VARCHAR(100),
    IN p_phone_number VARCHAR(50),
    IN p_images VARCHAR(100),
    IN p_status INT,
    IN p_complain_raised_date DATE,
    IN p_description VARCHAR(100),
    IN p_available_slots VARCHAR(100),
    IN p_rejected_reason VARCHAR(100),
    p_rejected_date DATE,
    IN p_street VARCHAR(100),
    IN p_city VARCHAR(100),
    IN p_zip INT,
    IN p_state VARCHAR(100)
)
BEGIN
    UPDATE ticket_info
    SET ticket_type = COALESCE(p_ticket_type,ticket_type),           
        name = COALESCE(p_name,name),
        phone_number = COALESCE(p_phone_number,phone_number),
        images = COALESCE(p_images,images),
        status = COALESCE(p_status,status),
        complain_raised_date = COALESCE(p_complain_raised_date,complain_raised_date),
        description = COALESCE(p_description,description),
        available_slots = COALESCE(p_available_slots,available_slots),
        rejected_reason = COALESCE(p_rejected_reason,rejected_reason),
        rejected_date = COALESCE(p_rejected_date,rejected_date),
        street = COALESCE(p_street,street),
        city = COALESCE(p_city,city),
        zip = COALESCE(p_zip,zip),
        state = COALESCE(p_state,state)
    WHERE ticket_id = p_ticket_id;               -- Changed from issue_id to ticket_id
END //
DELIMITER ;

-- Stored Procedure: Soft delete (deactivate) a ticket by ticket_id
DELIMITER //
CREATE PROCEDURE spDeleteTicketInfo(
    IN p_ticket_id INT                           -- Changed from issue_id to ticket_id
)
BEGIN
    UPDATE ticket_info
    SET is_active = FALSE
    WHERE ticket_id = p_ticket_id;               -- Changed from issue_id to ticket_id
END //
DELIMITER ;


CREATE TABLE employee (
    employee_id CHAR(100) PRIMARY KEY,               
    company_id VARCHAR(100),
    first_name VARCHAR(100) ,
    last_name VARCHAR(100) ,
    phone_number VARCHAR(15) UNIQUE,
    email VARCHAR(100) UNIQUE DEFAULT NULL,
    invite_url VARCHAR(255) DEFAULT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    specialization VARCHAR(255),
    areas_covered TEXT DEFAULT NULL,
    assigned_locations TEXT DEFAULT NULL,
    employee_status VARCHAR(50),
    employee_no_of_completed_work INT DEFAULT 0,
    no_of_pending_works INT DEFAULT 0,
    street VARCHAR(255) DEFAULT NULL,
    city VARCHAR(100) DEFAULT NULL,
    zip VARCHAR(10) DEFAULT NULL,
    skills TEXT DEFAULT NULL,
    qualification TEXT DEFAULT NULL,
    experience TEXT DEFAULT NULL,
    registered_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    available BOOLEAN DEFAULT NULL,
    photo BLOB DEFAULT NULL,
    FOREIGN KEY (company_id) REFERENCES company(company_id) ON DELETE CASCADE
);

-- Stored Procedure to Create Employee
DELIMITER //

CREATE PROCEDURE spCreateEmployee(
    IN p_employee_id CHAR(100),
    IN p_company_id VARCHAR(100),
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_phone_number VARCHAR(15),
    IN p_email VARCHAR(100),
    IN p_invite_url VARCHAR(255),
    IN p_specialization VARCHAR(255),
    IN p_areas_covered TEXT,
    IN p_assigned_locations TEXT,
    IN p_employee_status VARCHAR(50),
    IN p_employee_no_of_completed_work INT,
    IN p_no_of_pending_works INT,
    IN p_street VARCHAR(255),
    IN p_city VARCHAR(100),
    IN p_zip VARCHAR(10),
    IN p_skills TEXT,
    IN p_qualification TEXT,
    IN p_experience TEXT,
    IN p_available BOOLEAN,
    IN p_photo BLOB
)
BEGIN
    INSERT INTO employee (
        employee_id, company_id, first_name, last_name,
        phone_number, email, invite_url, is_active,
        specialization, areas_covered, assigned_locations,
        employee_status, employee_no_of_completed_work,
        no_of_pending_works, street, city, zip, skills,
        qualification, experience, registered_time, available,
        photo
    ) VALUES (
        p_employee_id, p_company_id, p_first_name, p_last_name,
        p_phone_number, p_email, p_invite_url, TRUE,
        p_specialization, p_areas_covered, p_assigned_locations,
        p_employee_status, p_employee_no_of_completed_work,
        p_no_of_pending_works, p_street, p_city, p_zip, p_skills,
        p_qualification, p_experience, CURRENT_TIMESTAMP, p_available,
        p_photo
    );
END //

DELIMITER ;

-- Stored Procedure to Read Employee
DELIMITER //

CREATE PROCEDURE spGetByIdEmployee(
    IN p_employee_id CHAR(100)
)
BEGIN
    SELECT * FROM employee WHERE employee_id = p_employee_id;
END //
spUpdateEmployee
DELIMITER ;

-- Stored Procedure to Update Employee
DELIMITER //

CREATE PROCEDURE spUpdateEmployee(
    IN p_employee_id CHAR(100),
    IN p_company_id VARCHAR(100),
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_phone_number VARCHAR(15),
    IN p_email VARCHAR(100),
    IN p_invite_url VARCHAR(255),
    IN p_specialization VARCHAR(255),
    IN p_areas_covered TEXT,
    IN p_assigned_locations TEXT,
    IN p_employee_status VARCHAR(50),
    IN p_employee_no_of_completed_work INT,
    IN p_no_of_pending_works INT,
    IN p_street VARCHAR(255),
    IN p_city VARCHAR(100),
    IN p_zip VARCHAR(10),
    IN p_skills TEXT,
    IN p_qualification TEXT,
    IN p_experience TEXT,
    IN p_available BOOLEAN,
    IN p_photo BLOB
)
BEGIN
    UPDATE employee
    SET
        company_id = COALESCE(p_company_id,company_id),
        first_name = COALESCE(p_first_name,first_name),
        last_name = COALESCE(p_last_name,last_name),
        phone_number = COALESCE(p_phone_number,phone_number),
        email = COALESCE(p_email,email),
        invite_url = COALESCE(p_invite_url,invite_url),
        specialization = COALESCE(p_specialization,specialization),
        areas_covered = COALESCE(p_areas_covered,areas_covered),
        assigned_locations = COALESCE(p_assigned_locations,assigned_locations),
        employee_status = COALESCE(p_employee_status,employee_status),
        employee_no_of_completed_work = COALESCE(p_employee_no_of_completed_work,employee_no_of_completed_work),
        no_of_pending_works = COALESCE(p_no_of_pending_works,no_of_pending_works),
        street = COALESCE(p_street,street),
        city = COALESCE(p_city,city),
        zip = COALESCE(p_zip,zip),
        skills = COALESCE(p_skills,skills),
        qualification = COALESCE(p_qualification,qualification),
        experience = COALESCE(p_experience,qualification),
        available = COALESCE(p_available,available),
        photo = COALESCE(p_photo,photo)
    WHERE employee_id = p_employee_id;
END //

DELIMITER ;

-- Stored Procedure to Delete Employee
DELIMITER //

CREATE PROCEDURE spDeleteEmployee(
    IN p_employee_id CHAR(100)
)
BEGIN
    DELETE FROM employee WHERE employee_id = p_employee_id;
END //

DELIMITER ;

-- Stored Procedure to Get All Employees
DELIMITER //

CREATE PROCEDURE spGetAllEmployees()
BEGIN
    SELECT * FROM employee;
END //

DELIMITER ;

-- Stored Procedure to Get All Employees & Available Employees Count
DELIMITER //

CREATE PROCEDURE spGetEmployeeCount(
IN p_company_id VARCHAR(255))
BEGIN
	SELECT 
		COUNT(CASE WHEN is_active = TRUE THEN 1 END) AS total_employee,
		COUNT(CASE WHEN available = 1 and is_active = TRUE THEN 1 END) AS available_employee
		FROM employee 
		WHERE company_id = p_company_id;
END //

DELIMITER ;

-- Stored Procedure to Get Ticket Counts
DELIMITER //

CREATE PROCEDURE spGetTicketCount()
BEGIN
    SELECT 
		COUNT(id) AS total_tickets,
		COUNT(CASE WHEN service_status = 'pending' THEN 1 END) AS pending_tickets,
        COUNT(CASE WHEN service_status = 'inprogress' THEN 1 END) AS inprogress_tickets,
        COUNT(CASE WHEN service_status = 'completed' THEN 1 END) AS completed_tickets
		FROM ticket_status;
END //

DELIMITER ;


