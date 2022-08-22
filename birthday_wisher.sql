CREATE TABLE Users
(
	email varchar(255) PRIMARY KEY NOT NULL,
    firstName varchar(255) NOT NULL,
    lastName varchar(255) NOT NULL,
	birthdate datetime NOT NULL
);




DELIMITER //

CREATE PROCEDURE getTodaysBirthdays()
BEGIN
SET time_zone = "-07:00";
SELECT * FROM Users WHERE MONTH(birthdate) = MONTH(NOW()) AND DAY(birthdate) = DAY(NOW())
OR (
            (
                YEAR(NOW()) % 4 <> 0
                OR (
                        YEAR(NOW()) % 100 = 0
                        AND YEAR(NOW()) % 400 <> 0
                    )
            )
            AND DAY(NOW()) = '01'
            AND MONTH(NOW()) = '03'
            AND DAY(birthdate) = '29'
            AND MONTH(birthdate) = '02'
        );
END //

DELIMITER ;





DELIMITER //

CREATE PROCEDURE deleteUser(IN emailToBeRemoved varchar(255))
BEGIN
	DELETE FROM Users
    WHERE email = emailToBeRemoved;
END //

DELIMITER ;




DELIMITER //

CREATE PROCEDURE addUser(IN email varchar(255), firstName varchar(255), lastName varchar(255), birthdate datetime)
BEGIN
	INSERT INTO Users
    VALUES (email, firstName, lastName, birthdate);
END //

DELIMITER ;
