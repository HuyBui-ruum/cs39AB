CREATE DATABASE ethereum;

USE ethereum;

CREATE TABLE quotes (
  `date` DATE      PRIMARY KEY,
  `time` TIME NOT NULL,
  price      DECIMAL(8, 4) NOT NULL
);

CREATE USER 'ethereum' IDENTIFIED BY '12345678';

GRANT ALL ON TABLE quotes TO 'ethereum';


