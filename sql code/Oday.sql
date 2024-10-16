CREATE DATABASE supermarketProject;
use supermarketProject;

CREATE TABLE customers (
  customerID int unsigned NOT NULL AUTO_INCREMENT,
  name varchar(50) DEFAULT NULL,
  phone varchar(15) DEFAULT NULL,
  email varchar(50) DEFAULT NULL,
  PRIMARY KEY (customerID)
);

CREATE TABLE suppliers (
  supplierID int unsigned NOT NULL AUTO_INCREMENT,
  name varchar(50) DEFAULT NULL,
  phone varchar(15) DEFAULT NULL,
  category varchar(30) DEFAULT NULL,
  PRIMARY KEY (supplierID)
) ;

CREATE TABLE products (
  productID int unsigned NOT NULL AUTO_INCREMENT,
  name varchar(50) DEFAULT NULL,
  quantity int unsigned DEFAULT NULL,
  unit varchar(30) DEFAULT NULL,
  category varchar(30) DEFAULT NULL,
  supplierID int unsigned DEFAULT NULL,
  price float unsigned DEFAULT NULL,
  PRIMARY KEY (productID),
  KEY supplierID (supplierID),
  CONSTRAINT products_ibfk_1 FOREIGN KEY (supplierID) REFERENCES suppliers (supplierID)
);

CREATE TABLE sales (
  saleID int NOT NULL AUTO_INCREMENT,
  customerID int unsigned NOT NULL,
  employeeID int DEFAULT NULL,
  payment_method varchar(15) DEFAULT NULL,
  total int DEFAULT NULL,
  time datetime DEFAULT NULL,
  PRIMARY KEY (saleID),
  KEY sales_ibfk_2 (customerID),
  CONSTRAINT sales_ibfk_1 FOREIGN KEY (customerID) REFERENCES customers (customerID),
  CONSTRAINT sales_ibfk_2 FOREIGN KEY (customerID) REFERENCES customers (customerID)
);

CREATE TABLE solditem (
  solditemID int unsigned NOT NULL AUTO_INCREMENT,
  productName varchar(50) DEFAULT NULL,
  productID int unsigned DEFAULT NULL,
  saleID int unsigned DEFAULT NULL,
  quantity int DEFAULT NULL,
  price int DEFAULT NULL,
  PRIMARY KEY (solditemID)
);

CREATE TABLE employee (
  employeeID int unsigned NOT NULL AUTO_INCREMENT,
  username varchar(50) NOT NULL,
  name varchar(50) DEFAULT NULL,
  password varchar(50) DEFAULT NULL,
  email varchar(50) DEFAULT NULL,
  age int unsigned DEFAULT NULL,
  phone varchar(15) DEFAULT NULL,
  title varchar(50) NOT NULL,
  hourly_pay int DEFAULT NULL,
  start_date date DEFAULT NULL,
  PRIMARY KEY (employeeID,username)
);

insert into employee(username, name, password, email, age, phone, title, hourly_pay, start_date) values ('hamza1', 'hamza najjar', 'hamza123','hamza@gmail.com' , 21,'97058972394' , 'manager' , 15, '2020-09-12');