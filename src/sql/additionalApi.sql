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
use pgm;      
DELIMITER $$

CREATE PROCEDURE spUpdateTicketAndStatus(
    IN p_company_id VARCHAR(255),
    IN p_ticket_id INT,
    IN p_employee_id VARCHAR(255)
)
BEGIN
    -- Update service_status to 'inprogress' in the ticket_status table
    UPDATE ticket_status
    SET service_status = 'inprogress'
    WHERE company_id = p_company_id
      AND ticket_id = p_ticket_id
      AND employee_id = p_employee_id;

    -- Update status to 2 in the ticket_info table
    UPDATE ticket_info
    SET status = 2
    WHERE ticket_id = p_ticket_id;

    -- Handle errors
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Update failed for one or both tables';
    END IF;
END$$

DELIMITER ;

CREATE DEFINER=`root`@`localhost` PROCEDURE `spUpdateTicketAndEmployeeStatus`(
    IN p_company_id VARCHAR(250),
    IN p_ticket_id INT,
    IN p_employee_id VARCHAR(250)
)
BEGIN
    -- Start a transaction
    START TRANSACTION;

    -- Step 1: Update ticket_status table to set the service_status to 'inprogress'
    UPDATE ticket_status
    SET service_status = 'inprogress', is_active = 1
    WHERE company_id = p_company_id
      AND ticket_id = p_ticket_id
      AND employee_id = p_employee_id;

    -- Step 2: Update ticket_info table to set status to 2
    UPDATE ticket_info
    SET status = 2, is_active = 1
    WHERE ticket_id = p_ticket_id;

    -- Step 3: Update employee table to increase employee_no_of_completed_work by 1
    -- and decrease no_of_pending_works by 1
    UPDATE employee
    SET employee_no_of_completed_work = employee_no_of_completed_work + 1,
        no_of_pending_works = no_of_pending_works - 1
    WHERE employee_id = p_employee_id;

    -- Check for any errors
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
    ELSE
        COMMIT;
    END IF;
END



CREATE DEFINER=`root`@`localhost` PROCEDURE `GetTicketDetails`()
BEGIN
    SELECT 
        ticket_id,
        ticket_type AS issue_type,
        name AS customer_name,
        phone_number,
        complain_raised_date AS date,
        city
    FROM 
        ticket_info
    WHERE 
        is_active = TRUE;
END





DELIMITER //

CREATE PROCEDURE spGetTicketInfoCustom()
BEGIN
    SELECT 
        ticket_id, 
        ticket_type AS issue_type, 
        name AS customer_name, 
        phone_number AS phone, 
        complain_raised_date AS date, 
        city
    FROM ticket_info;
END //

DELIMITER ;



DELIMITER //

CREATE PROCEDURE RejectTicket(
    IN p_ticket_id INT,
    IN p_company_id VARCHAR(250),
    IN p_employee_id VARCHAR(250)
)
BEGIN
    -- Update ticket_status table, set is_active to FALSE
    UPDATE ticket_status 
    SET is_active = FALSE 
    WHERE ticket_id = p_ticket_id
    AND company_id = p_company_id
    AND employee_id = p_employee_id;

    -- Update ticket_info table, set status to 1
    UPDATE ticket_info 
    SET status = 1
    WHERE ticket_id = p_ticket_id
    AND company_id = p_company_id;
END //

DELIMITER ;
