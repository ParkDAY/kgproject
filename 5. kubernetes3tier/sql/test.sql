alter user 'root'@'localhost' identified by 'root';
alter user 'root'@'%' identified by 'root';
DROP DATABASE IF EXISTS pratice_board;
create database TESTDB;
use TESTDB;

CREATE TABLE test_table (
  `num` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(50) NOT NULL,
  `writer` VARCHAR(50) NOT NULL,
  `content` TEXT NOT NULL,
  `reg_date` DATETIME NOT NULL
  );

COMMIT;