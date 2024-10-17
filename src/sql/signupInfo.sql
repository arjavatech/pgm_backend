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

CREATE PROCEDURE spCreateSignUp(
    p_company_id VARCHAR(255),
    p_id VARCHAR(255),
    p_login_type VARCHAR(100),
    p_password VARCHAR(100),
    p_approved_by VARCHAR(100),
    p_signup_url VARCHAR(255),
    p_is_employee BOOLEAN,
    IN p_last_modified_by VARCHAR(250)
)
BEGIN
    INSERT INTO sign_up (company_id, id, login_type, password, approved_by, signup_url, is_employee, is_active,last_modified_by)
    VALUES (p_company_id, p_id, p_login_type, p_password, p_approved_by, p_signup_url, p_is_employee, TRUE,p_last_modified_by);
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
    p_is_employee BOOLEAN,
    p_last_modified_by VARCHAR(250)
)
BEGIN
    UPDATE sign_up
    SET login_type = COALESCE(p_login_type, login_type),
        password = COALESCE(p_password, password),
        approved_by = COALESCE(p_approved_by, approved_by),
        signup_url = COALESCE(p_signup_url, signup_url),
        is_employee = COALESCE(p_is_employee, is_employee),
        last_modified_by = COALESCE(p_last_modified_by ,last_modified_by)
    WHERE id = p_id;
END //
DELIMITER ;

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
