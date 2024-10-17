    CREATE TABLE ticket_status (
        ticket_token VARCHAR(250) PRIMARY KEY,
        company_id VARCHAR(250) NOT NULL,
        employee_id VARCHAR(250) NOT NULL,
        ticket_id INT NOT NULL,
        work_started_time DATETIME DEFAULT NULL,
        work_ended_time DATETIME DEFAULT NULL,
        photos TEXT DEFAULT NULL,
        service_status ENUM('rejected', 'pending', 'inprogress', 'completed', 'assigned') DEFAULT 'pending',
        rejected_reason TEXT DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    );
DELIMITER $$

CREATE PROCEDURE spCreateTicketStatus(
    IN p_ticket_token VARCHAR(36),
    IN p_company_id VARCHAR(36),
    IN p_employee_id VARCHAR(36),
    IN p_ticket_id INT,
    IN p_work_started_time DATETIME,
    IN p_work_ended_time DATETIME,
    IN p_photos TEXT,
    IN p_service_status ENUM('rejected', 'pending', 'inprogress', 'completed', 'assigned'),
    IN p_rejected_reason TEXT
    IN p_last_modified_by VARCHAR(250)
)
BEGIN
    INSERT INTO ticket_status (
        ticket_token, company_id, employee_id, ticket_id, work_started_time, work_ended_time, 
        photos, service_status, rejected_reason,last_modified_by
    )
    VALUES (
        p_ticket_token, p_company_id, p_employee_id, p_ticket_id, p_work_started_time, 
        p_work_ended_time, p_photos, p_service_status, p_rejected_reason,p_last_modified_by
    );
END$$

DELIMITER 

DELIMITER $$

CREATE PROCEDURE spGetTicketStatusById(
    IN p_ticket_token VARCHAR(36)
)
BEGIN
    SELECT * FROM ticket_status 
    WHERE ticket_token = p_ticket_token AND is_active = TRUE;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE spGetAllActiveTicketStatuses()
BEGIN
    SELECT * FROM ticket_status 
    WHERE is_active = TRUE;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE spUpdateTicketStatus(
    IN p_ticket_token VARCHAR(36),
    IN p_company_id VARCHAR(36),
    IN p_employee_id VARCHAR(36),
    IN p_ticket_id INT,
    IN p_work_started_time DATETIME,
    IN p_work_ended_time DATETIME,
    IN p_photos TEXT,
    IN p_service_status ENUM('rejected', 'pending', 'inprogress', 'completed', 'assigned'),
    IN p_rejected_reason TEXT,
    IN p_last_modified_by
)
BEGIN
    UPDATE ticket_status 
    SET 
        company_id = p_company_id,
        employee_id = p_employee_id,
        ticket_id = p_ticket_id,
        work_started_time = p_work_started_time,
        work_ended_time = p_work_ended_time,
        photos = p_photos,
        service_status = p_service_status,
        rejected_reason = p_rejected_reason,
        updated_at = CURRENT_TIMESTAMP,
        last_modified_by = p_last_modified_by
    WHERE ticket_token = p_ticket_token AND is_active = TRUE;
END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE spDeleteTicketStatus(
    IN p_ticket_token VARCHAR(36)
)
BEGIN
    UPDATE ticket_status 
    SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
    WHERE ticket_token = p_ticket_token;
END$$

DELIMITER ;
