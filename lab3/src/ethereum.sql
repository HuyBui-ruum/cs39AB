CREATE DATABASE ethereum;

USE ethereum;

CREATE TABLE prices (
  `datetime` DATETIME      PRIMARY KEY,
  price      DECIMAL(8, 4) NOT NULL
);

CREATE USER 'ethereum' IDENTIFIED BY '12345678';

GRANT ALL ON TABLE quotes TO 'ethereum';


