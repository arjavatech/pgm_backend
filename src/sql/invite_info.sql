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
    IN p_status VARCHAR(255),
    IN p_last_modified_by VARCHAR(250)
)
BEGIN
    INSERT INTO invite_info (email, url, time_stamp, status,last_modified_by)
    VALUES (p_email, p_url, p_time_stamp, p_status,p_last_modified_by);
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
    IN p_status VARCHAR(255),
    IN p_last_modified_by VARCHAR(250)

)
BEGIN
    UPDATE invite_info
    SET 
        url = COALESCE(p_url, url),
        time_stamp = COALESCE(p_time_stamp, time_stamp),
        status = COALESCE(p_status, status)
        last_modified_by = COALESCE(p_last_modified_by,last_modified_by)
    WHERE 
        email = p_email;
END //

DELIMITER ;