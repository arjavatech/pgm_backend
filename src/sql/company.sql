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

CREATE PROCEDURE spCreateCompany(
    IN p_company_id VARCHAR(255),
    IN p_company_name VARCHAR(255),
    IN p_logo VARCHAR(255),
    IN p_phone_number VARCHAR(20),
    IN p_email VARCHAR(255),
    IN p_first_name VARCHAR(255),
    IN p_last_name VARCHAR(255),
    IN p_street VARCHAR(255),
    IN p_city VARCHAR(255),
    IN p_zip VARCHAR(10),
    IN p_state VARCHAR(255),
    IN p_last_modified_by VARCHAR(255)
)
BEGIN
    INSERT INTO company_info (
        company_id, company_name, logo, phone_number, email, first_name, last_name, street, city, zip, state, last_modified_by
    ) 
    VALUES (
        p_company_id, p_company_name, p_logo, p_phone_number, p_email, p_first_name, p_last_name, p_street, p_city, p_zip, p_state, p_last_modified_by
    );
END //

DELIMITER ;


CREATE PROCEDURE `spGetAllActiveCompanies`()
BEGIN
    SELECT * FROM company
    WHERE isactive = TRUE;
END //
DELIMITER ;


DELIMITER //

CREATE PROCEDURE spUpdateCompany(
    IN p_company_id VARCHAR(255),
    IN p_company_name VARCHAR(255),
    IN p_logo VARCHAR(255),
    IN p_phone_number VARCHAR(20),
    IN p_email VARCHAR(255),
    IN p_first_name VARCHAR(255),
    IN p_last_name VARCHAR(255),
    IN p_street VARCHAR(255),
    IN p_city VARCHAR(255),
    IN p_zip VARCHAR(10),
    IN p_state VARCHAR(255),
    IN p_last_modified_by VARCHAR(255)
)
BEGIN
    UPDATE company_info 
    SET 
        company_name = p_company_name, 
        logo = p_logo, 
        phone_number = p_phone_number, 
        email = p_email, 
        first_name = p_first_name, 
        last_name = p_last_name, 
        street = p_street, 
        city = p_city, 
        zip = p_zip, 
        state = p_state,
        last_modified_by = p_last_modified_by,
        last_modified_date_time = NOW()
    WHERE company_id = p_company_id;
END //

DELIMITER ;

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