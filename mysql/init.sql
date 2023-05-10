CREATE DATABASE IF NOT EXISTS sales_db;

USE sales_db;

CREATE TABLE IF NOT EXISTS sales(
    sales_id int primary key AUTO_INCREMENT,
    source varchar(100),
    state varchar(2),
    total_sum_amount float
);