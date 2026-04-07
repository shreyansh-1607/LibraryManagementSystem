CREATE DATABASE IF NOT EXISTS Library;
SHOW DATABASES;
USE Library;

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
	username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'librarian') NOT NULL
);

-- inserting default acc (pass: admin123 and lib123)
INSERT IGNORE INTO users VALUES ('admin', 'admin123', 'admin');
INSERT IGNORE INTO users VALUES ('lib1', 'lib123', 'librarian');

CREATE TABLE IF NOT EXISTS bookrecord (
	Bno VARCHAR(10) PRIMARY KEY, 
    ISBN  VARCHAR(20) UNIQUE,
    Bname VARCHAR(100) NOT NULL,
    auth VARCHAR(100),
    price INT,
    publ VARCHAR(100),
    category VARCHAR(50),
    total_qty INT,
    avail_qty INT,
    d_o_purchase DATE
);

CREATE TABLE IF NOT EXISTS member (
	Mno VARCHAR(10) PRIMARY KEY,
    Mname VARCHAR(100) NOT NULL,
    mob VARCHAR(15) ,
    email VARCHAR(100),
    mem_type ENUM('student', 'faculty') DEFAULT 'student',
    DOP DATE,
    Adr VARCHAR(120)
);

CREATE TABLE IF NOT EXISTS issue (
	issue_id INT AUTO_INCREMENT PRIMARY KEY,
    Bno VARCHAR(10) NOT NULL,
    Mno VARCHAR(10) NOT NULL,
    d_o_issue DATE,
    due_date DATE,
    d_o_ret DATE DEFAULT NULL,
    fine INT DEFAULT 0,
    FOREIGN KEY(Bno) REFERENCES bookrecord(Bno),
    FOREIGN KEY(Mno) REFERENCES member(Mno)
);


DELIMITER //
CREATE TRIGGER set_due_date
BEFORE INSERT ON issue
FOR EACH ROW
BEGIN
  IF NEW.due_date IS NULL THEN
    SET NEW.due_date = DATE_ADD(NEW.d_o_issue, INTERVAL 3 MONTH);
  END IF;
END;
//
DELIMITER ;

    
	
	