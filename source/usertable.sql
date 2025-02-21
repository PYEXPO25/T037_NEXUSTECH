CREATE DATABASE attendance_db;

USE attendance_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('Student', 'Faculty') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
