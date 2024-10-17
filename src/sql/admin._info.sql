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