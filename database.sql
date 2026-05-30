CREATE DATABASE eduvault_ai;
USE eduvault_ai;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    roll_no VARCHAR(50) UNIQUE,
    email VARCHAR(100),
    password VARCHAR(255),
    role ENUM('student','admin') DEFAULT 'student'
);

CREATE TABLE student_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no VARCHAR(50),
    tenth_marks VARCHAR(20),
    inter_marks VARCHAR(20),
    btech_cgpa VARCHAR(20),
    skills TEXT,
    certifications TEXT,
    achievements TEXT,
    resume_file VARCHAR(255),
    memo_file VARCHAR(255)
);