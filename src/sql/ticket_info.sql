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
    IN p_state VARCHAR(100),
    IN p_last_modified_by VARCHAR(250)
)
BEGIN
    INSERT INTO ticket_info (company_id, ticket_type, name, phone_number, images,  status, complain_raised_date, description, available_slots, rejected_reason, rejected_date, street, city, zip, state, is_active,last_modified_by)
    VALUES (p_company_id, p_ticket_type, p_name, p_phone_number, p_images, p_status, p_complain_raised_date, p_description, p_available_slots, p_rejected_reason, p_rejected_date, p_street, p_city, p_zip, p_state, TRUE,p_last_modified_by);
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
    IN p_state VARCHAR(100),
     IN p_last_modified_by VARCHAR(250)
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
        state = COALESCE(p_state,state),
        last_modified_by = COALESCE(p_last_modified_by,last_modified_by),
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

DELIMITER $$

CREATE PROCEDURE spGetTicketStatusAndInfoByToken(
    IN p_ticket_token VARCHAR(36)
)
BEGIN
    SELECT 
        *
    FROM 
        ticket_status ts
    JOIN 
        ticket_info ti ON ts.ticket_id = ti.ticket_id
    WHERE 
        ts.ticket_token = p_ticket_token AND ts.is_active = TRUE;
END$$

DELIMITER ;
