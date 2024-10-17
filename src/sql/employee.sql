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
    IN p_employee_id VARCHAR(250),
    IN p_company_id VARCHAR(250),
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_phone_number VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_invite_url VARCHAR(255),
    IN p_specialization VARCHAR(100),
    IN p_areas_covered TEXT,
    IN p_assigned_locations TEXT,
    IN p_employee_status ENUM('active', 'inactive', 'suspended'),
    IN p_employee_no_of_completed_work INT,
    IN p_no_of_pending_works INT,
    IN p_street VARCHAR(100),
    IN p_city VARCHAR(100),
    IN p_zip INT,
    IN p_skills TEXT,
    IN p_qualification VARCHAR(100),
    IN p_experience INT,
    IN p_available BOOLEAN,
    IN p_photo VARCHAR(255),
    IN p_last_modified_by VARCHAR(250)
)
BEGIN
    INSERT INTO employee (
        employee_id, company_id, first_name, last_name,
        phone_number, email, invite_url, specialization,
        areas_covered, assigned_locations, employee_status,
        employee_no_of_completed_work, no_of_pending_works, street,
        city, zip, skills, qualification, experience,
        available, photo, last_modified_by
    )
    VALUES (
        p_employee_id, p_company_id, p_first_name, p_last_name,
        p_phone_number, p_email, p_invite_url, p_specialization,
        p_areas_covered, p_assigned_locations, p_employee_status,
        p_employee_no_of_completed_work, p_no_of_pending_works, p_street,
        p_city, p_zip, p_skills, p_qualification, p_experience,
        p_available, p_photo, p_last_modified_by
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
    IN p_employee_id VARCHAR(250),
    IN p_company_id VARCHAR(250),
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_phone_number VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_invite_url VARCHAR(255),
    IN p_specialization VARCHAR(100),
    IN p_areas_covered TEXT,
    IN p_assigned_locations TEXT,
    IN p_employee_status ENUM('active', 'inactive', 'suspended'),
    IN p_employee_no_of_completed_work INT,
    IN p_no_of_pending_works INT,
    IN p_street VARCHAR(100),
    IN p_city VARCHAR(100),
    IN p_zip INT,
    IN p_skills TEXT,
    IN p_qualification VARCHAR(100),
    IN p_experience INT,
    IN p_available BOOLEAN,
    IN p_photo VARCHAR(255),
    IN p_last_modified_by VARCHAR(250)
)
BEGIN
    UPDATE employee
    SET 
        company_id = p_company_id,
        first_name = p_first_name,
        last_name = p_last_name,
        phone_number = p_phone_number,
        email = p_email,
        invite_url = p_invite_url,
        specialization = p_specialization,
        areas_covered = p_areas_covered,
        assigned_locations = p_assigned_locations,
        employee_status = p_employee_status,
        employee_no_of_completed_work = p_employee_no_of_completed_work,
        no_of_pending_works = p_no_of_pending_works,
        street = p_street,
        city = p_city,
        zip = p_zip,
        skills = p_skills,
        qualification = p_qualification,
        experience = p_experience,
        available = p_available,
        photo = p_photo,
        last_modified_by = p_last_modified_by
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
